# Daily brief - local draft run.
#
# Fired by Windows Task Scheduler Mon/Wed/Fri at 04:00. Leaves a draft in _drafts/ and
# stops: no commit, no push. Publishing is a separate, human-gated step
# (see publish.py).
#
# Replaces the cloud routines trig_016pPLZ... and trig_01Ms15Bw..., both
# disabled 2026-08-20. Their sandbox had no network egress: every source
# returned EGRESS_BLOCKED and market.py got 403 on CONNECT, so two consecutive
# days produced a brief with zero content. This machine reaches all 26 sources.
#
# This wrapper is deliberately ASCII-only. Windows PowerShell 5.1 mis-decodes
# non-ASCII script text often enough that Chinese string literals here break the
# parser; all Chinese lives in the files this script reads, never inline.
#
# Manual test:
#   powershell -ExecutionPolicy Bypass -File _system\run-local.ps1
#   powershell -ExecutionPolicy Bypass -File _system\run-local.ps1 -Date 20260821

param(
    [string]$Date = ""              # YYYYMMDD; defaults to today
)

$ErrorActionPreference = "Stop"

$repo   = Split-Path -Parent $PSScriptRoot        # ...\09_daily_brief
$drafts = Join-Path $repo "_drafts"
$logs   = Join-Path $drafts "logs"
foreach ($d in @($drafts, $logs)) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d | Out-Null }
}

if ([string]::IsNullOrWhiteSpace($Date)) { $Date = Get-Date -Format "yyyyMMdd" }
$draft = Join-Path $drafts "Brief_$Date.md"
$log   = Join-Path $logs   "$Date.log"

function Say($msg) {
    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $msg
    Write-Output $line
    Add-Content -Path $log -Value $line -Encoding UTF8
}

Say "start $Date"

# Never clobber an existing draft: a scheduler re-run must not overwrite a draft
# already reviewed or hand-edited. Delete the file to force a rebuild.
if (Test-Path $draft) {
    Say "draft exists, skipping: $draft"
    exit 0
}

# Nor re-run over a brief already published for this date. Without this the run
# burns several minutes and then the agent correctly refuses to write a
# duplicate, which the exit-1 path below would misreport as a broken run.
$published = Join-Path $repo "briefs\Brief_$Date.md"
if (Test-Path $published) {
    Say "already published, skipping: $published"
    exit 0
}

# A run already in flight must not be duplicated. The draft-exists check above
# cannot catch this: during generation the file does not exist yet, so a second
# invocation sails past it and starts a parallel run. That happened on
# 2026-08-22 when a scheduled run fired while a manual run was still working,
# burning API budget on a discarded second copy.
#
# The lock records the owning PID so a lock left behind by a crash or a hard
# kill does not block every future run. If that process is gone, the lock is
# stale and we take it over.
$lock = Join-Path $drafts ".run-$Date.lock"
if (Test-Path $lock) {
    $owner = (Get-Content $lock -Raw -ErrorAction SilentlyContinue).Trim()
    $alive = $false
    if ($owner -match '^\d+$') {
        $alive = [bool](Get-Process -Id ([int]$owner) -ErrorAction SilentlyContinue)
    }
    if ($alive) {
        Say "another run is in progress (pid $owner), skipping"
        exit 0
    }
    Say "stale lock from pid $owner, taking over"
    Remove-Item $lock -Force -ErrorAction SilentlyContinue
}
Set-Content -Path $lock -Value $PID -Encoding ASCII

# Prefer a CLI on PATH. This machine has none: Claude Code is installed as the
# VS Code extension, which ships its own binary under a version-stamped folder.
# That path changes on every extension update (2.1.234 and 2.1.236 both present
# at time of writing), so resolve the newest rather than hard-coding one.
$claude = (Get-Command claude -ErrorAction SilentlyContinue).Source
if (-not $claude) {
    $bundled = Join-Path $env:USERPROFILE ".vscode\extensions\anthropic.claude-code-*\resources\native-binary\claude.exe"
    $claude = Get-Item $bundled -ErrorAction SilentlyContinue |
              Sort-Object LastWriteTime -Descending |
              Select-Object -First 1 -ExpandProperty FullName
    if ($claude) { Say "claude not on PATH, using bundled: $claude" }
}
if (-not $claude) {
    Say "claude CLI not found on PATH and no VS Code extension binary located"
    Say "fix: npm install -g @anthropic-ai/claude-code"
    exit 1
}

$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) {
    Say "python not found on PATH"
    Remove-Item $lock -Force -ErrorAction SilentlyContinue
    exit 1
}

$promptFile   = Join-Path $repo "_system\DAILY_PROMPT.md"
$overrideFile = Join-Path $repo "_system\LOCAL_OVERRIDE.md"
foreach ($f in @($promptFile, $overrideFile)) {
    if (-not (Test-Path $f)) { Say "missing prompt file: $f"; exit 1 }
}

# The shared spec plus the local-run override (draft path, no push).
# {{DATE}} is the only substitution.
$prompt = (Get-Content $promptFile -Raw -Encoding UTF8) + "`n`n" +
          ((Get-Content $overrideFile -Raw -Encoding UTF8) -replace '\{\{DATE\}\}', $Date)

$promptTmp = Join-Path $logs "prompt_$Date.txt"
Set-Content -Path $promptTmp -Value $prompt -Encoding UTF8

Push-Location $repo
try {
    Say "invoking claude -p (several minutes)"

    # acceptEdits: unattended, so it must not block on a permission prompt.
    # Tools are limited to research and file writes - no git.
    # The prompt goes in on stdin. Passing it positionally lets a bare
    # multi-word argument be swallowed by the preceding --allowedTools list.
    $tools = "Read,Write,Edit,Glob,Grep,WebFetch,WebSearch,Bash(python:*),Bash(date:*),Bash(curl:*)"
    Get-Content $promptTmp -Raw -Encoding UTF8 |
        & $claude -p --permission-mode acceptEdits --allowedTools $tools 2>&1 |
        ForEach-Object { Add-Content -Path $log -Value $_ -Encoding UTF8 }

    # The agent is told to leave a draft and never touch git. It does not
    # always obey: on 2026-08-27 nuclear and the main site both committed and
    # pushed themselves, which silently bypassed the publish.py --auto quality
    # gate and made the run look like a failure (no draft -> exit 1).
    #
    # So decide on what is actually on disk rather than on what was asked for.
    $selfPublished = Test-Path $published

    if ($selfPublished) {
        # It published itself. Say so loudly - this bypassed the gate - then
        # run the checks read-only so the warnings still reach the log.
        Say "WARNING: agent wrote $published directly, bypassing the quality gate"
        if (Test-Path $draft) {
            Say "draft also present, left in place: $draft"
        }
        $head = (& git -C $repo log -1 --format=%H -- "briefs/Brief_$Date.md" 2>$null)
        if ($head) {
            Say "already committed as $head"
        } else {
            Say "NOT COMMITTED - it is on disk but not pushed; publish it by hand"
        }
        Say "post-hoc check (advisory, already public):"
        & $py (Join-Path $repo "_system\publish.py") $Date --dry-run --auto 2>&1 |
            ForEach-Object { Add-Content -Path $log -Value $_ -Encoding UTF8 }
        exit 0
    }

    if (-not (Test-Path $draft)) {
        Say "run finished but no draft was produced - see log: $log"
        exit 1
    }

    $kb = [math]::Round((Get-Item $draft).Length / 1KB, 1)
    Say "done: $draft ($kb KB)"

    # Publish through the gate: it stops on a truncated draft, a leftover
    # placeholder or a missing fixed section and keeps the draft for the
    # morning. Milder findings stay advisory and go out, logged either way.
    Say "publishing"
    & $py (Join-Path $repo "_system\publish.py") $Date --auto 2>&1 |
        ForEach-Object { Add-Content -Path $log -Value $_ -Encoding UTF8 }
    if ($LASTEXITCODE -eq 0) {
        Say "published $Date"
    } else {
        Say "publish aborted (exit $LASTEXITCODE), draft kept: $draft"
        exit 1
    }
}
finally {
    Pop-Location
    Remove-Item $promptTmp -ErrorAction SilentlyContinue
    Remove-Item $lock -Force -ErrorAction SilentlyContinue
}
