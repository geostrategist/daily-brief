# 固定巡檢來源

每日晨報開始時，逐一 WebFetch 本清單網址。取得失敗者記錄於當日晨報的巡檢摘要，不靜默略過。

清單以外的資料，透過 WebSearch 補充，但須符合 `EDITORIAL.md` 的來源品質規則。

**實測一律用 WebFetch，不用 curl。** 晨報產製時用的是 WebFetch，兩者結果會不一致。
**且不能只看 HTTP 碼**——本清單於 2026-08-23 複測時發現 Japan Times 回 200 卻是
2023至2025年的舊快取，GMA News RSS 回 200 但停滯兩週。回 200 而內容過期，
比直接失敗更危險，因為它會安靜地把舊聞當新聞餵進晨報。

---

## 國際企業

**RSS 為本主題的主力來源**。三支皆為 XML，逐筆含標題、連結與 GMT 發布時間，抓取穩定，不受 WAF 阻擋。

| 來源 | 網址 | 備註 |
|---|---|---|
| Yahoo 股市 · 財經新聞 | https://tw.stock.yahoo.com/rss?category=news | RSS，50 則／次 |
| Yahoo 股市 · 台股 | https://tw.stock.yahoo.com/rss?category=tw-market | RSS，50 則／次 |
| Yahoo 股市 · 國際市場 | https://tw.stock.yahoo.com/rss?category=intl-markets | RSS，50 則／次 |
| 中央社財經 | https://www.cna.com.tw/list/aie.aspx | 通訊社 |
| Nikkei Asia | https://asia.nikkei.com/ | 產業與供應鏈 |
| 國防部即時軍事動態 | https://www.mnd.gov.tw/news/plaactlist | 軍機艦架次原始數據 |

**RSS 使用注意**：Yahoo 的 RSS 是**聚合**，實際內容出自各家媒體（經濟日報、工商時報、中央社、鉅亨網等）。三點必須遵守：

1. **RSS 只當線索，不當來源**。看到值得寫的條目，點進原文確認後，**引用原始媒體與其網址**，不引用 Yahoo 的轉載頁。
2. **署名要查**。Yahoo 聚合中夾雜投顧、名嘴與內容農場（標題出現「揭黃金買點」「曝多空生死」這類），依 `EDITORIAL.md` 第三節一律排除。
3. **pubDate 為 GMT**，換算台灣時間需加 8 小時。

## 東南亞

| 來源 | 網址 | 備註 |
|---|---|---|
| Inquirer | https://www.inquirer.net/ | 可用。菲媒，含國政與商業。2026-08-23 換入，取代停滯的 GMA |
| Philstar | https://www.philstar.com/rss/nation | RSS |
| Manila Times | https://www.manilatimes.net/news/feed | RSS，50 則／次 |
| Yahoo 股市 · 國際市場 | https://tw.stock.yahoo.com/rss?category=intl-markets | RSS，兼收區域財經 |

原 The Diplomat、ASEAN 官方、菲律賓海岸防衛隊三站因 WAF 阻擋（403／307）於 2026-08-18 移除。

## 日／韓

本主題每日只寫一則，取日韓兩國當日最重要的國際新聞或經貿動態。

| 來源 | 網址 | 備註 |
|---|---|---|
| Nikkei Asia · Politics | https://asia.nikkei.com/Politics | 可用，當日條目。2026-08-23 換入，取代已死的 Japan Times feed |
| 共同通信 | https://english.kyodonews.net/ | **WebFetch 主機層阻擋不可用**，見文末 |
| Nikkei Asia | https://asia.nikkei.com/ | 日本經貿與供應鏈 |
| 韓聯社 Yonhap（英文） | https://en.yna.co.kr/ | **WebFetch 主機層阻擋不可用**，見文末 |
| Korea Herald | https://www.koreaherald.com/ | 韓媒，具署名 |
| 防衛省報道発表 | https://www.mod.go.jp/j/press/news/index.html | 可用但更新稀疏，最新為 8/7。屬該站發布頻率低，非抓取失敗 |

原外務省（403）與 NHK 政治（工具層阻擋）於 2026-08-18 移除。同日新增韓國兩個來源。

## 無人載具

| 來源 | 網址 | 備註 |
|---|---|---|
| The War Zone | https://www.twz.com/ | 技術細節 |
| DefenseScoop | https://defensescoop.com/ | 美軍採購 |
| Breaking Defense | https://breakingdefense.com/ | 預算與合約 |
| Defense News 海軍 | https://www.defensenews.com/naval/ | 無人艦艇 |
| 立法院議事及發言系統 | https://ppg.ly.gov.tw/ppg/ | 無人載具條例進度 |

## 人工智慧

| 來源 | 網址 | 備註 |
|---|---|---|
| 歐盟數位政策（AI Act） | https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai | 歐盟官方，取代已失效之 artificialintelligence-act.eu |
| NIST AI | https://www.nist.gov/artificial-intelligence | 標準 |
| 國科會 | https://www.nstc.gov.tw/ | **JS 載入取不到日期**，僅作進入點，見文末 |
| Stanford HAI | https://hai.stanford.edu/news | 評測與研究 |
| CSIS | https://www.csis.org/analysis | 200，1187連結。智庫分析，涵蓋出口管制、關鍵技術與國防工業 |

## 財稅與會計

| 來源 | 網址 | 備註 |
|---|---|---|
| 財政部新聞稿 | https://www.mof.gov.tw/singlehtml/285 | 函釋與修法 |
| 全國法規資料庫 | https://law.moj.gov.tw/ | 條文原文 |
| 金管會 | https://www.fsc.gov.tw/ch/home.jsp?id=96&parentpath=0,2 | 財報揭露 |
| International Tax Review | https://www.internationaltaxreview.com/ | 可用，當日條目。國際稅改、Pillar Two、移轉訂價。2026-08-23 換入，取代需登入的 EY |
| 會計研究發展基金會 | https://www.ardf.org.tw/ | 公報 |

## 選用模組：World Monitor（預設關閉）

免費層僅提供發現層資料，實際事件資料需訂閱。目前僅在需要交叉查核外電覆蓋時使用。

- 免費工具：`get_sources`（10 次/分，無每日額度）
- 端點：`POST https://worldmonitor.app/mcp`
- 須帶描述性 User-Agent，否則於邊緣被過濾
- 台灣籍來源僅 4 個、日本 6 個，覆蓋密度低於本清單直接巡檢，故不作主線

啟用方式：將本節標題的「預設關閉」改為「啟用」，並於當日晨報註明資料來源。

---

## 已知失效與限制

以下為 2026-08-23 以 WebFetch 逐一複測 29 個網址的結果，18 個可用、11 個有問題。

**主機層阻擋（2 個）**：共同通信 `english.kyodonews.net`、韓聯社 `en.yna.co.kr`。
WebFetch 回主機拒絕而非數字狀態碼，連日一致，非暫時性。
日韓動態改由 Nikkei Asia、Korea Herald 與中央社支撐。

**回 200 但內容過期或無內容（4 個）**：

- **Japan Times feed 已死**，回 200 但內容為 2023 至 2025 年舊快取，
  **這是最危險的一種失效**，因為它會安靜地把三年前的新聞當新聞餵進晨報。已移除。
- **GMA News RSS 停滯**，回 200 但最新條目停在 8/8，已換為 Inquirer。
- **EY Tax News 為登入牆**，回 200 但內容是會員驗證頁與服務條款，
  已換為 International Tax Review。
- **國科會與立法院議事系統為 JS 載入**，回 200 但取不到日期與條目。
  兩者僅作進入點，需要其內容時以 WebSearch 指向具體頁面。

**可用但更新稀疏（3 個）**：防衛省報道発表（最新 8/7）、
歐盟 AI Act 官網（最新新聞稿 7/31）、NIST AI（僅月份層級日期）。
三者屬該站發布頻率低，**不是抓取失敗，不必每日記為失敗**。

**日期精度不足（2 個）**：Defense News 海軍版僅顯示相對時間（「2 天前」），
NIST 僅到月份。引用時須點進個別文章確認日期。

---

## 來源調整紀錄

- 2026-08-18：建立初始清單，共 26 個固定巡檢網址。
- 2026-08-18：新增核能產業四個來源（核安會、JAIF、World Nuclear News、IAEA）。
- 2026-08-23：核能產業四個來源整節移除，該主題已交由子站 `nuclear/`。
- 2026-08-23：全站 29 個網址以 WebFetch 逐一複測，結果見「已知失效與限制」。
  換掉三個：Japan Times（feed 為 2023-2025 舊快取）改 Nikkei Asia Politics、
  GMA News（停滯兩週）改 Inquirer、EY Tax News（登入牆）改 International Tax Review。
  共同通信與韓聯社改記為主機層阻擋不可用。
- 2026-08-23：新增 CSIS `/analysis`，供主題一的出口管制與供應鏈、主題五的AI治理與國防科技。
  **智庫分析屬〔B〕級**，引用時須指明是該機構的評估而非既成事實。
- 2026-08-18：主題一由「兩岸」改為「國際企業」，改以 Yahoo 股市三支 RSS 為主力。移除九個長期失效來源：陸委會（403）、國台辦（編碼損毀）、外務省（403）、NHK 政治（工具層阻擋）、The Diplomat 東南亞（403）、ASEAN 官方（307）、菲律賓海岸防衛隊（403）、OECD 稅務（403）、歐盟 AI Act 站（網域不存在且原非官方站）。各以可抓取的具署名替代來源補上。
