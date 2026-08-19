"""Fetch previous-session closes for the indices the brief opens with.

Prints a ready-to-paste Markdown table plus a machine-readable JSON block.
Indices that fail are reported as 未取得 rather than silently dropped, so the
brief can record the gap.

The change is measured against the PREVIOUS TRADING DAY's close, taken from the
daily bar series. Do not use meta.chartPreviousClose: for a ranged request that
field holds the close preceding the *window*, not the previous session, so it
silently compares against a price several sessions old. That bug produced wrong
漲跌 and 幅度 for all six indices in the 2026-08-18 brief.

The table is 前一日市場, so every row is the last COMPLETED session, never a
mid-session quote. When the brief runs off-schedule and an Asian market is
already open, that market's live price is carried in the raw JSON for the
narrative instead of contaminating the table.

Yahoo intermittently returns a null daily bar for a session that did trade
(^N225 and ^TWII for 2026-08-18), and backfills it hours later. Falling back to
the 60-minute series keeps the baseline on the right session, but the last
hourly bar is NOT the close - it misses the closing auction. ^N225 on
2026-08-18 closed at 67,460.73 while its final 60m bar read 67,506.77, a 46
point error that reached print. Any value taken from the hourly series is
therefore flagged 近似 in the 狀態 column and listed in the raw block, so the
brief either says so or re-runs later once the daily bar lands.

Usage:  python _system/market.py
"""

import datetime
import json
import sys
import urllib.parse
import urllib.request

if hasattr(sys.stdout, "reconfigure"):          # Windows consoles default to cp950
    sys.stdout.reconfigure(encoding="utf-8")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "Chrome/120 Safari/537.36")

INDICES = [
    ("道瓊", "^DJI"),
    ("標普 500", "^GSPC"),
    ("那斯達克", "^IXIC"),
    ("費城半導體", "^SOX"),
    ("台股加權", "^TWII"),
    ("日經 225", "^N225"),
]


def local_date(ts, tzoff):
    """Stamp an epoch second in the exchange's own local time."""
    return datetime.datetime.fromtimestamp(
        ts + tzoff, datetime.timezone.utc).strftime("%Y-%m-%d")


def chart(symbol, interval):
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
           + urllib.parse.quote(symbol)
           + "?range=1mo&interval=" + interval)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)["chart"]["result"][0]


def session_closes(result, tzoff):
    """Map local date -> that session's last traded price."""
    closes = result["indicators"]["quote"][0]["close"]
    out = {}
    for t, c in zip(result["timestamp"], closes):
        if c is not None:
            out[local_date(t, tzoff)] = c            # later bars overwrite earlier
    return out


def fetch(symbol):
    daily = chart(symbol, "1d")
    meta = daily["meta"]
    tzoff = meta.get("gmtoffset") or 0

    live = meta.get("regularMarketPrice")
    now_ts = meta.get("regularMarketTime")
    if live is None or now_ts is None:
        raise ValueError("missing price fields")
    today = local_date(now_ts, tzoff)

    # A quote from an earlier local date is by definition a completed close.
    # Only same-day quotes need the session-end check, and that check must run
    # against real wall-clock time: currentTradingPeriod tracks now, not the
    # quote, so comparing it with a stale regularMarketTime silently discards a
    # session that already closed (^TWII on 2026-08-19 at 08:00 Taipei).
    now_real = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    period = (meta.get("currentTradingPeriod") or {}).get("regular") or {}
    end = period.get("end")
    if today < local_date(now_real, tzoff):
        today_done = True
    else:
        today_done = end is not None and now_ts >= end

    by_date = session_closes(daily, tzoff)
    exact = set(by_date)                             # dates backed by a real daily bar
    try:                                             # patch Yahoo's null daily bars
        by_date = dict(session_closes(chart(symbol, "60m"), tzoff), **by_date)
    except Exception:                                # noqa: BLE001 - hourly is a bonus
        pass
    if today_done:
        by_date[today] = live
        exact.add(today)

    dates = sorted(d for d in by_date if d < today or (today_done and d == today))
    if len(dates) < 2:
        raise ValueError("need two completed sessions")
    last_d, prev_d = dates[-1], dates[-2]
    last, prev = by_date[last_d], by_date[prev_d]

    approx = [d for d in (last_d, prev_d) if d not in exact]
    return {"last": last, "prev": prev, "chg": last - prev,
            "pct": (last - prev) / prev * 100,
            "date": last_d, "prev_date": prev_d,
            "state": "收盤（近似）" if approx else "收盤",
            "approx_dates": approx,
            "live": live, "live_date": today,
            "live_intraday": not today_done and today in by_date}


rows, data = [], {}
for name, sym in INDICES:
    try:
        d = fetch(sym)
        data[name] = d
        rows.append("| {} | {:,.2f} | {:+,.2f} | {:+.2f}% | {} |".format(
            name, d["last"], d["chg"], d["pct"], d["state"]))
    except Exception as e:                      # noqa: BLE001 - report, don't crash the run
        data[name] = {"error": str(e)}
        rows.append("| {} | 未取得 | 未取得 | 未取得 | - |".format(name))

print("| 指數 | 數值 | 漲跌 | 幅度 | 狀態 |")
print("|---|---|---|---|---|")
print("\n".join(rows))
print()
for name, d in data.items():
    if "error" not in d:
        line = "<!-- {}: {} 收盤 vs 前一交易日 {} 收盤 {:,.2f}".format(
            name, d["date"], d["prev_date"], d["prev"])
        if d["approx_dates"]:
            line += "；【{} 無日線，值取自 60 分 K，非收盤價，稍後日線補上後應重跑】".format(
                "、".join(d["approx_dates"]))
        if d["live_intraday"]:
            line += "；{} 盤中即時 {:,.2f}（{:+.2f}%）".format(
                d["live_date"], d["live"], (d["live"] - d["last"]) / d["last"] * 100)
        print(line + " -->")
print()
print("<!-- raw")
print(json.dumps(data, ensure_ascii=False, indent=2))
print("-->")
