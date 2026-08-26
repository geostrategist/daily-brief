"""Promote a reviewed draft from _drafts/ into briefs/ and push.

The 05:00 local run writes a draft and stops. Nothing reaches the site until
this script runs, so a bad brief is a file on disk rather than a published page.

    python _system/publish.py              # today's draft
    python _system/publish.py 20260821     # a specific date
    python _system/publish.py --list       # what is waiting
    python _system/publish.py --dry-run    # show the plan, touch nothing

Refuses to overwrite an already-published brief unless --force is given: the
common accident is re-running a draft over a brief that was edited after
publication, and silently losing those edits.
"""

import argparse
import datetime
import re
import shutil
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):          # Windows consoles default to cp950
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):          # SystemExit messages go to stderr
    sys.stderr.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parent.parent   # …/09_daily_brief
DRAFTS = REPO / "_drafts"
BRIEFS = REPO / "briefs"


def run(cmd, check=True):
    """Run a command in the repo root and return its stdout."""
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        out = (r.stdout or "") + (r.stderr or "")
        raise SystemExit(f"失敗：{' '.join(cmd)}\n{out.strip()}")
    return (r.stdout or "").strip()


def drafts_waiting():
    if not DRAFTS.exists():
        return []
    out = []
    for f in sorted(DRAFTS.glob("Brief_*.md"), reverse=True):
        m = re.fullmatch(r"Brief_(\d{8})\.md", f.name)
        if m:
            out.append((m.group(1), f))
    return out


def check_draft(path, date):
    """Surface the problems worth catching before a brief goes public.

    Advisory only. Whether the brief is any good is a judgement call and this
    cannot make it; it flags the mechanical failures that are embarrassing once
    published, and the two failure modes actually seen in production: a market
    table where every index failed to fetch, and a calendar still listing dates
    that have already passed.
    """
    text = path.read_text(encoding="utf-8")
    warn = []

    required = ["今日三分鐘摘要", "前一日市場", "建議決策行動",
                "應持續追蹤議題", "巡檢摘要"]
    missing = [h for h in required if f"## {h}" not in text]
    if missing:
        warn.append("缺少固定欄位：" + "、".join(missing))

    # Six since 2026-08-24, per DAILY_PROMPT.md and EDITORIAL.md section 6.
    topics = re.findall(r"^## 主題[一二三四五六]", text, re.M)
    if len(topics) < 6:
        warn.append(f"只有 {len(topics)} 個主題，應為 6 個")

    items = re.findall(r"^### \d+\.", text, re.M)
    graded = re.findall(r"〔[ABC]〕", text)
    baseline = re.findall(r"〔巡檢基線〕", text)
    if items and len(graded) + len(baseline) < len(items):
        warn.append(f"{len(items)} 則之中只有 {len(graded)} 則標了來源等級、"
                    f"{len(baseline)} 則為巡檢基線，合計不足")

    if "待查核" not in text:
        warn.append("全文沒有「待查核」")

    if "未來事件行事曆" not in text:
        warn.append("缺少「未來事件行事曆」（EDITORIAL 第十二節）")

    # the placeholder that means the model did not finish a section
    for ph in ["TODO", "TBD", "待補", "XXX", "（待填）"]:
        if ph in text:
            warn.append(f"仍留有佔位字樣「{ph}」")

    # the cloud-routine failure signature: every index unfetched
    market = re.search(r"## 前一日市場(.*?)^## ", text, re.S | re.M)
    if market and market.group(1).count("未取得") >= 6:
        warn.append("市場表六個指數全部「未取得」，確認 market.py 是否被網路阻擋")

    # a calendar row whose date has already passed
    try:
        today = datetime.date(int(date[:4]), int(date[4:6]), int(date[6:]))
    except ValueError:
        today = None
    if today:
        cal = re.search(r"\*\*未來事件行事曆\*\*(.*?)^---", text, re.S | re.M)
        if cal:
            for mm, dd in re.findall(r"^\|\s*(\d{2})-(\d{2})\s*\|", cal.group(1), re.M):
                # a month far behind today's is next year's, not a stale row
                row = datetime.date(today.year, int(mm), int(dd))
                if row < today and (today - row).days < 300:
                    warn.append(f"行事曆仍列有已過期的日期 {mm}-{dd}"
                                f"（今天 {today:%m-%d}），第十二節第 1 點要求移除")

    if len(text) < 4000:
        warn.append(f"全文僅 {len(text)} 字元，偏短，確認是否被截斷或巡檢失敗")

    return warn


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("date", nargs="?", help="YYYYMMDD，省略則用今天")
    ap.add_argument("--list", action="store_true", help="列出待發布的草稿")
    ap.add_argument("--dry-run", action="store_true", help="只顯示將要做什麼")
    ap.add_argument("--force", action="store_true", help="覆蓋已發布的同日晨報")
    ap.add_argument("--yes", "-y", action="store_true", help="不詢問直接發布")
    args = ap.parse_args()

    waiting = drafts_waiting()

    if args.list:
        if not waiting:
            print("沒有待發布的草稿。")
            return
        print(f"待發布草稿（{len(waiting)} 份）：\n")
        for date, f in waiting:
            kb = f.stat().st_size / 1024
            mark = "　已發布過" if (BRIEFS / f.name).exists() else ""
            print(f"  {date}  {kb:6.1f} KB{mark}")
        print("\n發布：python _system/publish.py [YYYYMMDD]")
        return

    date = args.date or datetime.date.today().strftime("%Y%m%d")
    if not re.fullmatch(r"\d{8}", date):
        raise SystemExit(f"日期格式應為 YYYYMMDD，收到：{date}")

    draft = DRAFTS / f"Brief_{date}.md"
    if not draft.exists():
        print(f"找不到草稿：{draft}")
        if waiting:
            print("\n目前有這些草稿：")
            for d, _ in waiting:
                print(f"  {d}")
        raise SystemExit(1)

    target = BRIEFS / draft.name
    if target.exists() and not args.force:
        raise SystemExit(
            f"{target.name} 已發布過。\n"
            f"確定要覆蓋就加 --force；先比對差異：\n"
            f"  git diff --no-index briefs/{draft.name} _drafts/{draft.name}"
        )

    iso = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    kb = draft.stat().st_size / 1024
    print(f"草稿：{draft}")
    print(f"日期：{iso}　大小：{kb:.1f} KB")

    warn = check_draft(draft, date)
    if warn:
        print("\n檢查發現：")
        for w in warn:
            print(f"  ⚠ {w}")
        print("  （以上為提醒，不阻擋發布）")
    else:
        print("檢查：固定欄位、六個主題、來源等級、待查核、行事曆、市場表均無異常。")

    print("\n將執行：")
    print(f"  1. 複製到 briefs/{draft.name}")
    print("  2. python _system/rebuild-manifest.py")
    print(f"  3. git add briefs/ && git commit -m 'brief: {iso}' && git push")

    if args.dry_run:
        print("\n--dry-run：未執行任何動作。")
        return

    if not args.yes:
        ans = input("\n確定發布？(y/N) ").strip().lower()
        if ans not in ("y", "yes"):
            print("已取消，草稿保留原處。")
            return

    shutil.copy2(draft, target)
    print(f"\n已複製 → {target}")

    print(run([sys.executable, str(REPO / "_system" / "rebuild-manifest.py")]))

    if not run(["git", "config", "user.email"], check=False):
        run(["git", "config", "user.name", "geostrategist"])
        run(["git", "config", "user.email", "geostrategist@gmail.com"])

    run(["git", "add", "briefs/"])
    if not run(["git", "diff", "--cached", "--name-only"], check=False):
        print("沒有變更需要提交（內容與已發布版本相同）。")
        return

    run(["git", "commit", "-m", f"brief: {iso}"])
    print(f"已提交：brief: {iso}")

    r = subprocess.run(["git", "push"], cwd=REPO, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("\npush 失敗：")
        print((r.stdout or "") + (r.stderr or ""))
        print("已 commit 但未推送，處理完網路或權限問題後執行 git push。")
        raise SystemExit(1)

    print("已推送。")
    print("https://geostrategist.github.io/daily-brief/ （GitHub Pages 約需一分鐘）")
    draft.unlink()
    print(f"草稿已清除：{draft.name}")


if __name__ == "__main__":
    main()
