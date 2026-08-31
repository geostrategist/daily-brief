# 實踐國企晨報 · KH USC IBM's Daily Brief

每週一、三、五巡檢六大主題並產出一份晨報：國際企業、東南亞、日／韓、無人載具、人工智慧、財稅與會計政策。核能已另設子站。

網站：https://geostrategist.github.io/daily-brief/

---

## 這是什麼

一個沒有後端的靜態網站。依排程由 Claude Code agent 巡檢固定來源、比對前 21 份晨報、只寫變化，產出一份 Markdown 檔並推上 GitHub Pages。

前端在瀏覽器端讀 Markdown 並渲染，支援日期切換、語音朗讀、離線閱讀與手機安裝。

## 子站

四個子站沿用同一套架構，各有自己的 `_system/` 設定與 `briefs/`：

| 子站 | 排程 | 問的問題 |
|---|---|---|
| [核能晨報](nuclear/) | 週二 02:00 | 核能的安全、保安、保防 |
| [國家安全晨報](security/) | 週一至四 03:00 | 台灣內部的韌性哪裡破了 |
| [國際衝突晨報](conflict/) | 週二、四 04:00 | 國家之間正在如何對抗 |
| [期刊晨報](journals/) | 週一 01:00 | 今天有什麼值得讀的新研究 |

本站主題七「核能產業」已於 2026-08-23 整節移除，核能一律看子站。
主題二「東南亞」的南海部分自 2026-08-22 移入衝突站，本站保留東協機制、選舉政局與供應鏈。

安全類議題不在本站新增主題。國安站與衝突站的界線是**受害者或標的在不在台灣**。

## 目錄結構

```
index.html              單檔前端（Tailwind CDN + marked + DOMPurify + Web Speech API）
manifest.json           PWA 設定
sw.js                   Service Worker：外殼快取優先，晨報內容網路優先
briefs/
  manifest.json         日期索引，新的在最前面
  Brief_YYYYMMDD.md     每份晨報
icons/                  PWA 圖示
_system/
  TOPICS.md             主題設定 — 改這裡就改變隔日巡檢範圍
  SOURCES.md            固定巡檢網址清單（26 個）
  EDITORIAL.md          編輯規範 — 決定怎麼寫
  rebuild-manifest.py   依 briefs/ 內實際檔案重建索引
nuclear/                核能晨報子站，結構同上，設定獨立
security/               國家安全晨報子站
conflict/               國際衝突晨報子站
journals/               期刊晨報子站，資料來自 Crossref API
```

三份 `_system/` 設定檔是這個專案的核心。程式碼幾乎不必再動，日常調整都在這三份檔案裡。

## 每次執行的流程

1. 讀 `_system/TOPICS.md`、`SOURCES.md`、`EDITORIAL.md`
2. 逐一 WebFetch 固定來源，取得失敗者記錄於當日晨報，不靜默略過
3. 回溯比對近 21 份晨報，只寫新增與變化
4. 產出 `briefs/Brief_YYYYMMDD.md`，含建議決策行動與應持續追蹤議題兩節
5. 更新 `briefs/manifest.json`
6. commit 並 push，GitHub Pages 自動發布

## 本機預覽

```bash
python -m http.server 8899
# 開 http://localhost:8899
```

`file://` 直接開會因 CORS 而讀不到 `briefs/`，必須起一個 server。

## 新增一份晨報

把 `Brief_YYYYMMDD.md` 放進 `briefs/`，然後：

```bash
python _system/rebuild-manifest.py
git add . && git commit -m "brief: YYYY-MM-DD" && git push
```

## 設計取捨

**為什麼是 Markdown 而非 HTML**：內容與呈現分離。改版面不必碰內容，改內容不必碰程式。

**為什麼不用框架**：沒有建置步驟，就沒有建置失敗。排程 agent 只需寫一個檔案再推上去。

**為什麼朗讀用瀏覽器 TTS 而非音檔**：不必產製、不必儲存、不必付費。代價是語音品質受限於使用者的作業系統。

**免責**：本報彙整公開資訊，非投資或決策建議。

---

實踐大學高雄校區 國際企業管理學系
