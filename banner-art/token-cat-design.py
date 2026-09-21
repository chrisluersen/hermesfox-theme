# cat-in-box, hjw removed, two-tone carbonfox.
# FIDELITY-CRITICAL: the plain art (tags stripped) must reconstruct the source
# char-for-char. Split segments are NOT rstripped (that loses interior gap
# spaces); only the row's natural right padding is trimmed once, up front.
CATBOX_RAW = [
    "  ,-.       _,---._ __  / \\",
    " /  )    .-'       `./ /   \\",
    "(  (   ,'            `/    /|",
    " \\  `-\"             \\'\\   / |",
    "  `.              ,  \\ \\ /  |",
    "   /`.          ,'-`----Y   |",
    "  (            ;        |   '",
    "  |  ,-.    ,-'         |  /",
    "  |  | (   |            | /",
    "  )  |  \\  `.___________|/",
    "  `--'   `--'",
]
# box starts at this column (0-indexed) for each row
SPLIT = [13, 16, 19, 17, 18, 18, 18, 18, 19, 14, 8]
CAT = "#33b1ff"
BOX = "#7f8489"

def build():
    out = []
    for raw, sp in zip(CATBOX_RAW, SPLIT):
        row = raw.rstrip()                                   # trim right padding once
        indent = row[:len(row) - len(row.lstrip())]          # leading art spaces
        body = row[len(indent):]                             # rest after indent
        cut = sp - len(indent)
        cat_part = body[:cut]                                # exact, no strip
        box_part = body[cut:]                                # exact, no strip
        # art indent INSIDE the cat tag so every YAML line has uniform 2-space indent
        pieces = [f"[{CAT}]{indent}{cat_part}[/]"] if cat_part.strip() else []
        if box_part.strip():
            pieces.append(f"[{BOX}]{box_part}[/]")
        out.append("".join(pieces))
    return out

if __name__ == "__main__":
    for r in build():
        print(r)
