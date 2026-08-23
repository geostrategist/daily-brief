# 國家安全晨報 · National Security Daily Brief

每日巡檢並產出一份晨報。母站「實踐國企晨報」的子站，沿用同一套架構但有自己的
`_system/` 設定與 `briefs/`。

網站：https://geostrategist.github.io/daily-brief/security/

---

## 這是什麼

問一個問題：**台灣內部的韌性哪裡破了**

一個沒有後端的靜態網站。每天由本機排程在 03:00 巡檢固定來源、比對前 21 份晨報、
只寫變化，產出草稿到 `_drafts/`，**由人過目後才發布**。

## 版面

十二個固定欄位：今日三分鐘摘要、台海軍事動態速覽、認知作戰與資訊操縱、滲透統戰與情報活動、關鍵基礎設施與資安、經濟脅迫與供應鏈韌性、移民人流與邊境管理、境外滲透案例對照、法制與國安治理、未來事件行事曆、建議研究與寫作行動、應持續追蹤議題。

**第 3 至 9 節每日固定出現，無實質內容者寫一則巡檢基線，不得整節略去。**
理由是這些欄位各自代表一個不同的觀察位置，「今日某處無事」本身即為資訊，
且固定結構使讀者每日看見同一組區分。

## 本站特有的兩條紀律

**歸因紀律**（`EDITORIAL.md` 第四節）。國安議題的報導充斥未經證實的歸因，
「這是中共認知作戰」在台灣的公共討論中經常先於證據出現。本報寫歸因時須同時交代
**誰做的歸因、用什麼方法、信心程度多高**，三者缺一就只寫現象不寫歸因。

**指控的雙面性**（第五節）。認知作戰的指控本身即為認知作戰的常見手法，
滲透的指控可被用於政治鬥爭，移民的威脅論述可被用於族群動員。
本報同時記錄現象與指控，不預設指控為真也不預設為假。
政黨互控除非進入司法程序，一律不寫。

移民欄位另有一條：涉及特定族群時**須同時列出該族群在母體中的佔比**，
避免以絕對數字製造比例錯覺。本節處理的是制度與統計，不是人。

## 目錄結構

```
index.html              單檔前端，Service Worker 快取名稱與母站分離
manifest.json           PWA 設定
sw.js                   Service Worker
briefs/
  manifest.json         日期索引，新的在最前面
  Brief_YYYYMMDD.md     每日晨報
_drafts/                每日 03:00 產出的草稿，未發布。已 gitignore
  logs/                 每次執行的完整輸出
_system/
  TOPICS.md             欄位設定 — 改這裡就改變隔日巡檢範圍與版面
  SOURCES.md            固定巡檢網址清單，含各自的已知限制
  EDITORIAL.md          編輯規範 — 決定怎麼寫
  DAILY_PROMPT.md       每日指令原文
  LOCAL_OVERRIDE.md     本機執行時附加的覆寫規則（寫到 _drafts/、不要 push）
  run-local.ps1         本機 03:00 排程執行的腳本，只產草稿
  publish.py            過目後發布：搬進 briefs/、重建索引、commit、push
  rebuild-manifest.py   依 briefs/ 內實際檔案重建索引
  style_check.py        文體檢查，發布前跑
```

三份設定檔（TOPICS、SOURCES、EDITORIAL）是這個子站的核心。

## 每日的實際操作

03:00，Windows 工作排程器會跑 `_system/run-local.ps1`，巡檢來源、寫出草稿到
`_drafts/Brief_YYYYMMDD.md`，然後**停在那裡**。網站上不會有任何變化。

看稿：

```bash
python security/_system/publish.py --list       # 有哪些草稿在等
python security/_system/publish.py --dry-run    # 檢查結果，不動任何東西
python security/_system/publish.py              # 確認後發布
```

`publish.py` 會檢查固定欄位、來源等級、待查核、佔位字樣與文體。

**兩件要知道的事**：

其一，發布用的是 `git add security/`，會把該資料夾底下**所有**未提交變更
一併納入那支 commit。若同時改了 `_system/` 的設定又發布晨報，兩者會被綁在
同一個 commit，訊息只會寫「security: 日期」。要分開就先各自 commit 再發布。

其二，發布會**刪掉草稿**。若此時排程或手動執行的 `run-local.ps1` 仍在跑，
它結束時會找不到草稿而回報「run finished but no draft was produced」並以 1 結束。
那是誤報，晨報其實已發布。確認方式為看 `briefs/` 內該日檔案是否存在。
這些是提醒，不阻擋發布——晨報是判斷，腳本代替不了。

## 本機預覽

```bash
python -m http.server 8899
# 開 http://localhost:8899/security/
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
