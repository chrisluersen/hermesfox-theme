# Changelog

## Unreleased

- Added the separately selectable Tokencat upgrade, preserving the Carbonfox
  palette, companion exports and original artwork without changing their bytes.
- Added mapped Hermes/dashboard, Windows Terminal and VS Code upgrade exports,
  strict parsing, provenance and contrast checks, and cross-platform CI.
- Made VS Code selected suggestion text and focused-match colors explicit in
  both upgrade exports; regression tests require AA text contrast in each state.
- Corrected palette documentation and scoped historical runtime evidence;
  cross-surface runtime acceptance remains incomplete.
- Added standalone WezTerm TOML and Zellij modern-role KDL exports, complete
  palette mappings, strict emitted-structure checks and malformed-input coverage.
- Verified changed VS Code suggestion states through switching and cold restart,
  WezTerm native loading/ANSI rendering, and current pure Hermes consumers;
  full app acceptance limits remain explicit in the compatibility matrix.
- Fixed CLI selected completion metadata contrast using the existing darker
  surface token, with emitted-role and optional actual-native style regressions.
- Narrowed VS Code preservation claims to measured files and disclosed that
  existing shared storage was opened without a before-image.
- Restricted emitted KDL RGB digits to ASCII and added WezTerm/Zellij contrast
  coverage with low-contrast foreground counterexamples.

### Retained Carbonfox changes

- Hermes colour roles: blue = chrome, cyan = labels, teal = tool calls, dimmed
  purple = reasoning, gray = passive rules. Syntax and diff colours now follow
  nightfox's own spec (green strings, magenta keywords, tinted diff rows), and
  surfaces follow nvim (statusline bg0, popup sel0/sel1). Added `shell_dollar`.
- Added a two-tone token-cat variant (cat purple→pink, box blue→teal), staged
  until the TUI renders multi-colour banner rows.
- Validation checks Carbonfox against `palette.json` and Tokencat against
  `palettes/tokencat.json`; explicit mappings and pinned roles guard color drift.
- Promoted the active local Carbonfox skin as the canonical distributable skin.
- Documented the active token-cat hero and archived banner-logo artwork.
- Added a validator and unit tests for the shipped theme assets. Current strict
  YAML validation requires PyYAML; Rich is required for artwork-rendering tests.
- Pinned and checksum-verified the optional Nerd Fonts installer.
- Removed generated, duplicate, backup, and stale banner experiments from the release tree.
- Added concise provenance, support boundaries, and non-destructive installation guidance.
