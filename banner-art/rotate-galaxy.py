"""Generate true ROTATION frames for the carbonfox galaxy hero.

Frame 0 is taken byte-identical from the current carbonfox.yaml hero (which
matches the asciiart.eu 'ASCII Rotating Galaxy' still). Subsequent frames
rotate the whole galaxy about its center by successive angles, re-rasterizing
the glyph grid so each frame is a genuine rotation (spiral arms sweep), NOT a
vertical scroll.

Each output row keeps the ONE [hex]...[/] tag per row convention and stays on
the carbonfox palette. Frame 0 is emitted unchanged.

Usage: python3 rotate-galaxy.py  (writes banner-art/galaxy-rotate-frames.yaml)
"""
import math
import yaml
import os
import re
from pathlib import Path

HERMES_HOME = Path(os.environ.get("HERMES_HOME")
                       or Path.home() / "AppData" / "Local" / "hermes")
SKIN = HERMES_HOME / "skins/carbonfox.yaml"
OUT = HERMES_HOME / "banner-art/galaxy-rotate-frames.yaml"

TAG = re.compile(r"\[(#(?:[0-9a-fA-F]{3,8}))\](.*?)\[/\]")


def parse_frame(frame: str):
    """Return (W, rows) where rows is list of (list[(color,glyph)], content_width)."""
    rows = []
    for line in frame.strip().split("\n"):
        line = line.rstrip()
        if not line.strip():
            continue
        # build a full-width grid (content) by filling with spaces
        segs = []
        cursor = 0
        content = ""
        for m in TAG.finditer(line):
            content += line[cursor : m.start()]
            content += m.group(2)
            cursor = m.end()
        content += line[cursor:]
        rows.append(content)
    W = max(len(r) for r in rows)
    # pad to uniform width
    grid = [list(r.ljust(W)) for r in rows]
    return W, grid


def rotate_grid(grid, cx, cy, deg):
    """Rotate a 2D glyph grid about (cx,cy) by deg degrees clockwise.

    Nearest-neighbour inverse mapping. Empty cells (space) map to space.
    Returns a new grid of the same shape.
    """
    H = len(grid)
    W = len(grid[0])
    theta = math.radians(deg)
    cos, sin = math.cos(theta), math.sin(theta)
    out = [[" " for _ in range(W)] for _ in range(H)]
    for oy in range(H):
        for ox in range(W):
            # inverse rotate output point -> source point
            dx, dy = ox - cx, oy - cy
            sx = cx + dx * cos + dy * sin
            sy = cy - dx * sin + dy * cos
            ix, iy = int(round(sx)), int(round(sy))
            if 0 <= ix < W and 0 <= iy < H:
                out[oy][ox] = grid[iy][ix]
    return out


def frame_to_markup(grid, color_map):
    """Convert a glyph grid back to one-tag-per-row markup.

    color_map: {(x,y): color} from frame 0 so colors rotate with the glyphs.
    Each row gets ONE [color]...[/] tag wrapping the whole non-empty row.
    """
    H = len(grid)
    W = len(grid[0])
    rows = []
    for oy in range(H):
        content = "".join(grid[oy])
        # color: majority non-space color in this row from color_map
        colors = [color_map.get((x, oy)) for x in range(W) if grid[oy][x] != " "]
        colors = [c for c in colors if c]
        color = colors[0] if colors else "#7f8489"
        rows.append(f"  [{color}]{content.rstrip()}[/]")
    return "\n".join(rows)


def main():
    data = yaml.safe_load(SKIN.read_text(encoding="utf-8"))
    frames = data["banner_hero_frames"]
    W0, g0 = parse_frame(frames[0])

    H0 = len(g0)
    cx, cy = (W0 - 1) / 2.0, (H0 - 1) / 2.0

    # Build color map from frame 0 (which glyph is what color)
    color_map = {}
    for oy, line in enumerate(frames[0].strip().split("\n")):
        line = line.rstrip()
        for m in TAG.finditer(line):
            color = m.group(1).lower()
            text = m.group(2)
            start = line.index(text)
            for k, ch in enumerate(text):
                if ch != " ":
                    color_map[(start + k, oy)] = color

    # Frame 0 is emitted unchanged; generate rotation frames.
    # 12 frames over 360deg -> 30deg steps gives a smooth sweep.
    N_FRAMES = 12
    DEG_STEP = 360.0 / N_FRAMES
    out_frames = [frames[0]]  # frame 0 byte-identical
    for f in range(1, N_FRAMES):
        deg = f * DEG_STEP
        rg = rotate_grid(g0, cx, cy, deg)
        out_frames.append(frame_to_markup(rg, color_map))

    # Emit as YAML (mirror the existing structure)
    out = yaml.safe_dump(
        {"banner_hero_frames": out_frames},
        allow_unicode=True,
        sort_keys=False,
        default_style="|",
        width=200,
    )
    OUT.write_text(out, encoding="utf-8")
    print(f"Wrote {len(out_frames)} frames ({N_FRAMES}-step rotation) to {OUT}")
    print(f"frame 0 identical: {out_frames[0] == frames[0]}")


if __name__ == "__main__":
    main()
