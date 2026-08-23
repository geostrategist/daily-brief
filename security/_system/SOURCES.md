# 固定巡檢來源

每日晨報開始時，逐一 WebFetch 本清單網址。取得失敗者記錄於當日晨報的巡檢摘要，不靜默略過。

清單以外的資料，透過 WebSearch 補充，但須符合 `EDITORIAL.md` 的來源品質規則。

**本清單的網址皆已實測**，狀態記於備註欄，最近一次為 2026-08-23。

**實測一律用 WebFetch，不用 curl。** 晨報產製時用的是 WebFetch，
而兩者結果會不一致——2026-08-23 的複測發現陸委會、CISA、EUvsDisinfo 三站
`curl` 回 200 但 WebFetch 回 403。以 curl 測會得到「站是好的」的錯誤結論。

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
| EUvsDisinfo | https://euvsdisinfo.eu/ | **WebFetch 回 403 不可用**，見文末。兼供欄位八 |
| 國安局 | https://www.nsb.gov.tw/ | **純JS站不可用**，全站僅3.4KB、零連結，見文末 |

---

## 滲透、統戰與情報活動（欄位四）

| 來源 | 網址 | 備註 |
|---|---|---|
| 法務部調查局 | https://www.mjib.gov.tw/news/Index?Module=1 | 200，新聞快報列表。**注意**：`/news` 回 500；`/news/Details/1/1` 雖回200但內容為 NoNews，見文末 |
| 陸委會新聞稿 | https://www.mac.gov.tw/News.aspx?n=05B73310C5C3A632 | **WebFetch 回 403 不可用**，見文末。curl 可通但不作數 |
| 中央社政治 | https://www.cna.com.tw/list/aipl.aspx | 200。通訊社，作為線索 |
| 立法院議事及發言系統 | https://ppg.ly.gov.tw/ppg/ | 200。質詢紀錄與法案進度 |

---

## 關鍵基礎設施與資安（欄位五）

| 來源 | 網址 | 備註 |
|---|---|---|
| 數位發展部資安署 | https://moda.gov.tw/ACS/index | 200 |
| CISA Advisories | https://www.cisa.gov/news-events/cybersecurity-advisories | **WebFetch 回 403 不可用**，見文末。含 IOC 與 TTP |
| 國防安全研究院 | https://indsr.org.tw/ | 200。兼供欄位三與欄位九 |

---

## 經濟脅迫與供應鏈韌性（欄位六）

| 來源 | 網址 | 備註 |
|---|---|---|
| 陸委會新聞稿 | https://www.mac.gov.tw/News.aspx?n=05B73310C5C3A632 | 同欄位四，**WebFetch 回 403 不可用** |
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
| EUvsDisinfo | https://euvsdisinfo.eu/ | 同欄位三，**WebFetch 回 403 不可用** |
| 日本公安調查廳 | https://www.moj.go.jp/psia/ | 200。日文，年報與內外情勢回顧 |
| ASPI | https://www.aspi.org.au/ | 200。澳洲智庫，本欄位澳紐案例的主要途徑 |
| Jamestown China Brief | https://jamestown.org/programs/cb/ | 200。中國對外影響力研究 |
| CSIS | https://www.csis.org/analysis | 200，1187連結。智庫分析，兼供欄位三的中國影響力操作研究 |

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
2. **調查局、中央社政治**——欄位四與六的主力（陸委會不可用）
3. **台灣民主實驗室、IORG**——欄位三，更新頻率低，快速掃過即可
4. **資安署**——欄位五（CISA 不可用，缺口以 WebSearch 補）
5. **移民署、勞動部、內政部**——欄位七，統計類更新以月為單位
6. **公安調查廳、ASPI、CSIS、Jamestown**——欄位八，取一則即可（EUvsDisinfo 不可用）
7. **立法院、全國法規資料庫**——欄位九

---

## 已知失效與限制

- **`www.mjib.gov.tw/news` 回 500**。`/news/Details/1/1` 回200但內容為 NoNews，
  2026-08-22 首次巡檢即撞上，改用 `/news/Index?Module=1` 取得新聞快報列表。
  **此站是「200不等於巡檢成功」的實例**，取回內容後須確認確有條目。
- **`www.mac.gov.tw/` 首頁回 403**，改用 `News.aspx?n=05B73310C5C3A632`。
- **`www.asio.gov.au` 與 `www.canada.ca` 連線失敗**（`000`），見欄位八說明。
- **陸委會、CISA、EUvsDisinfo 三站 WebFetch 回 403**（2026-08-23 複測確認）。
  三站以 curl 均可取得，但晨報用的是 WebFetch，故實際不可用。
  替代：陸委會的政策立場改由中央社政治與立法院質詢取得；CISA 的資安通報
  改由數發部資安署與 WebSearch 取得；EUvsDisinfo 的歐洲案例改由 ASPI
  與 WebSearch 取得。**引用時仍須回溯至原機構文件，取不到就寫入待查核。**
- **國安局 `www.nsb.gov.tw` 為純 JS 站**，全站僅 3.4KB、零個連結，
  WebFetch 只讀得到標題「國家安全局」，`/zh/news` 與 `/zh/publications` 均回 404。
  國安局的公開材料改由立法院議事系統的業務報告與質詢紀錄取得。
- **政府網站多為 JS 載入**，靜態抓取常取不到內文標題。
  母站 SOURCES 已記錄國科會即為此例。取不到標題時記入巡檢摘要，
  **不要因為抓到 200 就當作巡檢成功**。
- **移民署與勞動部的統計以月為單位更新**，多數日子無新數字。
  這不是巡檢失敗，寫巡檢基線即可。

---

## 來源調整紀錄

- 2026-08-22：建站，20 個來源（去重後 17 個網址），逐一實測。
  調查局與陸委會改用替代路徑，澳加官方來源不可用。
- 2026-08-23：新增 CSIS `/analysis`，供欄位三認知作戰與欄位八境外對照。
  **智庫分析屬〔B〕級**，引用時須指明是該機構的評估而非既成事實。
- 2026-08-23：首次巡檢後回填。調查局改用 `/news/Index?Module=1`。
- 2026-08-23（更正）：先前記「陸委會、CISA、EUvsDisinfo 事後重測均回200，
  研判為當下限流」，**該判斷有誤**。以 curl 重測固然回 200，但改用 WebFetch
  複測，三站一致回 403，與首次巡檢當日的情形相同，屬持續性阻擋而非單日限流。
  錯在測試方法用錯工具，已改記為不可用並各給替代途徑。
  **本清單此後一律以 WebFetch 實測。**
- 2026-08-23：國安局改記為不可用（純JS站，零連結）。
  全站 22 個網址以 WebFetch 複測，18 個可用，4 個不可用。
