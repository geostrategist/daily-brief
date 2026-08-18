"""Fetch previous-session closes for the indices the brief opens with.

Prints a ready-to-paste Markdown table plus a machine-readable JSON block.
Indices that fail are reported as 未取得 rather than silently dropped, so the
brief can record the gap.

Usage:  python _system/market.py
"""

import datetime
import json
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

INDICES = [
    ("道瓊", "^DJI"),
    ("標普 500", "^GSPC"),
    ("那斯達克", "^IXIC"),
    ("費城半導體", "^SOX"),
    ("台股加權", "^TWII"),
    ("日經 225", "^N225"),
]


def fetch(symbol):
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
           + urllib.parse.quote(symbol)
           + "?range=5d&interval=1d")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        meta = json.load(r)["chart"]["result"][0]["meta"]

    last = meta.get("regularMarketPrice")
    prev = meta.get("chartPreviousClose")
    if last is None or prev is None:
        raise ValueError("missing price fields")

    ts = meta.get("regularMarketTime")
    date = ""
    if ts:
        # stamp the close in the exchange's own local time, not UTC
        tzoff = meta.get("gmtoffset") or 0
        date = datetime.datetime.fromtimestamp(
            ts + tzoff, datetime.timezone.utc).strftime("%Y-%m-%d")

    return {"last": last, "prev": prev, "chg": last - prev,
            "pct": (last - prev) / prev * 100, "date": date}


rows, data = [], {}
for name, sym in INDICES:
    try:
        d = fetch(sym)
        data[name] = d
        rows.append("| {} | {:,.2f} | {:+,.2f} | {:+.2f}% | {} |".format(
            name, d["last"], d["chg"], d["pct"], d["date"]))
    except Exception as e:                      # noqa: BLE001 - report, don't crash the run
        data[name] = {"error": str(e)}
        rows.append("| {} | 未取得 | 未取得 | 未取得 | — |".format(name))

print("| 指數 | 收盤 | 漲跌 | 幅度 | 收盤日 |")
print("|---|---|---|---|---|")
print("\n".join(rows))
print()
print("<!-- raw")
print(json.dumps(data, ensure_ascii=False, indent=2))
print("-->")
