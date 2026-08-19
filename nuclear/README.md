# 核能晨報 · Nuclear Daily Brief

每日巡檢七個主題並產出一份核能晨報：台灣核能爭議、全球核電與 SMR、日本核電重啟、
歐洲核能、南韓核能、美國核安與核子保安、核燃料與產業鏈。

網站：https://geostrategist.github.io/daily-brief/nuclear/

---

## 這是什麼

母站「實踐國企晨報」的子站，沿用同一套已驗證的架構：沒有後端的靜態網站，
每天由 Claude Code 排程 agent 巡檢固定來源、比對前 21 份晨報、只寫變化，
產出一份 Markdown 檔並推上 GitHub Pages。

**為什麼另開子站而非併入母站主題七**：母站七大主題共用一份晨報，核能被壓縮到每日一至兩則。
本站不受此限，七個主題各自成節，且可寫到機組編號與單位的層級。
母站主題七自本站上線後改為只寫當日核能最重大的一件事，避免兩邊重複。

## 目錄結構

```
index.html              單檔前端，由母站 index.html 衍生
manifest.json           PWA 設定（圖示指向 ../icons/）
sw.js                   Service Worker，快取名稱與母站分離
briefs/
  manifest.json         日期索引，新的在最前面
  Brief_YYYYMMDD.md     每日晨報
_system/
  TOPICS.md             主題設定 — 改這裡就改變隔日巡檢範圍
  SOURCES.md            固定巡檢網址清單（18 個，逐一實測過）
  EDITORIAL.md          編輯規範 — 決定怎麼寫
  DAILY_PROMPT.md       排程 agent 的每日指令原文
  rebuild-manifest.py   依 briefs/ 內實際檔案重建索引
```

四份 `_system/` 設定檔是這個專案的核心。程式碼幾乎不必再動，日常調整都在這些檔案裡。

## 與母站的關係

兩站共用 repo、GitHub Pages 網域與 `icons/`，其餘各自獨立：

| 項目 | 母站 | 本站 |
|---|---|---|
| 網址 | `/daily-brief/` | `/daily-brief/nuclear/` |
| 晨報 | `briefs/` | `nuclear/briefs/` |
| 設定 | `_system/` | `nuclear/_system/` |
| 預設風格 | 報紙白 | 學術藏青 |
| localStorage 鍵 | `brief-skin` | `nuclear-skin` |
| SW 快取 | `brief-shell-v2` | `nuclear-shell-v1` |

風格設定與快取都已分離，兩站互不干擾。頁尾互相連結。

## 每日流程

見 `_system/DAILY_PROMPT.md`。摘要如下：

1. 讀 `TOPICS.md`、`SOURCES.md`、`EDITORIAL.md`
2. 逐一 WebFetch 18 個固定來源，取得失敗者記錄於當日晨報，不靜默略過
3. 回溯比對近 21 份晨報，只寫新增與變化
4. 產出 `nuclear/briefs/Brief_YYYYMMDD.md`
5. `python nuclear/_system/rebuild-manifest.py`
6. commit 並 push，GitHub Pages 自動發布

## 本機預覽

```bash
python -m http.server 8899
# 開 http://localhost:8899/nuclear/
```

`file://` 直接開會因 CORS 而讀不到 `briefs/`，必須起一個 server。

## 這個領域特有的三個坑

架構沿用母站，但核能報導有三類母站不會遇到的錯誤，規範中已各有對應條文：

**一、機組指涉不清**（`EDITORIAL.md` 第四節）。同一電廠常有多部機組，狀態各不相同。
「柏崎刈羽核電廠重啟」是無效資訊，「柏崎刈羽 6 號機重啟審查通過」才是。
併網、商轉、臨界、重啟審查通過、地方同意，這些詞的時間可差數年，混用即為錯誤。

**二、單位與數量級**（第五節）。發電容量的 MWe 與 MWt 可差三倍；日文的「万kW」
經英文摘要常掉一個數量級。**創刊日就遇到一次**：島根 2 號機的「82.0 万kW」
（＝820 MWe）被英文途徑誤讀為 82.0 MW，回查日文原文才攔下。鈾的磅 U3O8、
噸鈾（tU）、SWU 三種單位也不可互換。

**三、立場**（第六節）。核能是台灣高度政治化的議題。本報只報事實與其後果，不倡議。
不用褒貶性形容詞描述核能本身；擁核與反核的主張一律以引述處理；
判讀可以有判斷，但判斷須指向可觀察的後果，不指向價值評價。
產業協會（nucleareurope、NEI）與反核團體適用同一套來源等級規則，不因立場方向而寬嚴不一。

## 已知不可用的來源

`SOURCES.md` 文末有完整清單與實測結果。最需要注意的是：

**NRC（nrc.gov）全站對本系統回 403**，HTML 與 RSS、curl 與 WebFetch 都一樣。
美國管制動態一律經 ANS Nuclear Newswire 等第三方取得，
依規範**不得標 A 級**，並須在待查核註明「本報未取得 NRC 原文」。

韓聯社與 Korea Herald 為 JS 渲染，靜態抓取取不到標題；台電的「核能發電」頁
只有導覽選單，機組狀態改用開放資料 JSON（判讀規則見 `SOURCES.md`）。

## 設計取捨

**為什麼是 Markdown 而非 HTML**：內容與呈現分離。改版面不必碰內容，改內容不必碰程式。

**為什麼由母站 index.html 衍生而非重寫**：前端的卡片化、來源等級標籤、
事實與判讀分段等邏輯全部是通用的——它依渲染後的 H2／H3 建構，不綁定特定主題。
只換了品牌字串、預設配色，以及把「前一日市場」的漲跌上色改為機組狀態的異動標示。

**為什麼機組狀態表取代市場表**：核能晨報的讀者要先知道「哪些機組現在是什麼狀態」，
就像財經讀者要先看價格。台灣機組即使無異動也固定列出。

**免責**：本報彙整公開資訊，非投資或決策建議。本報不倡議擁核或反核，只報事實與其後果。

---

實踐大學高雄校區 國際企業管理學系
