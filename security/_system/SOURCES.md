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
| IORG | https://iorg.tw/ | 可用。資訊操作研究，具資料集 |
| ASPI | https://www.aspi.org.au/ | 可用。中國影響力操作研究，兼供欄位八 |
| CSIS | https://www.csis.org/analysis | 可用。智庫分析，兼供欄位八 |
| EUvsDisinfo | https://euvsdisinfo.eu/ | **WebFetch 回 403 不可用**，見文末 |

**台灣民主實驗室與國安局已於 2026-08-23 移除**。國安局為純JS站本就取不到內容
（全站3.4KB、零連結）。台灣民主實驗室則抓得到，移除屬編輯判斷而非技術問題。
本欄位的歸因來源因而以 IORG、ASPI、CSIS 為主，**三者皆為研究機構**，
其歸因依 `EDITORIAL.md` 第四節仍須交代方法與信心程度，不因機構聲譽而免除。

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
| 數位發展部資安署 | https://moda.gov.tw/ACS/index | 可用。台灣主管機關 |
| The Record | https://therecord.media/ | 可用。資安專業媒體，含關鍵基礎設施攻擊、勒索軟體、國家級行動 |
| Federal News Network · 關鍵基礎設施 | https://federalnewsnetwork.com/tag/critical-infrastructure/ | 可用。美國聯邦資安政策與CISA動態 |
| 國防安全研究院 | https://indsr.org.tw/ | 可用。兼供欄位三與欄位九 |
| CISA | https://www.cisa.gov/ | **WebFetch 回 403 不可用**（全站含 RSS），見文末 |
| 美國國土安全部 DHS | https://www.dhs.gov/group/all/newsroom | **WebFetch 回 403 不可用**（全站），見文末 |

---

## 經濟脅迫與供應鏈韌性（欄位六）

| 來源 | 網址 | 備註 |
|---|---|---|
| 中央社財經 | https://www.cna.com.tw/list/aie.aspx | 可用。母站已驗證 |
| ASPI | https://www.aspi.org.au/ | 可用。維有脅迫性外交資料庫，本節的個案計數來源 |
| CSIS | https://www.csis.org/analysis | 可用。出口管制與供應鏈槓桿分析 |
| 陸委會新聞稿 | https://www.mac.gov.tw/News.aspx?n=05B73310C5C3A632 | 同欄位四，**WebFetch 回 403 不可用** |

**本節在陸委會不可用後只剩中央社一個固定來源**，故補列 ASPI 與 CSIS。
兩者為研究機構而非官方，**其個案計數與判斷屬〔B〕級**，
涉及台灣的貿易措施仍須回查官方公告或企業重訊，取不到就寫入待查核。

---

## 移民、人流與邊境管理（欄位七）

| 來源 | 網址 | 備註 |
|---|---|---|
| 內政部 | https://www.moi.gov.tw/ | 可用。函釋與修法 |
| The Record | https://therecord.media/ | 可用。兼供本節的邊境生物辨識與資料庫議題 |

**移民署與勞動部勞動力發展署已於 2026-08-23 移除**。兩站 WebFetch 均可取得，
移除的理由不是抓不到而是產出不合本節所需——實測當日移民署首頁為「新住民尋親」
一類的宣導性新聞，勞動部為「產業新尖兵計畫」一類的職訓推廣，
均非本節要的人數、國籍別與年度比較。
**兩署的統計月報仍是本節的優先訊號**，需要時以 WebSearch 直接指向其統計專頁，
不再每日巡檢其首頁。

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
3. **IORG、ASPI、CSIS**——欄位三，更新頻率低，快速掃過即可
4. **資安署、The Record、Federal News Network**——欄位五（CISA 與 DHS 不可用，由此二媒體替代）
5. **內政部**——欄位七（移民署與勞動部已移除，統計改以 WebSearch 指向其統計專頁）
6. **公安調查廳、ASPI、CSIS、Jamestown**——欄位八，取一則即可（EUvsDisinfo 不可用）
7. **立法院、全國法規資料庫**——欄位九

---

## 已知失效與限制

- **`www.mjib.gov.tw/news` 回 500**。`/news/Details/1/1` 回200但內容為 NoNews，
  2026-08-22 首次巡檢即撞上，改用 `/news/Index?Module=1` 取得新聞快報列表。
  **此站是「200不等於巡檢成功」的實例**，取回內容後須確認確有條目。
- **`www.mac.gov.tw/` 首頁回 403**，改用 `News.aspx?n=05B73310C5C3A632`。
- **`www.asio.gov.au` 與 `www.canada.ca` 連線失敗**（`000`），見欄位八說明。
- **美國 DHS 與 CISA 全站 WebFetch 回 403**（2026-08-23 實測）。
  兩站的首頁、新聞頁與 CISA 的 advisories RSS（`/cybersecurity-advisories/all.xml`）
  一律回 403，非單一路徑問題。**兩者的產出改由 The Record 與 Federal News Network
  取得**，此二站均大量報導 CISA 通報與 DHS 政策，實測當日即有
  「NSA、FBI 警告駭客以AI生成工具攻擊關鍵基礎設施」與
  「CISA 人力削減影響」等條目。**引用時須回溯至 CISA 或 DHS 原始編號**，
  取不到就於該則「待查核」寫明。
- **陸委會、CISA、EUvsDisinfo 三站 WebFetch 回 403**（2026-08-23 複測確認）。
  三站以 curl 均可取得，但晨報用的是 WebFetch，故實際不可用。
  替代：陸委會的政策立場改由中央社政治與立法院質詢取得；CISA 的資安通報
  改由數發部資安署與 WebSearch 取得；EUvsDisinfo 的歐洲案例改由 ASPI
  與 WebSearch 取得。**引用時仍須回溯至原機構文件，取不到就寫入待查核。**
- **國安局 `www.nsb.gov.tw` 已自清單移除**。該站為純 JS 站，全站僅 3.4KB、
  零個連結，WebFetch 只讀得到標題「國家安全局」，`/zh/news` 與 `/zh/publications`
  均回 404。國安局的公開材料改由立法院議事系統的業務報告與質詢紀錄取得。
  **此處保留紀錄，是為了讓日後有人想加時看得到已經試過且失敗。**
- **政府網站多為 JS 載入**，靜態抓取常取不到內文標題。
  母站 SOURCES 已記錄國科會即為此例。取不到標題時記入巡檢摘要，
  **不要因為抓到 200 就當作巡檢成功**。
- **移民與勞動統計以月為單位更新**，多數日子無新數字。
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
- 2026-08-23：欄位五新增 The Record 與 Federal News Network，
  兩站均以 WebFetch 實測可用且當日即有關鍵基礎設施條目。
  同時列入 CISA 與 DHS 並記為不可用，理由見文末——列而不刪是為了讓
  日後有人想加時看得到已經試過且失敗，不必再試一次。
- 2026-08-23：欄位七移除移民署與勞動部勞動力發展署。兩站抓得到，
  但其首頁產出為宣導與職訓推廣，非本節所需的統計。統計改以 WebSearch
  直接指向統計專頁。欄位七另加 The Record 供邊境生物辨識與資料庫議題。
- 2026-08-23：欄位六補列 ASPI 與 CSIS。陸委會不可用後該節只剩中央社一個來源，
  低於每節至少兩個的門檻。
- 2026-08-23：欄位三移除台灣民主實驗室與國安局。國安局為純JS站本就不可用，
  台灣民主實驗室抓得到，移除屬編輯判斷。欄位三的歸因來源改以
  IORG、ASPI、CSIS 為主。
