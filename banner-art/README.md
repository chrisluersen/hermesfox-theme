# Banner ASCII Art Archive

Saved pieces Chris likes, so we don't have to re-find them.
Drop any new art you like in here as `.txt` files.

## Space budget (hero column in the TUI banner)
- **Target: 40–50 cols wide × 11–20 rows tall**
- Right column (tools/skills/MCP) takes ~60% of terminal width; hero gets the rest
- Up to ~70 cols on very wide terminals; keep ≤20 tall
- One `[color]…[/]` tag per row when colored (TUI constraint)

## token-cat — the live hero (2026-09-20)

- **Name: `token-cat`.** 29×11, Hayley Jane Wakenshaw (Flump) — asciiart.eu id
  `8c5113000921d06a`. Artist initials `hjw` removed from the box front; the
  `$TOKENS` label sits in their place.
- Files: `token-cat-29x11.txt` (source art) · `token-cat-web-source-raw.txt`
  (verbatim web extract, identical md5) · `token-cat-design.py` (row plan) ·
  `token-cat-preview.png` (current colourful render).
- **Live coloring (owner's call, 2026-09-20 — supersedes the per-element map): a hue
  gradient, one stop per row, violet → teal.** Top row → feet row:
  `#ab7bf0 #9e88fd #9095ff #80a2ff #6fafff #5dbbff #4cc7ff #3ed1ff #3bdbfb #45e3f2
  #57eae8`. Interpolated in **OKLab**, with a **lightness ramp laid over the hue
  sweep** (perceptual L .680 → .860).
- **Why the ramp is the whole point (measured).** The first gradient attempt swept
  hue at *constant* lightness — the owner's screenshot labels every swatch "L0", and
  the stops really did land flat: the first seven sit inside rel-lum **.3900–.3966**
  (a spread of 0.007 — no perceptible ordering), and only the last four rise, to
  .5666. In this palette blue `#78a9ff` .396, purple `#be95ff` .397 and cyan
  `#33b1ff` .394 are **luminance-identical** (only teal `#3ddbd9` .567 separates), so
  a hue-only sweep reads as **flat stripes, not shading**. Ramping perceptual
  lightness across the same 11 hue steps took the rel-lum span from **+0.170 →
  +0.376** and put the dimmest stop at **5.84:1** on the `#16161e` terminal
  background. Re-tune or invert the direction by changing the two lightness
  endpoints. **How the live ramp was chosen, honestly (2026-09-20):** a wider first
  ramp (L .635 → .868, stops starting `#9d6de1`) was shipped, then rejected on
  review — an independent reviewer *and* a vision pass both flagged its top as too
  dim, and re-measuring agreed: its largest single OKLab step was **0.0400** and its
  dimmest stop only **4.89:1**, the floor of legibility. So the criterion was
  formalised — **max single step ≤ 0.045, dimmest stop ≥ 5.0:1, span ≥ +0.30** — and
  the live ramp wins it outright: max step **0.0368**, dimmest stop **5.84:1**, span
  **+0.3758**. The rejected ramp is kept for comparison in
  `token-cat-gradient-final.png`; `token-cat-gradient-candidates.png` has all five.
  **Mean ΔE deviation is the wrong test** — it calls the rejected ramp the "most
  even" of the five while the seam a viewer sees is the *largest* step. Test the max.
- **Live render:** `token-cat-preview.png`. Three-way comparison
  (`token-cat-gradient.png`): per-element → hue-only attempt → this one.
- **Superseded — do not restore unless the owner asks: the per-element map** (cat
  purple `#be95ff` / box blue `#78a9ff` / feet cyan `#33b1ff` / `$TOKENS` teal
  `#3ddbd9`). It absorbed five owner corrections on 2026-09-20 and is kept **only**
  because the region argument it settled is still the record of what is cat and what
  is box. Red `#ee5396`, green `#25be6a` and white `#f2f4f8` were removed on request
  — do not reintroduce them.
- **HISTORICAL region map (superseded by the gradient on 2026-09-20; still the record
  of what is cat and what is box).**
  **THE REGION MAP IS OWNER-WORDED — DO NOT RE-DERIVE IT FROM THE GLYPHS.**
  On 2026-09-20 I got it wrong three times: a left/right split ("half of the cat is
  blue"), then two mutually contradictory vision reads of the ASCII, then a
  head-hump reading. The owner's own wording settled it:
  *"the very bottom straight line is still the box, the cat is also the triangle at
  the end of the curve as well as the other marks following the curve above the
  square"* —
  **the BOX+LID is the right structure**: front face, the bottom straight line
  (r10 c12-23), the walls (cols 24-28), the lid flaps (cols 22-28, rows 1-4), and
  the box's top edge `,-'` at r8 c12-14, which sits level with the cat's arm.
  **The TORSO IS THE CAT** — rows 5-7 hold the cat's own outline (`,`, `,'-`----Y`,
  `;`), so they are purple. He corrected this explicitly ("the cat belly … is blue
  right now"): an earlier revision pushed the box boundary left through rows 5-7
  and swallowed the belly. Per-row cut `{1:22, 2:22, 3:22, 4:22, 5:26, 6:26, 7:24,
  8:12, 9:14, 10:11}`, label split out on r9. **Everything else is the CAT** — left
  silhouette, head, back, torso, inner line. Row 11 is the feet band.
  **If the map ever needs re-deriving: do not read the glyphs, do not trust a
  vision model on ASCII art, and do not guess a fourth time.** Render each candidate
  region in a loud diagnostic colour with a column ruler (`token-cat-regions.png`,
  `token-cat-leftflank.png` are the ones that worked) and ask the owner to point.
- **Multi-colour rows require the row-preserving TUI parser.** `ui-tui/src/banner.ts`
  `parseRichRows()` returns one row per line with every colour run inside it, and
  `ArtLines` renders one `<Text>` per row with nested `<Text>` per run.
  `parseRichMarkup()` is now the flat legacy view (`parseRichRows().flat()`) — it
  is fine for a run list, but anything that RENDERS lines must use `parseRichRows`,
  because the flat shape makes each run its own row (23 entries for this 11-row
  hero). That is a local patch to the checkout: `hermes update` will offer to
  stash it.
- Candidate sheets kept for reference: `token-cat-vibe-options.png` (gradient vs
  structural options), `token-cat-final3-candidates.png` (4-hue options),
  `token-cat-multicolor-candidates.png` (7-hue, pre-removal),
  `token-cat-accent-candidate.png`, `token-cat-legacy-cyan-preview.png`.
- **A single fixed split column does not work on this art — per-row splits do.**
  The cat/box boundary wanders (col 5 on row 1, col 9 on row 3, col 3 on row 7),
  and one column seam at col 18 sliced `$TOKENS` into `$TOK` / `ENS` and cut the
  box roof and floor mid-run. The live scheme instead splits **per row**, at
  boundaries chosen to land on space runs, and splits the `$TOKENS` row three
  ways (cat | box wall | `$TOKENS` | box wall) so the label is never cut.
- **Rows that end in a backslash carry one trailing space before the closing
  tag.** Rich reads `\[` as an escaped bracket, so `… / \[/]` prints a literal
  `[/]` in the CLI (the TUI regex is immune). The trailing space is invisible in
  both and is what keeps the CLI clean.

## Files (measured 2026-08-14)
| File | Size | Views | Note |
|------|------|-------|------|
| `token-cat-29x11.txt` | 29×11 | — | **The live hero.** See above |
| `swan-chris-pick.txt` | 54×5 | — | Chris's earlier pick (was the banner_logo) |
| `two-love-birds-jgs-37x10.txt` | 37×10 | 1,664 | jgs classic, fits well |
| `two-birds-reading-jgs-52x16.txt` | 46×16 | 448 | jgs, fits on wide terminals |
| `goose-shanaka-28x13.txt` | 28×13* | 346 | Shanaka Dias |
| `swan-asciiart-46x18.txt` | 46×18* | 212 | asciiart.eu swan |

\* Leading whitespace was stripped by web extraction — re-pad before use.

## Sources
- **asciiart.eu** — canonical archive, ranked by views. JS-rendered; use web extraction.
- asciiartfarts.com, ascii.co.uk, ascii-art.de, reddit.com/r/ASCII
