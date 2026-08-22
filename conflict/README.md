# 國際衝突晨報 · International Conflict Daily Brief

每日巡檢並產出一份晨報。母站「實踐國企晨報」的子站，沿用同一套架構但有自己的
`_system/` 設定與 `briefs/`。

網站：https://geostrategist.github.io/daily-brief/conflict/

---

## 這是什麼

問一個問題：**國家之間正在如何對抗**

一個沒有後端的靜態網站。每天由本機排程在 04:00 巡檢固定來源、比對前 21 份晨報、
只寫變化，產出草稿到 `_drafts/`，**由人過目後才發布**。

## 版面

十一個固定欄位：今日三分鐘摘要、兩岸、東亞、南海、南太平洋、南亞、中亞、跨區域結構、未來事件行事曆、建議研究與寫作行動、應持續追蹤議題。

**第 2 至 8 節每日固定出現，無實質內容者寫一則巡檢基線，不得整節略去。**
理由是這些欄位各自代表一個不同的觀察位置，「今日某處無事」本身即為資訊，
且固定結構使讀者每日看見同一組區分。

## 本站特有的三條紀律

**交戰雙方的說法都是說法**（`EDITORIAL.md` 第四節）。交戰方的官方戰報一律為〔C〕級，
即使出自國防部——戰時的官方發布是交戰行為的一部分。雙方數字不一致時並列，
**不取平均、不擇一**。無法判斷孰是孰非時寫「雙方說法不一致」。

**階段標記**。六區依地理分節，但每則標題後標 `[徵候]` `[交戰]` `[談判]` `[停火]` `[結構]`，
讓讀者看得出一件事是剛起、正在打、還是在談。標記錯誤比沒有標記嚴重。

**每區三則上限**（第九節）。不因某區當日事件多而放寬。放寬會讓兩岸與南海
吃掉整份晨報，其餘四區退化為裝飾。南太平洋與中亞多數日子只有巡檢基線，這是正常的。

## 目錄結構

```
index.html              單檔前端，Service Worker 快取名稱與母站分離
manifest.json           PWA 設定
sw.js                   Service Worker
briefs/
  manifest.json         日期索引，新的在最前面
  Brief_YYYYMMDD.md     每日晨報
_drafts/                每日 04:00 產出的草稿，未發布。已 gitignore
  logs/                 每次執行的完整輸出
_system/
  TOPICS.md             欄位設定 — 改這裡就改變隔日巡檢範圍與版面
  SOURCES.md            固定巡檢網址清單，含各自的已知限制
  EDITORIAL.md          編輯規範 — 決定怎麼寫
  DAILY_PROMPT.md       每日指令原文
  LOCAL_OVERRIDE.md     本機執行時附加的覆寫規則（寫到 _drafts/、不要 push）
  run-local.ps1         本機 04:00 排程執行的腳本，只產草稿
  publish.py            過目後發布：搬進 briefs/、重建索引、commit、push
  rebuild-manifest.py   依 briefs/ 內實際檔案重建索引
  style_check.py        文體檢查，發布前跑
```

三份設定檔（TOPICS、SOURCES、EDITORIAL）是這個子站的核心。

## 每日的實際操作

04:00，Windows 工作排程器會跑 `_system/run-local.ps1`，巡檢來源、寫出草稿到
`_drafts/Brief_YYYYMMDD.md`，然後**停在那裡**。網站上不會有任何變化。

看稿：

```bash
python conflict/_system/publish.py --list       # 有哪些草稿在等
python conflict/_system/publish.py --dry-run    # 檢查結果，不動任何東西
python conflict/_system/publish.py              # 確認後發布
```

`publish.py` 會檢查固定欄位、來源等級、待查核、佔位字樣與文體。
這些是提醒，不阻擋發布——晨報是判斷，腳本代替不了。

## 本機預覽

```bash
python -m http.server 8899
# 開 http://localhost:8899/conflict/
```

`file://` 直接開會因 CORS 而讀不到 `briefs/`，必須起一個 server。

## 四站分工

| 站 | 排程 | 問的問題 |
|---|---|---|
| 實踐國企晨報（母站） | 05:00 | 國際商業與政策環境怎麼變 |
| 核能晨報 `nuclear/` | 02:00 | 核能的安全、保安、保防 |
| 國家安全晨報 `security/` | 03:00 | 台灣內部的韌性哪裡破了 |
| 國際衝突晨報 `conflict/` | 04:00 | 國家之間正在如何對抗 |

**國安站與衝突站的界線**：這件事的受害者或標的在不在台灣。在，寫國安站；不在，寫衝突站。
同一件事的兩面各寫一次時，角度須不同，不得重複敘述。

**免責**：本報彙整公開資訊，非投資或決策建議。

---

實踐大學高雄校區 國際企業管理學系
