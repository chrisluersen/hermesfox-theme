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
| `token-cat-29x11.txt` | 29×11 | **`banner_hero` — the LIVE hero** (2026-09-20). See below |
| `swan-chris-pick.txt` | 54×5 | `banner_logo` — swan (left) + block-font (right) |

## `token-cat` — the live hero (2026-09-20)

- 29×11, Hayley Jane Wakenshaw (`hjw`) — asciiart.eu id `8c5113000921d06a`. The
  artist's initials were removed from the box front and the `$TOKENS` label put in
  their place. Formerly archived here as `catbox-unboxed-33x11.txt`; same art, renamed
  to match the skin's source name (and re-measured: **29 cols** wide).
- **Colouring: one stop per row, violet → teal.** Top row → feet row:
  `#ab7bf0 #9e88fd #9095ff #80a2ff #6fafff #5dbbff #4cc7ff #3ed1ff #3bdbfb #45e3f2
  #57eae8`, interpolated in **OKLab with a lightness ramp (L .680 → .860)** laid over
  the hue sweep.
- **Why a ramp and not a hue sweep.** In this palette blue `#78a9ff`, purple `#be95ff`
  and cyan `#33b1ff` are **luminance-identical** (~.396 rel-lum), so a hue-only gradient
  reads as flat stripes. Ramping perceptual lightness across the same 11 hue steps took
  the rel-lum span from **+0.170 → +0.376** and put the dimmest stop at **5.84:1** on the
  `#161616` background.
- **The criterion, if you re-tune it:** judge a gradient by its **largest single step**,
  never the mean. Max OKLab step ≤ 0.045, dimmest stop ≥ 5.0:1, lightness span ≥ +0.30.
  A wider first ramp looked better on mean deviation and failed all three (max step
  0.0400, dimmest 4.89:1) — a real seam, invisible to the average.
- **Editing constraints (both are real, not cosmetic):** exactly **one `[color]…[/]` tag
  per row** (the TUI parser splits a second tag onto its own line), and any row whose art
  ends in a backslash must end `\ [/]` — one trailing space inside the tag, or Rich reads
  `\[` as an escaped bracket and the CLI prints a literal `[/]`.
- Render: `token-cat-preview.png`.

> **`banner_logo` note (2026-09-20):** the swan + "LUCKY TO HAVE AGENCY" block-font is
> **archived here** as `swan-chris-pick.txt` and is **no longer embedded in the skins** —
> it was taken out of the top banner at the owner's request. The art is kept for reuse:
> re-embedding it means adding a `banner_logo: |` block to `hermes/skins/*.yaml` (like
> `banner_hero`, the key is read **top-level**, not under `branding:`), one `[color]…[/]`
> tag per row.

## Sources
- **asciiart.eu** — canonical archive, ranked by views. JS-rendered; use web extraction.
- asciiartfarts.com, ascii.co.uk, ascii-art.de, reddit.com/r/ASCII
