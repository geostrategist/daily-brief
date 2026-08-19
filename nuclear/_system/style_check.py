"""Prose checks for a draft brief, per EDITORIAL.md section 13.

Advisory only. These are habits to notice before publishing, not errors: a brief
occasionally needs a colon, and thresholds are deliberately loose so a normal
day passes clean and only a real drift trips them.

Tables, code fences, link targets and source lines are excluded. They carry
their own conventions and would otherwise swamp the signal.
"""

import re

# Phrases ruled out outright.
BANNED = [
    ("值得注意的是", "填充語"),
    ("綜上所述", "填充語"),
    ("在當前背景下", "填充語"),
    ("整體而言", "填充語"),
    ("總的來說", "填充語"),
    ("重大突破", "誇示形容詞"),
    ("前所未有", "誇示形容詞"),
    ("徹底改變", "誇示形容詞"),
    ("關鍵轉折", "誇示形容詞"),
    ("值得注意地", "副詞開頭加逗點"),
    ("令人意外地", "副詞開頭加逗點"),
    ("本節將", "自我提示語氣"),
    ("以下先", "自我提示語氣"),
    ("接下來要處理的是", "自我提示語氣"),
]

# Parallel constructions: they pack a relationship into the syntax, so a reader
# can only accept or reject it rather than check it.
PARALLEL = [
    (r"不是[^。，]{1,24}而是", "「不是⋯而是⋯」"),
    (r"贏得了[^。]{1,30}卻輸掉", "「贏得了⋯卻輸掉了⋯」"),
    (r"之所以[^。]{1,30}是因為", "「之所以⋯是因為⋯」"),
]

# Turns of phrase that read as machine-written: inflated significance, hollow
# hedging, and the summarising cadence a model reaches for when it has nothing
# further to add.
AI_TELLS = [
    ("扮演著", "AI 語法"),
    ("發揮著", "AI 語法"),
    ("起到了", "AI 語法"),
    ("具有重要意義", "AI 語法"),
    ("有著深遠的影響", "AI 語法"),
    ("不僅僅是", "AI 語法"),
    ("在某種程度上", "空話"),
    ("可以說是", "空話"),
    ("眾所周知", "空話"),
    ("隨著⋯的發展", "AI 語法"),
    ("為⋯奠定了基礎", "AI 語法"),
    ("值得深思", "AI 語法"),
    ("引發廣泛關注", "AI 語法"),
    ("備受矚目", "AI 語法"),
    ("進一步凸顯", "AI 語法"),
    ("這一舉措", "AI 語法"),
    ("這一趨勢表明", "AI 語法"),
    ("標誌著", "AI 語法"),
    ("彰顯", "AI 語法"),
    ("持續關注", "無資訊"),
    ("密切關注", "無資訊"),
    ("拭目以待", "無資訊"),
    ("未來可期", "無資訊"),
]

# Mainland-Chinese or loose renderings. Left column is the official Taiwanese
# term; see REFERENCE.md section 8 for the statutory source of each.
TERMS = [
    ("乏燃料", "用過核子燃料"),
    ("廢燃料", "用過核子燃料"),
    ("貧化鈾", "耗乏鈾"),
    ("貧鈾", "耗乏鈾"),
    ("鈈", "鈽"),
    ("反應堆", "反應器"),
    ("安全殼", "圍阻體"),
    ("乾儲", "乾式貯存"),
    ("儲存設施", "貯存設施"),
    ("核素", "核種"),
    ("多重屏障", "多重障壁"),
    ("核電站", "核能電廠"),
    ("核污水", "含氚廢水"),
    ("核廢水", "含氚廢水"),
    ("電離輻射", "游離輻射"),
    ("退役", "除役"),
    ("保障監督", "核子保防"),
    ("保障措施", "核子保防"),
    ("核安保", "核子保安"),
    ("物理保護", "實體防護"),
    ("深度防禦", "縱深防禦"),
    ("關鍵區域", "要害區域"),
    ("監管機構", "主管機關"),
    ("原能會", "核安會"),
    ("原子能委員會", "核能安全委員會"),
]

CJK = r"一-鿿"


def prose_only(text):
    """Drop tables, fences, source lines and URLs, keeping body prose."""
    out = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or stripped.startswith("|") or stripped.startswith("- 來源："):
            continue
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", stripped):     # horizontal rule
            continue
        out.append(re.sub(r"\]\([^)]*\)", "]", line))
    return "\n".join(out)


def check(text):
    """Return a list of advisory warnings about the draft's prose."""
    warn = []
    prose = prose_only(text)

    for phrase, why in BANNED:
        if phrase in prose:
            warn.append(f"文體：出現「{phrase}」（{why}）")

    for phrase, why in AI_TELLS:
        if phrase in prose:
            warn.append(f"文體：出現「{phrase}」（{why}）")

    # Terminology is not a style preference: these are the statutory terms.
    for wrong, right in TERMS:
        if wrong in prose:
            warn.append(f"用語：出現「{wrong}」，法規用語為「{right}」")

    for pattern, label in PARALLEL:
        n = len(re.findall(pattern, prose))
        if n:
            warn.append(f"文體：{label} 出現 {n} 次")

    for pattern, label in [(r"——", "破折號"), (r"(?<![-<!])--(?!>)", "--"), (r"；", "分號")]:
        n = len(re.findall(pattern, prose))
        if n:
            warn.append(f"文體：{label} 出現 {n} 次")

    # Colons the format prescribes: the lede, the caveat line, the digest labels
    # and the inspection-summary labels. Only prose colons beyond those count.
    prescribed = (r"(一句話摘要|待查核|今天真正改變了什麼|最重要的三件事|可能受影響"
                  r"|對台灣的意義|歷史比對|安全聲明|來源篩選|來源品質問題|提示注入"
                  r"|完全失敗[^：]*|部分失敗[^：]*|單位核對|金額核對|規範編號|機組核對"
                  r"|觸發條件|範圍|優先訊號|刻意排除|來源)：")
    # One lede plus one caveat line per item already accounts for most of them,
    # so the threshold scales with the number of items rather than being fixed.
    items = max(1, len(re.findall(r"^### \d+\.", prose, re.M)))
    colons = len(re.findall(r"：", prose)) - len(re.findall(prescribed, prose))
    if colons > items + 8:
        warn.append(f"文體：冒號約 {colons} 處（已扣除既定格式），偏多")

    spaced = (len(re.findall(rf"[{CJK}] +[A-Za-z0-9]", prose))
              + len(re.findall(rf"[A-Za-z0-9] +[{CJK}]", prose)))
    if spaced > 5:
        warn.append(f"文體：中英數之間有空白約 {spaced} 處，本報格式不加空白")

    # Bold is sanctioned for the judgement opener, the digest and inspection
    # labels, and the leading phrase of an action item. Count only the rest.
    bold = re.findall(r"\*\*([^*\n]+)\*\*", prose)
    label = re.compile(r"^(今天真正改變了什麼|最重要的三件事|可能受影響|對台灣的意義"
                       r"|歷史比對|安全聲明|來源篩選|來源品質問題|提示注入|單位核對"
                       r"|完全失敗|部分失敗|數量級誤譯|單位標示不全|機組編號不明)")
    openers = len(re.findall(r"^\*\*", prose, re.M))
    extra = [b for b in bold if not label.match(b)]
    if len(extra) - openers > 10:
        warn.append(f"文體：粗體 {len(bold)} 處，超出判讀首句與既定標籤的用量")

    de = prose.count("的")
    if de > 220:
        warn.append(f"文體：「的」{de} 次，偏多，多數可刪")

    le = len(re.findall(r"了[，。、）]", prose))
    if le > 25:
        warn.append(f"文體：句末「了」{le} 次，偏多")

    return warn


if __name__ == "__main__":
    import sys
    from pathlib import Path

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        raise SystemExit("用法：python style_check.py <檔案>")
    problems = check(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if problems:
        for p in problems:
            print(f"  ⚠ {p}")
    else:
        print("文體檢查無異常。")
