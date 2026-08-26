# -*- coding: utf-8 -*-
"""Pull new journal articles from Crossref and write them to a JSON file.

The daily agent reads that file rather than calling the API itself: 48 journals
is too many WebFetch calls, and the selection judgement is the agent's job while
the fetching is not.

    python journals/_system/fetch.py                 # since the last run
    python journals/_system/fetch.py --days 7        # explicit window
    python journals/_system/fetch.py --out x.json

Crossref's `created` date is when the DOI was registered, which is what "new
today" means for our purpose — `published` can be a future issue date, and for
online-first articles it lags registration by months.
"""
import argparse
import datetime
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent          # …/journals
UA = "daily-brief/1.0 (mailto:geostrategist@gmail.com)"
API = "https://api.crossref.org/journals/{issn}/works"

# Front/back matter and other non-article records that Crossref carries for
# several journals (accounting titles are the worst offenders). Matched against
# the lowercased title.
JUNK = re.compile(
    r"^(front|back)\s+(matter|cover)|^editorial\s+(data|board)|^issue\s+information"
    r"|^table\s+of\s+contents|^contents$|^index$|^masthead|^erratum|^correction"
    r"|^corrigendum|^retraction|^acknowledg|^announcement|^call\s+for\s+papers"
    r"|^placement\s+ads|^advertis|^subscription|^editors.{0,3}\s+note$"
    r"|^books\s+received|^book\s+review|^in\s+memoriam|^obituar",
    re.I)


def parse_journals(path):
    """Read JOURNALS.md and return [(field, name, issn), ...]."""
    text = io.open(path, encoding="utf-8").read()
    out, field = [], ""
    for line in text.split("\n"):
        m = re.match(r"^##\s+(.+?)(?:（\d+）)?\s*$", line)
        if m:
            field = m.group(1).strip()
            continue
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*(\d{4}-\d{3}[\dXx])\s*\|", line)
        if m:
            out.append((field, m.group(1).strip(), m.group(2).upper()))
    return out


def get(url, tries=4):
    """GET with retry: Crossref rate-limits bursts, and a 429 is not fatal."""
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 500, 502, 503):
                time.sleep(2 * (i + 1))
                continue
            raise
        except Exception as e:                          # noqa: BLE001 - network flakiness
            last = e
            time.sleep(2 * (i + 1))
    raise last


def clean_abstract(raw):
    if not raw:
        return ""
    txt = re.sub(r"<[^>]+>", " ", raw)                  # JATS tags
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt[:600]


def fetch_journal(field, name, issn, since):
    q = urllib.parse.urlencode({
        "filter": "from-created-date:" + since,
        "rows": 40,
        "sort": "created",
        "order": "desc",
        "select": "title,author,created,DOI,URL,container-title,type,abstract,page,volume,issue",
    })
    url = API.format(issn=issn) + "?" + q
    try:
        msg = get(url)["message"]
    except Exception as e:                              # noqa: BLE001
        return {"field": field, "journal": name, "issn": issn,
                "error": "%s: %s" % (type(e).__name__, str(e)[:80]), "items": []}

    items = []
    for it in msg.get("items", []):
        title = (it.get("title") or [""])[0].strip()
        if not title or JUNK.search(title):
            continue
        if it.get("type") not in (None, "journal-article"):
            continue
        authors = []
        for a in (it.get("author") or [])[:6]:
            nm = (a.get("family") or "").strip()
            if nm:
                authors.append(nm)
        created = "-".join("%02d" % n for n in
                           (it.get("created", {}).get("date-parts") or [[0]])[0])
        items.append({
            "title": title,
            "authors": authors,
            "created": created,
            "doi": it.get("DOI", ""),
            "url": it.get("URL", ""),
            "volume": it.get("volume", ""),
            "issue": it.get("issue", ""),
            "page": it.get("page", ""),
            "abstract": clean_abstract(it.get("abstract")),
        })
    return {"field": field, "journal": name, "issn": issn,
            "total": msg.get("total-results", 0), "items": items}



def write_state(path, text):
    """Record the run date, tolerating pCloud's handling of dotfiles.

    The repo lives on a pCloud virtual drive (exFAT). pCloud re-applies the
    Hidden attribute to this dotfile behind our back, and Windows fails an
    open-for-write on an existing hidden file with ERROR_ACCESS_DENIED, so a
    plain write_text raises PermissionError. attrib -H does not stick on that
    filesystem; deleting first does. Fall back to that, then to a temp-file
    replace.

    This is bookkeeping only - the Crossref json is already on disk by now, so
    a failure here must never fail the run. It only costs the next run its
    incremental window, and that degrades to the 7-day default.
    """
    try:
        path.write_text(text, encoding="utf-8")
        return
    except PermissionError:
        pass

    try:
        path.unlink(missing_ok=True)
        path.write_text(text, encoding="utf-8")
        return
    except OSError:
        pass

    try:
        tmp = path.with_suffix(".tmp")
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    except OSError as exc:                              # noqa: BLE001
        print("  ! 無法更新 %s（%s），下次改用 7 天預設區間" % (path.name, exc))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=None,
                    help="回溯天數；省略則自上次執行起算，首次執行為7天")
    ap.add_argument("--out", default=None, help="輸出路徑，預設 _drafts/crossref_YYYYMMDD.json")
    ap.add_argument("--list", action="store_true", help="只列出期刊清單")
    args = ap.parse_args()

    journals = parse_journals(ROOT / "_system" / "JOURNALS.md")
    if args.list:
        for f, n, i in journals:
            print("%-12s %-46s %s" % (f, n, i))
        print("\n共 %d 種" % len(journals))
        return

    state_file = ROOT / "_system" / ".last-run"
    today = datetime.date.today()
    if args.days is not None:
        since_d = today - datetime.timedelta(days=args.days)
    elif state_file.exists():
        try:
            since_d = datetime.date.fromisoformat(state_file.read_text().strip())
        except Exception:                               # noqa: BLE001
            since_d = today - datetime.timedelta(days=7)
    else:
        since_d = today - datetime.timedelta(days=7)
    since = since_d.isoformat()

    print("查詢 %d 種期刊，自 %s 起新登錄者" % (len(journals), since))
    results, n_items, n_err = [], 0, 0
    for field, name, issn in journals:
        r = fetch_journal(field, name, issn, since)
        results.append(r)
        if r.get("error"):
            n_err += 1
            print("  ! %-44s %s" % (name[:44], r["error"]))
        else:
            k = len(r["items"])
            n_items += k
            if k:
                print("  + %-44s %d 篇" % (name[:44], k))
        time.sleep(0.8)                                 # be polite to the API

    out = Path(args.out) if args.out else (ROOT / "_drafts" /
                                           ("crossref_%s.json" % today.strftime("%Y%m%d")))
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "since": since,
        "journal_count": len(journals),
        "article_count": n_items,
        "error_count": n_err,
        "journals": results,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_state(state_file, today.isoformat())

    print("\n新文章 %d 篇，查詢失敗 %d 種 → %s" % (n_items, n_err, out))


if __name__ == "__main__":
    main()
