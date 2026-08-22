# 固定巡檢來源

每日晨報開始時，逐一 WebFetch 本清單網址。取得失敗者記錄於當日晨報的巡檢摘要，不靜默略過。

清單以外的資料，透過 WebSearch 補充，但須符合 `EDITORIAL.md` 的來源品質規則。

**本清單的網址皆於 2026-08-22 建站時實測**，狀態記於備註欄。
實測用 `curl -A "Mozilla/5.0" -o /dev/null -w "%{http_code}" -L <url>`，
WebFetch 的結果與 curl 一致（DSCA 已交叉驗證）。

---

## 台海軍事動態（欄位二）

| 來源 | 網址 | 備註 |
|---|---|---|
| 國防部即時軍事動態 | https://www.mnd.gov.tw/news/plaactlist | 200。軍機艦架次原始數據，本欄位的主力來源 |
| 海巡署 | https://www.cga.gov.tw/GipOpen/wSite/mp?mp=9997 | 200。越界漁船與公務船驅離紀錄 |

---

## 認知作戰與資訊操縱（欄位三）

| 來源 | 網址 | 備註 |
|---|---|---|
| 台灣民主實驗室 | https://doublethinklab.org/ | 200。歸因報告含方法論，本欄位品質最高的來源 |
| IORG | https://iorg.tw/ | 200。資訊操作研究，具資料集 |
| EUvsDisinfo | https://euvsdisinfo.eu/ | 200。歐盟對外事務部的假訊息資料庫，兼供欄位八 |
| 國安局 | https://www.nsb.gov.tw/ | 200。官方報告與立法院業務報告 |

---

## 滲透、統戰與情報活動（欄位四）

| 來源 | 網址 | 備註 |
|---|---|---|
| 法務部調查局 | https://www.mjib.gov.tw/news/Index?Module=1 | 200，新聞快報列表。**注意**：`/news` 回 500；`/news/Details/1/1` 雖回200但內容為 NoNews，見文末 |
| 陸委會新聞稿 | https://www.mac.gov.tw/News.aspx?n=05B73310C5C3A632 | 200。**注意**：首頁 `www.mac.gov.tw/` 回 403，須用本路徑 |
| 中央社政治 | https://www.cna.com.tw/list/aipl.aspx | 200。通訊社，作為線索 |
| 立法院議事及發言系統 | https://ppg.ly.gov.tw/ppg/ | 200。質詢紀錄與法案進度 |

---

## 關鍵基礎設施與資安（欄位五）

| 來源 | 網址 | 備註 |
|---|---|---|
| 數位發展部資安署 | https://moda.gov.tw/ACS/index | 200 |
| CISA Advisories | https://www.cisa.gov/news-events/cybersecurity-advisories | 200。含 IOC 與 TTP |
| 國防安全研究院 | https://indsr.org.tw/ | 200。兼供欄位三與欄位九 |

---

## 經濟脅迫與供應鏈韌性（欄位六）

| 來源 | 網址 | 備註 |
|---|---|---|
| 陸委會新聞稿 | https://www.mac.gov.tw/News.aspx?n=05B73310C5C3A632 | 同欄位四，兩節共用 |
| 中央社財經 | https://www.cna.com.tw/list/aie.aspx | 200。母站已驗證可用 |

---

## 移民、人流與邊境管理（欄位七）

| 來源 | 網址 | 備註 |
|---|---|---|
| 移民署 | https://www.immigration.gov.tw/ | 200。統計月報與新聞稿 |
| 勞動部勞動力發展署 | https://www.wda.gov.tw/ | 200。移工統計 |
| 內政部 | https://www.moi.gov.tw/ | 200。函釋與修法 |

---

## 境外滲透案例對照（欄位八）

| 來源 | 網址 | 備註 |
|---|---|---|
| EUvsDisinfo | https://euvsdisinfo.eu/ | 200。歐洲案例，同欄位三 |
| 日本公安調查廳 | https://www.moj.go.jp/psia/ | 200。日文，年報與內外情勢回顧 |
| ASPI | https://www.aspi.org.au/ | 200。澳洲智庫，本欄位澳紐案例的主要途徑 |
| Jamestown China Brief | https://jamestown.org/programs/cb/ | 200。中國對外影響力研究 |

**澳洲與加拿大官方來源不可用**：`asio.gov.au` 與 `canada.ca` 於本機實測連線失敗
（curl 回 `000`，非 HTTP 錯誤碼，研判為地域封鎖或 CDN 拒絕）。
本欄位的澳加案例改由 ASPI 與 WebSearch 取得，**引用時仍須回溯至官方原始文件**，
若原文取不到，於該則的「待查核」寫明。

---

## 法制與國安治理（欄位九）

| 來源 | 網址 | 備註 |
|---|---|---|
| 立法院議事及發言系統 | https://ppg.ly.gov.tw/ppg/ | 200。同欄位四 |
| 全國法規資料庫 | https://law.moj.gov.tw/ | 200。條文原文 |
| 國防安全研究院 | https://indsr.org.tw/ | 200。同欄位五 |

---

## 巡檢順序建議

1. **國防部即時軍事動態**——欄位二的表格要用，先取
2. **調查局、陸委會、中央社政治**——欄位四與六的主力
3. **台灣民主實驗室、IORG**——欄位三，更新頻率低，快速掃過即可
4. **資安署、CISA**——欄位五
5. **移民署、勞動部、內政部**——欄位七，統計類更新以月為單位
6. **EUvsDisinfo、公安調查廳、ASPI**——欄位八，取一則即可
7. **立法院、全國法規資料庫**——欄位九

---

## 已知失效與限制

- **`www.mjib.gov.tw/news` 回 500**。`/news/Details/1/1` 回200但內容為 NoNews，
  2026-08-22 首次巡檢即撞上，改用 `/news/Index?Module=1` 取得新聞快報列表。
  **此站是「200不等於巡檢成功」的實例**，取回內容後須確認確有條目。
- **`www.mac.gov.tw/` 首頁回 403**，改用 `News.aspx?n=05B73310C5C3A632`。
- **`www.asio.gov.au` 與 `www.canada.ca` 連線失敗**（`000`），見欄位八說明。
- **政府網站多為 JS 載入**，靜態抓取常取不到內文標題。
  母站 SOURCES 已記錄國科會即為此例。取不到標題時記入巡檢摘要，
  **不要因為抓到 200 就當作巡檢成功**。
- **移民署與勞動部的統計以月為單位更新**，多數日子無新數字。
  這不是巡檢失敗，寫巡檢基線即可。

---

## 來源調整紀錄

- 2026-08-22：建站，20 個來源（去重後 17 個網址），逐一實測。
  調查局與陸委會改用替代路徑，澳加官方來源不可用。
- 2026-08-23：首次巡檢後回填。調查局改用 `/news/Index?Module=1`。
  另記，首次巡檢當日陸委會、CISA、EUvsDisinfo 三站回403，事後重測均回200，
  研判為當下限流而非永久失效，清單不因單日403移除。
