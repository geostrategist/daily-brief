"""Promote a reviewed draft from conflict/_drafts/ into conflict/briefs/ and push.

The 04:00 local run writes a draft and stops. Nothing reaches the site until this
script runs, so a bad brief is a file on disk rather than a published page.

    python conflict/_system/publish.py              # today's draft
    python conflict/_system/publish.py 20260820     # a specific date
    python conflict/_system/publish.py --list       # what is waiting
    python conflict/_system/publish.py --dry-run    # show the plan, touch nothing

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

import style_check

if hasattr(sys.stdout, "reconfigure"):          # Windows consoles default to cp950
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):          # SystemExit messages go to stderr
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent   # …/conflict
REPO = ROOT.parent
DRAFTS = ROOT / "_drafts"
BRIEFS = ROOT / "briefs"


def run(cmd, check=True, capture=True):
    """Run a command in the repo root and return its stdout."""
    r = subprocess.run(cmd, cwd=REPO, capture_output=capture, text=True,
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


def check_draft(path):
    """Surface the problems worth catching before a brief goes public.

    Advisory only. The brief is a judgement call and this cannot make it; it
    flags the mechanical failures that are embarrassing once published, plus the
    prose habits ruled out by EDITORIAL.md section 13.
    """
    text = path.read_text(encoding="utf-8")
    warn = []

    required = ["今日三分鐘摘要", "兩岸", "東亞", "南海", "南太平洋",
                "南亞", "中亞", "跨區域結構", "巡檢摘要"]
    missing = [h for h in required if f"## {h}" not in text]
    if missing:
        warn.append("缺少固定欄位：" + "、".join(missing))

    items = re.findall(r"^### \d+\.", text, re.M)
    graded = re.findall(r"〔[ABC]〕", text)
    if items and len(graded) < len(items):
        warn.append(f"{len(items)} 則之中只有 {len(graded)} 則標了來源等級〔A〕〔B〕〔C〕")

    if "待查核" not in text:
        warn.append("全文沒有「待查核」")

    # the placeholder that means the model did not finish a section
    for ph in ["TODO", "TBD", "待補", "XXX", "（待填）"]:
        if ph in text:
            warn.append(f"仍留有佔位字樣「{ph}」")

    # Stage markers are how a geographically-sectioned brief still tells the
    # reader whether a thing is brewing, being fought, or being negotiated.
    items = re.findall(r"^### \d+\.(.*)$", text, re.M)
    staged = [i for i in items if re.search(r"\[(徵候|交戰|談判|停火|結構)\]", i)]
    if items and len(staged) < len(items):
        warn.append(f"{len(items)} 則之中只有 {len(staged)} 則標了階段"
                    "〔徵候／交戰／談判／停火／結構〕")

    # Three per region, per EDITORIAL.md section 9. Without the cap the two
    # busiest regions crowd out the other four.
    for region in ["兩岸", "東亞", "南海", "南太平洋", "南亞", "中亞"]:
        if f"## {region}" not in text:
            continue
        seg = text.split(f"## {region}", 1)[1].split("\n## ", 1)[0]
        n = len(re.findall(r"^### \d+\.", seg, re.M))
        if n > 3:
            warn.append(f"{region} 有 {n} 則，超過每區三則上限")

    if len(text) < 2000:
        warn.append(f"全文僅 {len(text)} 字元，偏短，確認是否被截斷")

    warn.extend(style_check.check(text))       # EDITORIAL.md 第十三節
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
            published = (BRIEFS / f.name).exists()
            mark = "　已發布過" if published else ""
            print(f"  {date}  {kb:6.1f} KB{mark}")
        print(f"\n發布：python conflict/_system/publish.py [YYYYMMDD]")
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
            f"  git diff --no-index conflict/briefs/{draft.name} conflict/_drafts/{draft.name}"
        )

    iso = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    kb = draft.stat().st_size / 1024
    print(f"草稿：{draft}")
    print(f"日期：{iso}　大小：{kb:.1f} KB")

    warn = check_draft(draft)
    if warn:
        print("\n檢查發現：")
        for w in warn:
            print(f"  ⚠ {w}")
        print("  （以上為提醒，不阻擋發布）")
    else:
        print("檢查：固定欄位、來源等級、待查核、文體均無異常。")

    print(f"\n將執行：")
    print(f"  1. 複製到 conflict/briefs/{draft.name}")
    print(f"  2. python conflict/_system/rebuild-manifest.py")
    print(f"  3. git add conflict/ && git commit -m 'conflict: {iso}' && git push")

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

    out = run([sys.executable, str(ROOT / "_system" / "rebuild-manifest.py")])
    print(out)

    if not run(["git", "config", "user.email"], check=False):
        run(["git", "config", "user.name", "geostrategist"])
        run(["git", "config", "user.email", "geostrategist@gmail.com"])

    run(["git", "add", "conflict/"])
    if not run(["git", "diff", "--cached", "--name-only"], check=False):
        print("沒有變更需要提交（內容與已發布版本相同）。")
        return

    run(["git", "commit", "-m", f"conflict: {iso}"])
    print(f"已提交：conflict: {iso}")

    r = subprocess.run(["git", "push"], cwd=REPO, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("\npush 失敗：")
        print((r.stdout or "") + (r.stderr or ""))
        print("已 commit 但未推送，處理完網路或權限問題後執行 git push。")
        raise SystemExit(1)

    print("已推送。")
    print(f"https://geostrategist.github.io/daily-brief/conflict/ （GitHub Pages 約需一分鐘）")
    draft.unlink()
    print(f"草稿已清除：{draft.name}")


if __name__ == "__main__":
    main()
