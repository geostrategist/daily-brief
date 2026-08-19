# 固定巡檢來源 · 核能晨報

每日晨報開始時，逐一 WebFetch 本清單網址。取得失敗者記錄於當日晨報的巡檢摘要，不靜默略過。

清單以外的資料，透過 WebSearch 補充，但須符合 `EDITORIAL.md` 的來源品質規則。

**本清單於 2026-08-19 逐一實測**，每列的「實測」欄記錄當時的 HTTP 狀態與可用性。
未通過實測者不列入主線，改列文末「已知不可用」。

---

## 台灣核能爭議

| 來源 | 網址 | 實測 | 備註 |
|---|---|---|---|
| 核能安全委員會 · 焦點新聞 | https://www.nusc.gov.tw/news/headline.html | 200，當日內容 | 主管機關。含機組狀態、防汛與檢查要求 |
| 台電 · 各機組發電量 JSON | https://service.taipower.com.tw/data/opendata/apply/file/d006001/001.json | 200，含當日時戳 | **機組狀態的唯一可靠來源**。見下方說明 |
| 立法院議事及發言系統 | https://ppg.ly.gov.tw/ppg/ | 200 | 核管法等法案進度 |

核安會的 RSS（`/rss/news.xml`）回 404，請直接解析 HTML 列表頁。

**台電機組狀態的正確用法**（2026-08-19 確認）：原先列入的
`taipower.com.tw/2289/2404/2405/nuclear/` 回 200 但內容僅為網站導覽選單、無任何機組資料，
已於創刊日移除。改用台電開放資料的各機組發電量 JSON：

```bash
curl -s "https://service.taipower.com.tw/data/opendata/apply/file/d006001/001.json"
```

回傳為 `{"DateTime": "...", "aaData": [...]}`，每列欄位為機組類型、機組名稱、裝置容量(MW)、
淨發電量(MW)、淨發電量/裝置容量比(%)、備註，約 214 列，`DateTime` 為十分鐘級的更新時戳。

判讀要點：**`機組類型` 欄若無「核能」分類，即表示三座核電廠均未併網發電。**
此時清單中僅會出現「核二Gas1」「核三Gas1」等列，那是各廠的氣渦輪機（機組類型為「燃料油」），
**不是反應器**，不得據以宣稱機組運轉中。2026-08-19 18:50 之資料即為此狀態。
反之，若出現機組類型為「核能」之列，則其淨發電量即為該機組之實際出力。

## 全球核電與 SMR

| 來源 | 網址 | 實測 | 備註 |
|---|---|---|---|
| World Nuclear News · RSS | https://www.world-nuclear-news.org/rss | 200，40 則含 2026 日期 | **本站主力來源**。逐筆含標題、連結、pubDate（GMT） |
| World Nuclear News · 首頁 | https://www.world-nuclear-news.org/ | 200 | RSS 未涵蓋時的補充 |
| IAEA News | https://www.iaea.org/news | 200，含 2026 內容 | 官方。RSS（`/feeds/topnews.rss`）回 404，用 HTML |
| IAEA PRIS | https://pris.iaea.org/pris/ | 200 | 機組狀態資料庫。查特定機組時進入，非每日巡檢 |
| ANS Nuclear Newswire | https://www.ans.org/news/ | 200，2026 內容密集 | 美國核能學會，具署名產業媒體 |

**WNN RSS 為本站抓取最穩定者**，pubDate 為 GMT，換算台灣時間加 8 小時。

## 日本核電重啟

| 來源 | 網址 | 實測 | 備註 |
|---|---|---|---|
| 原子力産業新聞（JAIF） | https://www.jaif.or.jp/journal/news/ | 200，2026 內容密集 | 日本原子力産業協會 |

JAIF 的 RSS（`https://www.jaif.or.jp/feed`）回 200 但無 `<item>` 條目，不可用；請直接解析 HTML 列表頁。
原子力規制委員會（nra.go.jp）與東京電力之公告頁尚未納入固定清單，需要時以 WebSearch 補，
取得原文連結後再引用。

## 歐洲核能

| 來源 | 網址 | 實測 | 備註 |
|---|---|---|---|
| ONR（英國核能管制辦公室） | https://www.onr.org.uk/news/ | 200，含 2026 | 官方。`/news-and-events/news/` 路徑回 404，用 `/news/` |
| ASNR（法國核安與輻防局） | https://www.asnr.fr/ | 200，含 2026 | 官方。內頁 `/l-asnr-en-action/actualites` 回 404，用首頁進入 |
| nucleareurope | https://www.nucleareurope.eu/news/ | 200，含 2026 | 歐洲核能產業協會。屬產業立場方，依編輯規範第三節，其倡議性宣稱不單獨採用 |
| EDF 新聞稿（英文） | https://www.edf.fr/en/the-edf-group/dedicated-sections/journalists/all-press-releases | 200 | 公司官方 |

ENSREG（`ensreg.eu/news`）回 404，已排除。

## 南韓核能

| 來源 | 網址 | 實測 | 備註 |
|---|---|---|---|
| 韓聯社 Yonhap（英文） | https://en.yna.co.kr/ | 200，2026 內容密集 | 通訊社 |
| Korea Herald | https://www.koreaherald.com/ | 200，2026 內容密集 | 韓媒，具署名 |

KHNP 英文站（`khnp.co.kr/eng/`）與 NSSC 英文站回 200 但內容僅 1.7KB 之 JS 外殼，靜態抓取取不到條目，
已排除；南韓官方動態經韓聯社與 Korea Herald 取得，並依規範標示來源等級。

## 美國核安與核子保安

| 來源 | 網址 | 實測 | 備註 |
|---|---|---|---|
| ANS Nuclear Newswire | https://www.ans.org/news/ | 200 | 兼作本主題主力 |
| energy.gov 新聞室 | https://www.energy.gov/newsroom | 200，含 2026 | DOE 官方。`/ne/articles` 與 `/ne/listings/ne-news` 皆回 404 |
| NEI（美國核能研究所） | https://www.nei.org/news | 200，含 2026 | 產業協會，屬立場方，同 nucleareurope 之限制 |

**NRC（nrc.gov）全站對本系統回 403**，`/reading-rm/doc-collections/news/`、`/pmns/pressreleases`、
事件報告頁與 RSS 皆然，curl 與 WebFetch 兩種抓取方式一致失敗。NRC 之許可、裁罰與事件報告
一律經 ANS Newswire 等第三方取得，**不得標 A 級**，並於待查核欄註明「本報未取得 NRC 原文」。

## 核燃料與產業鏈

| 來源 | 網址 | 實測 | 備註 |
|---|---|---|---|
| NucNet | https://www.nucnet.org/ | 200，2026 內容密集 | 獨立核能新聞通訊社，部分內容需訂閱，取得摘要即註明 |
| UxC | https://www.uxc.com/ | 200 | 鈾價指標。現貨價於首頁揭露，長約價需訂閱 |
| Cameco 新聞 | https://www.cameco.com/media/news | 200，含 2026 | 全球最大鈾生產商之一，公司重訊與產量指引 |

Nuclear Engineering International（`neimagazine.com`）回 403，已排除。
Reuters 能源版回 401（付費牆），已排除。

---

## 巡檢順序建議

清單共 **18 個**固定網址。建議順序為：先抓 WNN RSS（一次取得 40 則、涵蓋主題二至七的多數線索），
再抓核安會與 JAIF（台日兩地官方），其餘依主題順序補齊。

WNN RSS 只當線索，看到值得寫的條目仍須點進原文確認，並引用最原始的出處
（管制機關文件優於 WNN 報導，WNN 報導優於二手轉載）。

---

## 來源調整紀錄

- 2026-08-19：建立初始清單，共 18 個固定巡檢網址，逐一實測。
- 2026-08-19（創刊日修正）：台電「核能發電」頁實際回傳僅為導覽選單，無機組資料，
  已改為台電開放資料之各機組發電量 JSON，並載明「無核能分類即代表未併網」之判讀規則。
  排除 NRC（403）、Nuclear Engineering International（403）、Reuters（401）、
  ENSREG（404）、KHNP 與 NSSC 英文站（JS 外殼）、核安會 RSS（404）、IAEA RSS（404）、
  JAIF RSS（無條目）。
