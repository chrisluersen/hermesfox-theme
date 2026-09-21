#!/usr/bin/env python3
"""Generate SPIRAL-OUT frames for an ASCII spiral-galaxy TUI hero.

Matches the asciiart.eu 'ASCII Rotating Galaxy' motion (Injosoft / Elias Wejdin;
rights-reserved — recreate the idea, never copy their code). The galaxy is a
PINWHEEL: the core stays anchored and the spiral arms sweep OUTWARD. It is NOT
a rigid rotation of the whole glyph block.

WHY NOT rigid rotation: a nearest-neighbour raster rotation collapses source
rows into the same output row at non-axis angles, producing horizontal BANDING
that reads as a 3D tumble (a real bug a user flagged: "rotating 3 dimensionally
instead of 2 dimensionally"). Radius-damped point rotation avoids this.

Frame 0 is emitted byte-identical to the source hero. Colors rotate with the
glyphs via a (x,y)->color map carried from frame 0.

Usage:
    python3 rotate-galaxy.py --skin <path.yaml> [--frames 12] [--out <out.yaml>]

Reads `banner_hero_frames[0]` from the skin, writes a fresh YAML containing
only `banner_hero_frames: [ <N frames> ]`. Frame content stays in the clean
skin repo (never upstream).

After generating, RENDER to a contact sheet and vision-verify BEFORE wiring in:
the CORE must not move, the arms must sweep OUTWARD (pinwheel, not a spin), and
no frame may band, melt, or drop a row. Every frame must keep the SAME row
count (emit empty rows as spaces) or the TUI loop bounces vertically.
"""
import argparse
import math
import re
from pathlib import Path

import yaml

TAG = re.compile(r"\[(#(?:[0-9a-fA-F]{3,8}))\](.*?)\[/\]")

# radius below which the core does not rotate (anchored); radius at which the
# arm tips reach the full rotation phase. Tune per artwork.
R_CORE = 2.5
R_FULL = 9.0


def parse_frame(frame: str):
    rows = []
    for line in frame.strip().split("\n"):
        line = line.rstrip()
        if not line.strip():
            continue
        content = ""
        cursor = 0
        for m in TAG.finditer(line):
            content += line[cursor : m.start()]
            content += m.group(2)
            cursor = m.end()
        content += line[cursor:]
        rows.append(content)
    W = max(len(r) for r in rows)
    return W, [list(r.ljust(W)) for r in rows]


def build_phase_frame(grid, cx, cy, phase_deg, W, H):
    """Re-rasterize the galaxy with radius-damped rotation by phase_deg."""
    theta = math.radians(phase_deg)
    cos, sin = math.cos(theta), math.sin(theta)
    out = [[" " for _ in range(W)] for _ in range(H)]
    for oy in range(H):
        for ox in range(W):
            ch = grid[oy][ox]
            if ch == " ":
                continue
            dx, dy = ox - cx, oy - cy
            r = math.hypot(dx, dy)
            if r <= R_CORE:
                damp = 0.0
            elif r >= R_FULL:
                damp = 1.0
            else:
                damp = (r - R_CORE) / (R_FULL - R_CORE)
            a = math.atan2(dy, dx) + damp * theta
            nx = round(cx + r * math.cos(a))
            ny = round(cy + r * math.sin(a))
            if 0 <= nx < W and 0 <= ny < H:
                # don't clobber a core glyph already placed
                if out[ny][nx] == " ":
                    out[ny][nx] = ch
    return out


def frame_to_markup(grid, color_map, W):
    """Glyph grid -> one-tag-per-row markup, colors carried from frame 0.

    Emits ALL rows including empty ones so every frame keeps the same row
    count (a frame that drops a row bounces vertically in the TUI loop).
    """
    rows = []
    for oy in range(len(grid)):
        colors = [
            color_map.get((x, oy))
            for x in range(W)
            if grid[oy][x] != " " and color_map.get((x, oy))
        ]
        color = colors[0] if colors else "#7f8489"
        content = "".join(grid[oy])
        rows.append(f"  [{color}]{content.rstrip()}[/]")
    return "\n".join(rows)


def main():
    ap = argparse.ArgumentParser(description="Generate spiral-out galaxy hero frames")
    ap.add_argument("--skin", required=True, help="path to skin YAML holding banner_hero_frames")
    ap.add_argument("--frames", type=int, default=12, help="total frames (frame 0 reused)")
    ap.add_argument("--out", required=True, help="output YAML path")
    args = ap.parse_args()

    data = yaml.safe_load(Path(args.skin).read_text(encoding="utf-8"))
    frames = data["banner_hero_frames"]
    W0, g0 = parse_frame(frames[0])
    H0 = len(g0)
    cx, cy = (W0 - 1) / 2.0, (H0 - 1) / 2.0

    # color map from frame 0 so colors rotate with the glyphs
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

    deg_step = 360.0 / args.frames
    out_frames = [frames[0]]  # frame 0 byte-identical
    for f in range(1, args.frames):
        rg = build_phase_frame(g0, cx, cy, f * deg_step, W0, H0)
        out_frames.append(frame_to_markup(rg, color_map, W0))

    out = yaml.safe_dump(
        {"banner_hero_frames": out_frames},
        allow_unicode=True, sort_keys=False, default_style="|", width=200,
    )
    Path(args.out).write_text(out, encoding="utf-8")
    print(f"Wrote {len(out_frames)} spiral-out frames to {args.out}")
    print(f"frame 0 identical to source: {out_frames[0] == frames[0]}")
    counts = {f.count("\n") for f in out_frames}
    print(f"uniform row count: {counts == {frames[0].count(chr(10))}} ({sorted(counts)})")


if __name__ == "__main__":
    main()
