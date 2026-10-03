# Changelog

## Unreleased

- Hermes colour roles: blue = chrome, cyan = labels, teal = tool calls, dimmed
  purple = reasoning, gray = passive rules. Syntax and diff colours now follow
  nightfox's own spec (green strings, magenta keywords, tinted diff rows), and
  surfaces follow nvim (statusline bg0, popup sel0/sel1). Added `shell_dollar`.
- Added a two-tone token-cat variant (cat purple→pink, box blue→teal), staged
  until the TUI renders multi-colour banner rows.
- The validator now checks every skin colour against `palette.json` instead of a
  duplicated hardcoded table; pinned roles guard the colour grammar.
- Promoted the active local Carbonfox skin as the canonical distributable skin.
- Documented the active token-cat hero and archived banner-logo artwork.
- Added a dependency-free validator and unit tests for the shipped theme assets.
- Pinned and checksum-verified the optional Nerd Fonts installer.
- Removed generated, duplicate, backup, and stale banner experiments from the release tree.
- Added concise provenance, support boundaries, and non-destructive installation guidance.
