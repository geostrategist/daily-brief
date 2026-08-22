# 期刊清單

本檔為每日巡檢的期刊來源。**新增或移除期刊只改本檔**，不需更動程式碼。

`fetch.py` 解析本檔的表格，逐一以 ISSN 查 Crossref API。
ISSN 錯了不會報錯，只會永遠查不到新文章，看起來像「今日無新刊」，
所以**新增期刊前必須先實測**：

```bash
curl -s "https://api.crossref.org/journals/<ISSN>/works?rows=1&select=container-title" \
     -H "User-Agent: daily-brief/1.0 (mailto:geostrategist@gmail.com)" | python -m json.tool
```

回傳的 `container-title` 須與期刊名相符、`total-results` 須大於零。

---

## 為什麼用 Crossref 而非各出版社的 RSS

各出版社的 RSS 路徑散亂且常改版，MIT Press、Oxford 的 feed 實測回 404，
Cambridge 回 204 空內容，出版社站本身多有 WAF（`direct.mit.edu` 與 `academic.oup.com` 回 403）。
Crossref 是各出版社共同上繳 metadata 的權威登錄機構，一支 API 打完所有出版社，
且支援 `from-created-date` 增量查詢，正合每日巡檢所需。

**代價**：Crossref 只有書目 metadata，沒有全文與摘要。
摘要欄位（`abstract`）僅部分出版社提供，故本站的判讀以標題、作者、期刊、
以及必要時的 WebFetch 補充為準，**不假裝讀過全文**。

---

## 國際關係（10）

| 期刊 | ISSN | 備註 |
|---|---|---|
| Foreign Affairs | 0015-7120 | 政策評論，另有 RSS 可交叉 |
| Foreign Policy | 0015-7228 | 政策評論，另有 RSS 可交叉 |
| International Security | 0162-2889 | 安全研究頂刊 |
| International Organization | 0020-8183 | 國際制度頂刊 |
| International Studies Quarterly | 0020-8833 | ISA 旗艦 |
| Security Studies | 0963-6412 | 安全研究 |
| World Politics | 0043-8871 | 比較政治與國關 |
| European Journal of International Relations | 1354-0661 | 歐陸理論取向 |
| Review of International Studies | 0260-2105 | 英國學派 |
| International Affairs | 0020-5850 | Chatham House |

## 戰略與軍事（7）

| 期刊 | ISSN | 備註 |
|---|---|---|
| Journal of Strategic Studies | 0140-2390 | 戰略研究 |
| Survival | 0039-6338 | IISS，政策與戰略 |
| The Washington Quarterly | 0163-660X | CSIS，政策取向 |
| Journal of Peace Research | 0022-3433 | 量化衝突研究 |
| Journal of Conflict Resolution | 0022-0027 | 量化衝突研究 |
| Armed Forces & Society | 0095-327X | 軍隊與社會 |
| Intelligence and National Security | 0268-4527 | 情報研究 |
| The US Army War College Quarterly: Parameters | 0031-1723 | 美陸軍戰院季刊 |

**Naval War College Review 不可用**：Crossref 查無此刊（ISSN 0028-1484 回 404），
以 Parameters 替代。需該刊內容時以 WebSearch 補。

## 會計與財稅（7）

| 期刊 | ISSN | 備註 |
|---|---|---|
| The Accounting Review | 0001-4826 | AAA 旗艦 |
| Journal of Accounting and Economics | 0165-4101 | 實證會計 |
| Journal of Accounting Research | 0021-8456 | 芝加哥學派 |
| Contemporary Accounting Research | 0823-9150 | CAAA |
| Accounting, Organizations and Society | 0361-3682 | 會計與制度 |
| National Tax Journal | 0028-0283 | 稅制 |
| Review of Accounting Studies | 1380-6653 | 實證會計 |

**注意**：會計期刊的 Crossref 條目含大量前置與後置資料（編輯資料、廣告、
會議公告），`fetch.py` 已設過濾規則，見 `EDITORIAL.md` 第四節。

## AI 與法律（9）

| 期刊 | ISSN | 備註 |
|---|---|---|
| AI & Society | 0951-5666 | AI 與社會 |
| Artificial Intelligence and Law | 0924-8463 | AI 法律專刊 |
| Minds and Machines | 0924-6495 | AI 哲學與倫理 |
| Journal of Artificial Intelligence Research | 1076-9757 | JAIR，技術 |
| Computer Law & Security Review | 0267-3649 | 資訊法與資安法 |
| Harvard Law Review | 0017-811X | 法學評論 |
| Yale Law Journal | 0044-0094 | 法學評論 |
| Stanford Law Review | 0038-9765 | 法學評論 |
| Columbia Law Review | 0010-1958 | 法學評論 |

## 區域研究（9）

| 期刊 | ISSN | 備註 |
|---|---|---|
| The China Quarterly | 0305-7410 | 中國研究頂刊 |
| The China Journal | 1324-9347 | 中國研究 |
| China Perspectives | 2070-3449 | 法國現代中國研究中心 |
| Journal of Contemporary China | 1067-0564 | 當代中國 |
| Asian Survey | 0004-4687 | 亞洲區域 |
| The Pacific Review | 0951-2748 | 亞太 |
| Contemporary Southeast Asia | 0129-797X | 東南亞，ISEAS |
| Journal of East Asian Studies | 1598-2408 | 東亞 |
| Asian Security | 1479-9855 | 亞洲安全 |

## 政治經濟與科技政策（6）

| 期刊 | ISSN | 備註 |
|---|---|---|
| Review of International Political Economy | 0969-2290 | 國際政經 |
| New Political Economy | 1356-3467 | 政治經濟 |
| Research Policy | 0048-7333 | 科技創新政策 |
| Science and Public Policy | 0302-3427 | 科技政策 |
| Technological Forecasting and Social Change | 0040-1625 | 科技預測 |
| Energy Policy | 0301-4215 | 能源政策 |

---

## 清單調整紀錄

- 2026-08-23：建站，48 種期刊分六個領域。全數以 Crossref 實測，
  `container-title` 與 `total-results` 均核對。
  Naval War College Review 查無此刊，以 Parameters 替代。
