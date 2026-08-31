# 期刊晨報 · Journals Daily Brief

每週一巡檢 49 種學術期刊的新登錄文章，分六個研究領域，**每則說明為什麼值得讀**。

網站：https://geostrategist.github.io/daily-brief/journals/

---

## 這是什麼

其餘四站問「今天發生什麼事」，本站問**「今天有什麼值得讀的新研究」**。

讀者是要寫論文與評論的人。因此取捨與新聞站相反：
**寧可少寫幾則而每則說清楚用途，不求覆蓋當日全部新刊。**

## 為什麼用 Crossref 而非各出版社 RSS

各出版社的 RSS 路徑散亂且常改版，實測 MIT Press 與 Oxford 的 feed 回 404、
Cambridge 回 204 空內容，出版社站本身多有 WAF（`direct.mit.edu`、`academic.oup.com` 回 403）。

Crossref 是各出版社共同上繳 metadata 的權威登錄機構，**一支 API 打完所有出版社**，
且支援 `from-created-date` 增量查詢。代價是只有書目沒有全文，
**摘要僅約三分之一的條目有**，故 `EDITORIAL.md` 第三節專門處理「摘要不可得時怎麼辦」。

## 資料流

```
週一 01:00  run-local.ps1
         ├─ fetch.py          49 次 Crossref 查詢 → _drafts/crossref_YYYYMMDD.json
         └─ claude -p         讀該 json，選稿與撰寫 → _drafts/Brief_YYYYMMDD.md
（停在這裡，不 commit、不 push）

人工過目後
       python journals/_system/publish.py YYYYMMDD
```

**抓取交給程式，判斷交給 agent。** 49 次網路查詢不該由 agent 逐一 WebFetch，
它的工作是選稿與說明用途。

## 目錄結構

```
index.html              單檔前端，Service Worker 快取名稱與母站分離
briefs/                 已發布晨報與日期索引
_drafts/                草稿與 crossref json。已 gitignore
_system/
  JOURNALS.md           49 種期刊與 ISSN — 增刪期刊只改這裡
  TOPICS.md             九個欄位、各領域優先與排除、每節則數上限
  EDITORIAL.md          編輯規範 — 決定怎麼寫
  DAILY_PROMPT.md       執行指令原文
  LOCAL_OVERRIDE.md     本機執行的覆寫規則
  fetch.py              Crossref 查詢，產出 json
  run-local.ps1         本機週一 01:00 排程，先跑 fetch.py 再叫 agent
  publish.py            過目後發布
  rebuild-manifest.py   依 briefs/ 重建索引
  style_check.py        文體檢查
  .last-run             上次執行日期，供增量查詢。已 gitignore
```

## 新增期刊

只改 `JOURNALS.md`，但**新增前必須先實測 ISSN**：

```bash
curl -s "https://api.crossref.org/journals/<ISSN>/works?rows=1&select=container-title" \
     -H "User-Agent: daily-brief/1.0 (mailto:geostrategist@gmail.com)" | python -m json.tool
```

`container-title` 須與期刊名相符、`total-results` 須大於零。
**ISSN 錯了不會報錯，只會永遠查不到新文章**，看起來像「今日無新刊」。

## 手動執行

```bash
python journals/_system/fetch.py --days 7      # 只抓資料
python journals/_system/fetch.py --list        # 列出期刊清單
powershell -ExecutionPolicy Bypass -File journals\_system\run-local.ps1
```

## 五站分工

| 站 | 排程 | 問的問題 |
|---|---|---|
| **期刊晨報 `journals/`（本站）** | **週一 01:00** | **今天有什麼值得讀的新研究** |
| 核能晨報 `nuclear/` | 週二 02:00 | 核能的安全、保安、保防 |
| 國家安全晨報 `security/` | 週一至四 03:00 | 台灣內部的韌性哪裡破了 |
| 國際衝突晨報 `conflict/` | 週二、四 04:00 | 國家之間正在如何對抗 |
| 實踐國企晨報（母站） | 週一三五 04:00 | 國際商業與政策環境怎麼變 |

**與其他四站的界線**：其他四站寫事件，本站寫研究。
同一議題若既有新聞又有新論文，新聞歸該站、論文歸本站。

**免責**：本報彙整公開書目資訊，非投資或決策建議。

---

實踐大學高雄校區 國際企業管理學系
