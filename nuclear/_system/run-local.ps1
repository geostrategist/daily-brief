# Nuclear brief - local daily draft run.
#
# Fired by Windows Task Scheduler at 02:00. Leaves a draft in nuclear/_drafts/
# and stops: no commit, no push. Publishing is a separate, human-gated step
# (see publish.py).
#
# This wrapper is deliberately ASCII-only. Windows PowerShell 5.1 mis-decodes
# non-ASCII script text often enough that Chinese string literals here break the
# parser; all Chinese lives in the files this script reads, never inline.
#
# Manual test:
#   powershell -ExecutionPolicy Bypass -File nuclear\_system\run-local.ps1
#   powershell -ExecutionPolicy Bypass -File nuclear\_system\run-local.ps1 -Date 20260820

param(
    [string]$Date = ""              # YYYYMMDD; defaults to today
)

$ErrorActionPreference = "Stop"

$repo   = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)   # ...\09_daily_brief
$drafts = Join-Path $repo "nuclear\_drafts"
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

# A run already in flight must not be duplicated. The draft-exists check above
# cannot catch this: during generation the file does not exist yet, so a second
# invocation sails past it and starts a parallel run. That happened on the main
# site on 2026-08-22 when a scheduled run fired while a manual run was still
# working, burning API budget on a discarded second copy.
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

$claude = (Get-Command claude -ErrorAction SilentlyContinue).Source
if (-not $claude) { Say "claude CLI not found on PATH"; exit 1 }

$promptFile   = Join-Path $repo "nuclear\_system\DAILY_PROMPT.md"
$overrideFile = Join-Path $repo "nuclear\_system\LOCAL_OVERRIDE.md"
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

    if (Test-Path $draft) {
        $kb = [math]::Round((Get-Item $draft).Length / 1KB, 1)
        Say "done: $draft ($kb KB)"
        Say "review it, then: python nuclear\_system\publish.py $Date"
    } else {
        Say "run finished but no draft was produced - see log: $log"
        exit 1
    }
}
finally {
    Pop-Location
    Remove-Item $promptTmp -ErrorAction SilentlyContinue
    Remove-Item $lock -Force -ErrorAction SilentlyContinue
}
