# 固定巡檢來源

每日晨報開始時，逐一 WebFetch 本清單網址。取得失敗者記錄於當日晨報的巡檢摘要，不靜默略過。

清單以外的資料，透過 WebSearch 補充，但須符合 `EDITORIAL.md` 的來源品質規則。

---

## 兩岸

| 來源 | 網址 | 備註 |
|---|---|---|
| 中央社兩岸 | https://www.cna.com.tw/list/acn.aspx | 通訊社，第一手 |
| 陸委會新聞稿 | https://www.mac.gov.tw/News.aspx?n=05B73310C5C3A632 | 官方 |
| 國防部即時軍事動態 | https://www.mnd.gov.tw/PublishTable.aspx?types=%e5%8d%b3%e6%99%82%e8%bb%8d%e4%ba%8b%e5%8b%95%e6%85%8b&Title=%e5%9c%8b%e9%98%b2%e6%b6%88%e6%81%af | 軍機艦架次原始數據 |
| 國台辦 | http://www.gwytb.gov.cn/xwdt/xwfb/ | 對岸官方口徑 |

## 東南亞

| 來源 | 網址 | 備註 |
|---|---|---|
| The Diplomat 東南亞 | https://thediplomat.com/category/southeast-asia/ | 分析 |
| Nikkei Asia | https://asia.nikkei.com/ | 產業與供應鏈 |
| 菲律賓海岸防衛隊 | https://coastguard.gov.ph/index.php/11-news | 南海執法一手 |
| ASEAN 官方 | https://asean.org/news/ | 機制文件 |

## 日本

| 來源 | 網址 | 備註 |
|---|---|---|
| 防衛省報道発表 | https://www.mod.go.jp/j/press/news/index.html | 官方 |
| 外務省 | https://www.mofa.go.jp/mofaj/press/release/index.html | 官方 |
| NHK 政治 | https://www3.nhk.or.jp/news/cat04.html | 即時 |
| 日經 | https://www.nikkei.com/ | 經濟安保 |

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
| 歐盟 AI Act 官方 | https://artificialintelligence-act.eu/ | 法規原文 |
| NIST AI | https://www.nist.gov/artificial-intelligence | 標準 |
| 國科會 | https://www.nstc.gov.tw/folksonomy/list/c7cf9f5f-e1b3-4d1c-8e0b-9d2f0a1a0a1a | 台灣 AI 政策 |
| Stanford HAI | https://hai.stanford.edu/news | 評測與研究 |

## 財稅與會計

| 來源 | 網址 | 備註 |
|---|---|---|
| 財政部新聞稿 | https://www.mof.gov.tw/singlehtml/285 | 函釋與修法 |
| 全國法規資料庫 | https://law.moj.gov.tw/ | 條文原文 |
| 金管會 | https://www.fsc.gov.tw/ch/home.jsp?id=96&parentpath=0,2 | 財報揭露 |
| OECD 稅務 | https://www.oecd.org/tax/ | BEPS |
| 會計研究發展基金會 | https://www.ardf.org.tw/ | 公報 |

---

## 選用模組：World Monitor（預設關閉）

免費層僅提供發現層資料，實際事件資料需訂閱。目前僅在需要交叉查核外電覆蓋時使用。

- 免費工具：`get_sources`（10 次/分，無每日額度）
- 端點：`POST https://worldmonitor.app/mcp`
- 須帶描述性 User-Agent，否則於邊緣被過濾
- 台灣籍來源僅 4 個、日本 6 個，覆蓋密度低於本清單直接巡檢，故不作主線

啟用方式：將本節標題的「預設關閉」改為「啟用」，並於當日晨報註明資料來源。

---

## 來源調整紀錄

- 2026-08-18：建立初始清單，共 26 個固定巡檢網址。
