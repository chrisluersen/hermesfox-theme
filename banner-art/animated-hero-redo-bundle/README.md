# Animated Galaxy Hero — Redo Bundle

Packed 2026-08-14 when the animated-hero experiment was reverted (user chose to
go back to the static single-color cat-in-box). Everything needed to redo the
animated spiral-out galaxy hero lives here.

## What this bundle contains

| File | Purpose |
|------|---------|
| `upstream-diff-7-files.patch` | The full upstream working-tree diff for the 7 TUI animation files. Apply with `git apply` in `hermes-agent/` to restore the animated-hero seam (frames plumbing + TUI loop). |
| `galaxy-spiral-frames.yaml` | The GOOD 12-frame spiral-out frames (radius-damped pinwheel, uniform 19 rows, 0 banding). This is what went into the skin. |
| `galaxy-rotate-frames.yaml` | The SUPERSEDED 12-frame rigid-rotation frames (banding-prone). Do NOT use — kept for reference. |
| `rotate-galaxy-spiral.py` | The GOOD generator: radius-damped point rotation (core anchored, arms sweep outward). |
| `rotate-galaxy.py` | The SUPERSEDED rigid nearest-neighbour rotation (caused banding / "3D tumble"). Do NOT use. |
| `render-spiral-sheet.py` | Renders frames to a contact sheet for vision QA. |
| `galaxy-spiral-sheet.png` | Vision-verified contact sheet (core fixed across all 12 frames, pinwheel motion). |
| `galaxy-rotate-sheet.png` / `galaxy-rotate-live-sheet.png` | Superseded rigid-rotation sheets (banding visible). |
| `carbonfox-backup-before-spiral.yaml` | The live skin just before the spiral swap (backup reference). |

## How to redo (if wanted later)

1. **Restore the TUI seam** (upstream, 7 files):
   ```
   cd $HERMES_HOME\hermes-agent
   git apply $HERMES_HOME\banner-art\animated-hero-redo-bundle\upstream-diff-7-files.patch
   ```
   These files were: `apps/shared/src/skin.ts`, `hermes_cli/skin_engine.py`,
   `tui_gateway/server.py`, `ui-tui/src/app/createGatewayEventHandler.ts`,
   `ui-tui/src/banner.ts`, `ui-tui/src/components/branding.tsx`,
   `ui-tui/src/theme.ts`. Re-applying dirties upstream again — the update-time
   "restore local changes?" prompt (git stash pop) is expected and yes = keep.

2. **Swap the frames into the skin** (clean local repo, no upstream):
   Replace the top-level `banner_hero_frames:` list in `skins/carbonfox.yaml`
   with `galaxy-spiral-frames.yaml`. Frame content stays in the skin, never
   upstream.

3. **Verify** — ad-hoc script pattern in the skill
   `hermes-banner-hero-customization` → `references/hero-animation.md` (12
   frames, uniform rows, 1 tag/row, on-palette, frame0 byte-identical, CLI+TUI
   both serve 12). The packaged generator is
   `skills/hermes/hermes-banner-hero-customization/scripts/rotate-galaxy.py`
   (already updated to the spiral-out version).

## Key facts (so you don't re-derive them)

- **HERO_TICK_MS = 240** in `ui-tui/src/components/branding.tsx` (12 frames ≈
  2.9s/full loop). 160 was too fast.
- **Right motion = pinwheel** (radius-damped: core r<2.5 anchored, arms reach
  full phase by r>=9.0). Rigid rotation of the glyph block banded rows → looked
  like a 3D tumble. That's the bug the user rejected.
- **Every frame MUST keep the same row count** (emit empty rows as spaces) or
  the TUI loop bounces vertically.
- **Frame 0 must stay byte-identical** to the approved static hero.
- **Palette**: carbonfox only — bg `#161616`, `#7f8489`, `#78a9ff`, `#33b1ff`,
  `#3ddbd9`, `#be95ff`. One `[hex]…[/]` tag per row, never per cell.
- **Hero budget**: 40–50 cols × 11–20 rows, never exceed 20 rows.
- **Injosoft rights**: the asciiart.eu Rotating Galaxy idea is recreatable, but
  their code/art is rights-reserved — generate original frames.

## Decision history

- Rigid rotation first → banding → user: "rotating 3 dimensionally instead of 2
  dimensionally". Rebuilt as spiral-out pinwheel → vision-verified good.
- User ultimately chose to revert to the static single-color cat-in-box and
  remove the dirty upstream files. This bundle preserves the option to redo.
