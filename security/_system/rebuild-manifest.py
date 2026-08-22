"""Regenerate briefs/manifest.json from the Brief_*.md files on disk.

Run after adding or removing a brief. Newest date first.
"""
import json
import re
from pathlib import Path

briefs_dir = Path(__file__).resolve().parent.parent / "briefs"
entries = []
for f in sorted(briefs_dir.glob("Brief_*.md")):
    m = re.fullmatch(r"Brief_(\d{4})(\d{2})(\d{2})\.md", f.name)
    if not m:
        print(f"skip (unexpected name): {f.name}")
        continue
    entries.append({"date": "-".join(m.groups()), "file": f.name})

entries.sort(key=lambda e: e["date"], reverse=True)
out = briefs_dir / "manifest.json"
out.write_text(json.dumps({"briefs": entries}, ensure_ascii=False, indent=2) + "\n",
               encoding="utf-8")
print(f"{len(entries)} brief(s) -> {out}")
