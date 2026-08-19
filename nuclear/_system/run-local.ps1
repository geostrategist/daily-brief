# 核能晨報 · 本機每日產製
#
# 由 Windows 工作排程器在每天早上八點觸發。跑完只會在 nuclear/_drafts/ 留下一份草稿，
# 不 commit、不 push——上傳與否由人決定，見 publish.py。
#
# 手動測試：
#   powershell -ExecutionPolicy Bypass -File nuclear\_system\run-local.ps1
#   powershell -ExecutionPolicy Bypass -File nuclear\_system\run-local.ps1 -Date 20260820

param(
    [string]$Date = ""              # YYYYMMDD，省略則用今天
)

$ErrorActionPreference = "Stop"

$repo    = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)   # …\09_daily_brief
$drafts  = Join-Path $repo "nuclear\_drafts"
$logs    = Join-Path $drafts "logs"
if (-not (Test-Path $drafts)) { New-Item -ItemType Directory -Path $drafts  | Out-Null }
if (-not (Test-Path $logs))   { New-Item -ItemType Directory -Path $logs    | Out-Null }

if ([string]::IsNullOrWhiteSpace($Date)) { $Date = Get-Date -Format "yyyyMMdd" }
$stamp   = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$draft   = Join-Path $drafts "Brief_$Date.md"
$log     = Join-Path $logs   "$Date.log"

"[$stamp] 開始產製 $Date" | Tee-Object -FilePath $log

# 草稿已存在就不覆蓋——避免排程重跑蓋掉已經看過或改過的稿子。
# 要重跑先自行刪除該檔。
if (Test-Path $draft) {
    "[$stamp] 草稿已存在，略過：$draft" | Tee-Object -FilePath $log -Append
    "   要重跑請先刪除該檔。" | Tee-Object -FilePath $log -Append
    exit 0
}

$claude = (Get-Command claude -ErrorAction SilentlyContinue).Source
if (-not $claude) {
    "[$stamp] 找不到 claude CLI，中止。" | Tee-Object -FilePath $log -Append
    exit 1
}

# 指令原文放在 DAILY_PROMPT.md，與雲端版共用同一份規範。
# 此處只覆寫「寫到哪裡」與「不要 push」兩件事。
$promptFile = Join-Path $repo "nuclear\_system\DAILY_PROMPT.md"
if (-not (Test-Path $promptFile)) {
    "[$stamp] 找不到 DAILY_PROMPT.md，中止。" | Tee-Object -FilePath $log -Append
    exit 1
}
$basePrompt = Get-Content $promptFile -Raw -Encoding UTF8

$override = @"

---

# 本機執行的覆寫規則（優先於上文）

本次為**本機草稿產製**，不是雲端發布。上文第七步的發布流程**全部不執行**。

1. **寫到 ``nuclear/_drafts/Brief_$Date.md``**，不要寫進 ``nuclear/briefs/``。
2. **不要執行 rebuild-manifest.py。**
3. **不要 git add、不要 commit、不要 push。** 這份稿子要先給人看過。
4. 歷史比對照舊——讀 ``nuclear/briefs/`` 內既有晨報（那是已發布的），
   另外也讀 ``nuclear/_drafts/`` 內是否有尚未發布的近日草稿，避免與未發布稿重複。
5. 今天的日期是 **$Date**（台灣時間），直接用，不必再自行推算。

其餘規範（分節、來源等級、待查核、機組識別、單位、規範編號、立場中立、安全規範）
一律照上文執行，不因為是草稿而放寬。
"@

$prompt = $basePrompt + $override

Push-Location $repo
try {
    "[$stamp] 呼叫 claude -p …（這一步需要數分鐘）" | Tee-Object -FilePath $log -Append

    # --permission-mode acceptEdits：無人看管，不能停在權限詢問
    # 允許的工具限制在巡檢與寫檔，不給 git 相關能力
    $prompt | & $claude -p `
        --permission-mode acceptEdits `
        --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "WebFetch" "WebSearch" "Bash(python:*)" "Bash(date:*)" "Bash(curl:*)" `
        2>&1 | Tee-Object -FilePath $log -Append

    $done = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    if (Test-Path $draft) {
        $kb = [math]::Round((Get-Item $draft).Length / 1KB, 1)
        "[$done] 完成：$draft（$kb KB）" | Tee-Object -FilePath $log -Append
        "[$done] 過目後執行：python nuclear\_system\publish.py" | Tee-Object -FilePath $log -Append
    } else {
        "[$done] 跑完但沒有產生草稿檔，請看上面的輸出。" | Tee-Object -FilePath $log -Append
        exit 1
    }
}
finally {
    Pop-Location
}
