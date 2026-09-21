"""Render the spiral-out galaxy frames to a contact sheet for vision QA.

Strips [hex]...[/] tags, draws each frame at a fixed glyph cell size so the
full 12-frame rotation is visible on one sheet. Writes banner-art/galaxy-spiral-sheet.png
"""
import yaml
import os
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERMES_HOME = Path(os.environ.get("HERMES_HOME")
                       or Path.home() / "AppData" / "Local" / "hermes")
SRC = HERMES_HOME / "banner-art/galaxy-spiral-frames.yaml"
OUT = HERMES_HOME / "banner-art/galaxy-spiral-sheet.png"

data = yaml.safe_load(SRC.read_text(encoding="utf-8"))
frames = data["banner_hero_frames"]

TAG = re.compile(r"\[#[0-9a-fA-F]{3,8}\]|\[/\]")


def plain(f: str) -> list[str]:
    return [re.sub(TAG, "", line).rstrip("\n") for line in f.strip().split("\n")]


rows = [plain(f) for f in frames]
H = len(rows[0])
W = max(len(r) for r in rows[0] for rows_ in [rows] for r in rows[0])

# try a monospace font, fall back to default
try:
    font = ImageFont.truetype("C:/Windows/Fonts/Consolas.ttf", 20)
except Exception:
    font = ImageFont.load_default()

cell = 20
pad = 24
cols = 6
n = len(frames)
grid_cols = min(cols, n)
grid_rows = (n + grid_cols - 1) // grid_cols
sheet_w = grid_cols * (W * cell + pad) + pad
sheet_h = grid_rows * (H * cell + pad) + pad

img = Image.new("RGB", (sheet_w, sheet_h), "#161616")
draw = ImageDraw.Draw(img)

for i, rows_i in enumerate(rows):
    gx = i % grid_cols
    gy = i // grid_cols
    x0 = pad + gx * (W * cell + pad)
    y0 = pad + gy * (H * cell + pad)
    draw.text((x0, y0), f"f{i}", fill="#f2f4f8", font=font)
    for r, line in enumerate(rows_i):
        for c, ch in enumerate(line):
            if ch != " ":
                draw.text((x0 + c * cell, y0 + (r + 1) * cell), ch, fill="#78a9ff", font=font)

img.save(OUT)
print(f"wrote {OUT} ({sheet_w}x{sheet_h})")
