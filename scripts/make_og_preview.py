#!/usr/bin/env python
"""Generate a 1280x640 GitHub social-preview (og:image) for a public repo.

Carbonfox palette + the swan banner art from hermesfox-theme/ascii-art.

Usage:
  python make_og_preview.py <repo_name> <tagline> <out_path> [swan_art_path]
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Carbonfox palette
BG        = (22, 22, 22)      # #161616
BG_ALT    = (13, 13, 13)      # #0d0d0d
SURFACE   = (40, 40, 40)      # #282828
FG        = (242, 244, 248)   # #f2f4f8
FG_ALT    = (223, 223, 224)   # #dfdfe0
MUTED     = (151, 153, 155)   # #97999b
BLUE      = (120, 169, 255)   # #78a9ff
CYAN      = (51, 177, 255)    # #33b1ff
TEAL      = (61, 219, 217)    # #3ddbd9
GREEN     = (37, 190, 106)    # #25be6a
PURPLE    = (190, 149, 255)   # #be95ff
RED       = (238, 83, 150)    # #ee5396

W, H = 1280, 640


def find_font(names, size):
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def main():
    repo = sys.argv[1]
    tagline = sys.argv[2]
    out = Path(sys.argv[3])
    art_path = Path(sys.argv[4]) if len(sys.argv) > 4 else None

    swan = None
    if art_path and art_path.exists():
        swan = art_path.read_text(encoding="utf-8")

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # subtle top accent line
    d.rectangle([0, 0, W, 5], fill=TEAL)

    # ===== swan art (render as monospace text — ASCII is text, not blocks) =====
    swan_font = find_font(["cascadiamono.ttf", "cascadiamono-regular.ttf",
                           "consola.ttf", "dejavusansmono.ttf"], 24)
    if swan:
        art_lines = [l.rstrip("\n") for l in swan.splitlines()]
        # measure swan width, scale font so it fits ~460px
        sample = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        max_chars = max(len(l) for l in art_lines)
        line_h = 30
        # fit within 460px wide / ~340px tall
        fs = 24
        while True:
            f = find_font(["cascadiamono.ttf", "cascadiamono-regular.ttf",
                           "consola.ttf", "dejavusansmono.ttf"], fs)
            w = sample.textlength("X" * max_chars, font=f)
            if w <= 460 and fs * len(art_lines) <= 340 or fs <= 10:
                break
            fs -= 2
        f = find_font(["cascadiamono.ttf", "cascadiamono-regular.ttf",
                       "consola.ttf", "dejavusansmono.ttf"], fs)
        line_h = int(fs * 1.25)
        art_w = int(sample.textlength("X" * max_chars, font=f))
        art_h = line_h * len(art_lines)
        ox = 60
        oy = (H - art_h) // 2
        for i, line in enumerate(art_lines):
            d.text((ox, oy + i * line_h), line, font=f, fill=CYAN)
        # vertical divider after art
        d.rectangle([ox + art_w + 40, 90, ox + art_w + 42, H - 90], fill=SURFACE)
        text_x = ox + art_w + 70
    else:
        text_x = 70

    # ===== text =====
    title_font = find_font(["cascadiamono.ttf", "cascadiamono-regular.ttf",
                            "consola.ttf", "dejavusansmono.ttf"], 56)
    tag_font = find_font(["cascadiamono.ttf", "consola.ttf",
                          "dejavusansmono.ttf"], 24)
    small_font = find_font(["cascadiamono.ttf", "consola.ttf",
                            "dejavusansmono.ttf"], 20)

    # repo name
    d.text((text_x, 170), repo, font=title_font, fill=FG)
    # tagline
    d.text((text_x, 260), tagline, font=tag_font, fill=MUTED)
    # bottom-left foot
    d.text((text_x, H - 80), "carbonfox \u00b7 made with hermes", font=small_font, fill=TEAL)

    # little color swatches bottom right
    swatches = [BLUE, CYAN, TEAL, GREEN, PURPLE, RED]
    sw = 22
    gap = 8
    total = len(swatches) * (sw + gap)
    sx = W - 70 - total
    sy = H - 90
    for i, col in enumerate(swatches):
        d.rounded_rectangle([sx + i * (sw + gap), sy, sx + i * (sw + gap) + sw, sy + sw],
                            radius=4, fill=col)

    img.save(out)
    print(f"saved {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
