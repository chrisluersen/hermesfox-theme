# Banner ASCII Art Archive

Saved pieces Chris likes, so we don't have to re-find them.
Drop any new art you like in here as `.txt` files.

## Space budget (hero column in the TUI banner)
- **Target: 40–50 cols wide × 11–20 rows tall**
- Right column (tools/skills/MCP) takes ~60% of terminal width; hero gets the rest
- Up to ~70 cols on very wide terminals; keep ≤20 tall
- One `[color]…[/]` tag per row when colored (TUI constraint)

## Active pieces (used by the skins)
These are the sources of the banner art embedded in `hermes/skins/*.yaml`:

| File | Size | Role |
|------|------|------|
| `catbox-unboxed-33x11.txt` | 33×11 | `banner_hero` — single-color cat in box |
| `swan-chris-pick.txt` | 54×5 | `banner_logo` — swan (left) + block-font (right) |

## Sources
- **asciiart.eu** — canonical archive, ranked by views. JS-rendered; use web extraction.
- asciiartfarts.com, ascii.co.uk, ascii-art.de, reddit.com/r/ASCII
