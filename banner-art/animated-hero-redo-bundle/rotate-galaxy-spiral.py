"""Generate SPIRAL-OUT galaxy frames for the carbonfox hero.

MOTION: 'spiraling out from the middle' (asciiart.eu 'ASCII Rotating Galaxy'
look) — the core stays anchored and the spiral arms sweep outward around it,
like a pinwheel. This is NOT a rigid rotation of the whole raster.

Implementation:
  * Frame 0 is taken byte-identical from the live skin (the approved still).
  * Each glyph is treated as a point at polar (r, phi) about the center.
  * The rotation phase is DAMPED by radius: no rotation at the very core
    (r < R_CORE), ramping linearly to full phase by R_FULL. So the nucleus is
    anchored and the arms sweep outward. Smooth, no raster banding, no shear.
  * One [hex]...[/] tag per row, colors carried from frame 0, on-palette.
  * 12 frames / 30deg per frame = one smooth 360 loop.

Usage: python3 rotate-galaxy-spiral.py  (writes banner-art/galaxy-spiral-frames.yaml)
"""
import math
import yaml
import os
import re
from pathlib import Path

HERMES_HOME = Path(os.environ.get("HERMES_HOME")
                       or Path.home() / "AppData" / "Local" / "hermes")
SKIN = HERMES_HOME / "skins/carbonfox.yaml"
OUT = HERMES_HOME / "banner-art/galaxy-spiral-frames.yaml"

TAG = re.compile(r"\[(#(?:[0-9a-fA-F]{3,8}))\](.*?)\[/\]")

R_CORE = 2.5   # radius below which the core does not rotate (anchored)
R_FULL = 9.0   # radius at which the arm tips reach the full rotation phase


def parse_frame(frame: str):
    rows = []
    for line in frame.strip().split("\n"):
        line = line.rstrip()
        if not line.strip():
            continue
        content = ""
        cursor = 0
        for m in TAG.finditer(line):
            content += line[cursor:m.start()]
            content += m.group(2)
            cursor = m.end()
        content += line[cursor:]
        rows.append(content)
    W = max(len(r) for r in rows)
    grid = [list(r.ljust(W)) for r in rows]
    return W, grid


def color_map(frame: str):
    cm = {}
    for oy, line in enumerate(frame.strip().split("\n")):
        line = line.rstrip()
        for m in TAG.finditer(line):
            color = m.group(1).lower()
            text = m.group(2)
            start = line.index(text)
            for k, ch in enumerate(text):
                if ch != " ":
                    cm[(start + k, oy)] = color
    return cm


def build_phase_frame(g0, cm, cx, cy, phase_deg, W, H):
    """Re-rasterize the galaxy with radius-damped rotation by phase_deg."""
    theta = math.radians(phase_deg)
    cos, sin = math.cos(theta), math.sin(theta)
    out = [[" " for _ in range(W)] for _ in range(H)]
    for oy in range(H):
        for ox in range(W):
            ch = g0[oy][ox]
            if ch == " ":
                continue
            dx, dy = ox - cx, oy - cy
            r = math.hypot(dx, dy)
            # damping factor: 0 at core, 1 at full radius
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


def frame_to_markup(grid, cm, W):
    rows = []
    for oy in range(len(grid)):
        content = "".join(grid[oy])
        colors = [cm[(x, oy)] for x in range(W)
                  if grid[oy][x] != " " and (x, oy) in cm]
        color = colors[0] if colors else "#7f8489"
        # Emit ALL rows (including empty ones) so every frame keeps the same
        # row count — an empty row renders as spaces inside the tag, keeping
        # the TUI loop from vertically bouncing when a frame loses a row.
        rows.append(f"  [{color}]{content.rstrip()}[/]")
    return "\n".join(rows)


def main():
    data = yaml.safe_load(SKIN.read_text(encoding="utf-8"))
    frames = data["banner_hero_frames"]
    W, g0 = parse_frame(frames[0])
    H = len(g0)
    cx, cy = (W - 1) / 2.0, (H - 1) / 2.0
    cm = color_map(frames[0])

    N_FRAMES = 12
    DEG_STEP = 360.0 / N_FRAMES
    out_frames = [frames[0]]  # frame 0 byte-identical
    for f in range(1, N_FRAMES):
        deg = f * DEG_STEP
        rg = build_phase_frame(g0, cm, cx, cy, deg, W, H)
        out_frames.append(frame_to_markup(rg, cm, W))

    out = yaml.safe_dump(
        {"banner_hero_frames": out_frames},
        allow_unicode=True,
        sort_keys=False,
        default_style="|",
        width=200,
    )
    OUT.write_text(out, encoding="utf-8")
    print(f"Wrote {len(out_frames)} spiral-out frames to {OUT}")
    print(f"frame 0 identical: {out_frames[0] == frames[0]}")


if __name__ == "__main__":
    main()
