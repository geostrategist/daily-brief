# 固定巡檢來源

每日晨報開始時，逐一 WebFetch 本清單網址。取得失敗者記錄於當日晨報的巡檢摘要，不靜默略過。

清單以外的資料，透過 WebSearch 補充，但須符合 `EDITORIAL.md` 的來源品質規則。

**本清單的網址皆已實測**，狀態記於備註欄。

**實測一律用 WebFetch，不用 curl。** 晨報產製時用的是 WebFetch，兩者結果會不一致——
國安站於 2026-08-23 發現三站 curl 回 200 但 WebFetch 回 403。
本清單的備註欄若僅記 curl 結果（建站當日多為此），**遇該站取不到內容時
應先以 WebFetch 複測再判定**，不要因為 curl 通就認定站是好的。
已知本站的 The Diplomat、Inquirer、Rappler 即屬 curl 通而 WebFetch 403 者，故未列入。

---

## 通用（全區適用）

| 來源 | 網址 | 備註 |
|---|---|---|
| ACLED | https://acleddata.com/ | 200。武裝衝突事件資料庫，含地理定位與傷亡 |
| ReliefWeb | https://reliefweb.int/updates | 200。UN OCHA，人道情勢與傷亡統計 |
| UN Press | https://press.un.org/en | 200。安理會與大會，決議與表決 |
| ICRC | https://www.icrc.org/en/news | 200。國際紅十字會 |
| AP World | https://apnews.com/hub/world-news | 200。通訊社 |
| Al Jazeera | https://www.aljazeera.com/news/ | 200。非西方視角的對照 |
| Crisis Group | https://www.crisisgroup.org/ | 200。衝突預警與背景分析 |
| SIPRI | https://www.sipri.org/ | 200。軍費與軍備移轉統計 |
| Bellingcat | https://www.bellingcat.com/ | 200。開源情報與影像地理定位 |
| ISW | https://www.understandingwar.org/ | 200。戰場評估，**立場偏美方，須與他源交叉** |

---

## 兩岸與東亞（欄位二、三）

| 來源 | 網址 | 備註 |
|---|---|---|
| 國防部即時軍事動態 | https://www.mnd.gov.tw/news/plaactlist | 200。與國安站共用，本站只在架次結構性變化時引用 |
| 日本防衛省 | https://www.mod.go.jp/j/press/news/index.html | 200。日文，8 月內容曾未載入（母站已記錄） |
| 韓聯社（英文） | https://en.yna.co.kr/ | 200。韓國通訊社 |
| DW 國際 | https://www.dw.com/en/top-stories/s-9097 | 200。歐洲視角，兼供跨區域 |

**38 North 回 403**（朝鮮半島核武分析），WAF 阻擋，改由 WebSearch 取得其公開分析。

---

## 南海（欄位四）

| 來源 | 網址 | 備註 |
|---|---|---|
| AMTI（CSIS 亞洲海事透明倡議） | https://amti.csis.org/ | 200。島礁建設與對峙的衛星影像分析，本欄位主力 |
| Manila Times | https://www.manilatimes.net/news/feed | RSS，50則／次。菲方視角，含仁愛暗沙補給與海警對峙 |

**菲律賓海岸防衛隊 `coastguard.gov.ph` 回 403**。菲方的執法衝突敘事改由 AMTI、
Manila Times 與 WebSearch 取得。

**越南通訊社已於 2026-08-23 移除**。`en.vietnamplus.vn` 回 200 但內容為純 JS 載入，
34KB 之中零個連結、連 title 都是空的，靜態抓取取不到任何條目。改列 Manila Times RSS，
理由是本節需要的是南海爭端內容而非越南國內新聞，實測 Manila Times 當日即有
仁愛暗沙補給與中國海警跟監的條目。越南視角暫由 WebSearch 補充。

---

## 南太平洋（欄位五）

| 來源 | 網址 | 備註 |
|---|---|---|
| RNZ Pacific | https://www.rnz.co.nz/international/pacific-news | 200。紐西蘭公廣，本區報導最穩定者 |
| ABC Pacific | https://www.abc.net.au/pacific | 200。澳洲公廣 |
| BenarNews Pacific | https://www.benarnews.org/english/news/pacific/ | 200 |
| Islands Business | https://islandsbusiness.com/ | 200。斐濟，區域內視角 |
| Lowy Interpreter | https://www.lowyinstitute.org/the-interpreter | 200。澳洲智庫，兼供跨區域 |

**澳洲外交貿易部 `dfat.gov.au` 連線失敗**（`000`，研判為地域封鎖），
官方立場改由 ABC Pacific 與 WebSearch 取得。

---

## 南亞（欄位六）

| 來源 | 網址 | 備註 |
|---|---|---|
| The Hindu 國際 | https://www.thehindu.com/news/international/ | 200。印度視角 |
| Dawn | https://www.dawn.com/ | 200。巴基斯坦視角。**印巴議題須兩者並列** |

---

## 中亞（欄位七）

| 來源 | 網址 | 備註 |
|---|---|---|
| Eurasianet | https://eurasianet.org/ | 200。本區報導最完整者 |
| RFE/RL | https://www.rferl.org/ | 200。美國國會資助，**立場須留意**，與他源交叉 |
| Times of Central Asia | https://timesca.com/ | 200。區域內媒體 |

---

## 跨區域結構（欄位八）

| 來源 | 網址 | 備註 |
|---|---|---|
| OFAC Recent Actions | https://ofac.treasury.gov/recent-actions | 200。制裁清單異動，原始公告 |
| BIS | https://www.bis.doc.gov/ | 200。出口管制與實體清單 |
| 美國務院新聞稿 | https://www.state.gov/press-releases/ | 200 |
| EEAS（歐盟對外事務部） | https://www.eeas.europa.eu/ | 200 |
| Defense News | https://www.defensenews.com/ | 200。軍售與軍援，母站已驗證 |
| Breaking Defense | https://breakingdefense.com/ | 200。預算與合約，母站已驗證 |
| IISS | https://www.iiss.org/ | 200但為JS載入，靜態僅取得1個連結，見文末。軍力平衡 |
| CSIS | https://www.csis.org/analysis | 200，1187連結。智庫分析，涵蓋中國、印太安全、國防工業 |

**DSCA 全站回 403**（`dsca.mil`、`/press-media/major-arms-sales`、`/rss.xml` 皆是，
WebFetch 與 curl 結果一致）。美國對外軍售通知改由 Defense News 與 Breaking Defense 取得，
**引用時須回溯至 DSCA 原始通知編號**，取不到就於該則「待查核」寫明。

**歐盟官方公報 EUR-Lex 回 502**（建站當日），可能為暫時性，首次巡檢時重試。

**IISS 為 JS 站**。回 200 但 123KB 之中僅 1 個連結，靜態抓取取不到內文，
`/online-analysis/` 另回 403。此站列為背景參考，**取不到內文屬預期，不必每日記為失敗**，
需要其資料時改以 WebSearch 或直接引用其出版品。

**CSIS 於 2026-08-23 加入**。首頁與 `/analysis` 均可靜態抓取，後者條目最多故列後者。
注意本清單的 AMTI 即為 CSIS 旗下計畫，兩者不重複列計——AMTI 專供南海欄位的島礁與對峙分析，
CSIS 母站供其餘欄位的中國軍力、國防工業與印太安全分析。
**智庫分析屬〔B〕級**，其判斷不等同一手文件，引用時須指明是該機構的評估而非既成事實。

---

## 巡檢順序建議

1. **ACLED 與 ReliefWeb**——一次可得多區的事件線索，先取
2. **AP World、Al Jazeera、DW**——當日全球概況
3. **國防部、防衛省、韓聯社**——欄位二與三
4. **AMTI、Manila Times**——欄位四
5. **RNZ Pacific、ABC Pacific**——欄位五，訊號密度低，快速掃過
6. **The Hindu、Dawn**——欄位六，印巴議題並列兩者
7. **Eurasianet、RFE/RL**——欄位七，訊號密度低
8. **OFAC、BIS、Defense News、CSIS**——欄位八

---

## 已知失效與限制

- **DSCA 全站 403**，見欄位八說明。
- **38 North 403**、**菲律賓海岸防衛隊 403**、**澳洲 DFAT 連線失敗**，各見所屬欄位說明。
- **EUR-Lex 502**，建站當日狀態，首次巡檢時重試。
- **Reuters 回 401**，需訂閱，不列入清單。通訊社以 AP 為主。
- **ISW 與 RFE/RL 有明確立場**，前者偏美方戰場評估，後者為美國國會資助。
  兩者可用作線索與背景，**不得作為單一來源支撐傷亡數字或戰線位置**。
- **南太平洋與中亞的來源最不穩定**，部分僅有 HTML 列表頁且改版頻繁。
  若某區當日可用來源少於兩個，該區改以 WebSearch 為主，並於巡檢摘要註明。

---

## 來源調整紀錄

- 2026-08-22：建站，31 個來源（去重後 30 個網址），逐一實測。
  DSCA、38 North、菲海防、澳 DFAT 不可用，各有替代途徑。
- 2026-08-23：全站 33 個網址逐一複測。30 個正常，2 個為純 JS 站。
  越南通訊社移除改列 Manila Times RSS，IISS 保留但註明為 JS 站不計失敗。
  另更正一則：Breaking Defense 一度被自動偵測誤判為失效，複測回 173KB、206 連結，站正常。
- 2026-08-23：加入 CSIS `/analysis`（智庫分析，涵蓋中國、印太安全、國防工業）。
