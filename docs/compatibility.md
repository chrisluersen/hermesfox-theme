# Compatibility evidence — review candidate

**Status: local quality gates pass; VS Code runtime verification is partial; overall cross-surface acceptance remains incomplete.** No live profile was activated. This is not a production-readiness or release claim. Consult GitHub Actions for results on the exact commit; local success does not establish remote CI success.

## Pinned comparison targets

- Pinned stable source: Hermes `v0.21.6`, commit `818c13be1dc4fd28987e1e881a9408224afd4535`.
- Main source snapshot: `4eba3ebed1513d1efe45802f396a11679fff02cf` (an observation, not a claim about future main).
- VS Code tested: `1.136.2`; manifest baseline `^1.136.2`.
- Windows Terminal discovered: packaged `1.24.12741.0`; no isolated runtime acceptance.
- Additional isolation-source inspection: `a62979dc3601c9eae455bff5b35ba8f9bed0df30`, a distinct target from the earlier main snapshot.
- Nerd Fonts installer target: `v3.5.1`; unchanged optional installer already targets it. No fonts were installed.

Source contracts were read from these pinned public references without modifying the installed Hermes checkout. The isolation check evaluated only committed pure path-resolution functions, not application bootstrap or services. The candidate defines all **44** current shared skin color tokens, with no missing/extra entries, and covers the stable Python skin engine's built-in color-key union. This is **source-contract evidence**, not runtime acceptance.

## Per-surface matrix

| Surface | Repository / source evidence | Runtime status and exact missing gate |
|---|---|---|
| Classic CLI | Strict skin parsing, explicit aliases, semantic-role/color checks; actual Rich 14.3.3 markup renders both art variants to the source; stable Python color-key coverage | **Unverified**: clean approved stock launcher, isolated home, real TTY widths 40/80/120, startup, status/diff/completion fixtures and switch-back captures |
| Ink TUI | Main shared-token coverage; main resolver reads supplied aliases; active art remains one span per source row | **Unverified**: clean stock build plus isolated TTY, cold start/restart, hover/focus/diff/tool/reasoning states and switch-back. Historical renderer reports [#129481](https://github.com/NousResearch/hermes-agent/issues/129481) / [#46773](https://github.com/NousResearch/hermes-agent/issues/46773) have independently changing live status; alternate art not activated |
| Dashboard | Separate YAML, strict duplicate-key parsing, mapped hex colors and explicit transparent-glow/layout assertions. Read stable/main normalizer source: it retains `colorOverrides` and `warmGlow`, and accepts all authored override keys | **Unverified**: real isolated `/api/dashboard/themes` roundtrip, picker selection, computed styles, cards/forms/table/code/diff states and rollback. Do not repeat the earlier dropped-fields concern as a confirmed blocker for these snapshots |
| Desktop | Main resolver source consumes `ui_text`/`ui_border` and derives native CSS roles; candidate has every shared color token | **Unverified**: approved clean desktop artifact and proven user-data/home separation from the live instance, JSON-RPC skin readback, startup/controls/state captures and switch-back |
| Windows Terminal | Both distinct scheme names and all schema fields/16 ANSI colors verified as data; legacy scheme hash unchanged | **Unverified**: isolated settings/profile context, actual ANSI/truecolor/glyph/selection/cursor display and profile readback |
| VS Code | Two exact label-to-file contributions, matching workbench exports, complete ANSI colors and immutable legacy files | **Partially verified**: exact maps/token rules, switching/cold restart, all authored CSS variables, hover, editor selection, normal folder-mode status bar and earlier diff/ANSI captures. Terminal text selection, a genuinely disabled menu state, and comprehensive effective-state/accessibility coverage remain incomplete |

## Executed local gates

On Windows with Python **3.11.15**, PyYAML **6.0.3**, Rich **14.3.3**, Ruff **0.15.10** and contained ShellCheck **0.11.0**:

- Ruff lint and formatting checks pass.
- Full repository unit suite passes; exact current count and command outputs are recorded in the final local receipt. Tests include data mutation, strict parsing, legacy hashes, source art/geometry, contrast, provenance, both selector identities, and guarded font fixtures.
- Validator passes as both direct script and package entry point.
- `bash -n`, ShellCheck with `--norc` and all severities, and Git whitespace checks pass. ShellCheck returned zero diagnostics.
- Seven LF-normalized legacy hashes pass. The optional font installer itself is unchanged.
- CI workflow is parsed/contract-tested and action commit references resolve. Linux Python 3.11 and Windows Python 3.14 lanes are configured; consult their actual commit-linked results rather than inferring remote success from configuration or local execution.

## Remaining gates and stopping decision

ShellCheck's earlier missing-tool blocker is resolved. The contained binary ran successfully without changing shared PATH or Python environments. No linter requirement was weakened or skipped.

The inspected Hermes checkout has unrelated modifications and is not proof of a stock build. It was neither reset nor patched. The pinned stable `hermes_constants.py:get_default_hermes_root()` can resolve a nested test `HERMES_HOME` back to the live machine-wide root; read-only evaluation reproduced this collision. No CLI/TUI/dashboard/desktop launch was attempted under that unsafe isolation assumption. Build directories in a modified installation are not clean artifact provenance. Do not spoof roots, weaken guards, patch Hermes or attach to a live backend to obtain a pass.

Stage B was entered for isolated VS Code. Windows Terminal remains untested: only a packaged installation was established, with no qualified separate portable settings context in the scoped inventory. A new live tab/window/profile is not sufficient isolation. Missing evidence is not proof of a theme defect.

The private readiness packet in `.hermes/evidence/` records the concrete local discovery. Before future runtime work, record exact launch/stop commands, stock provenance, separate home/user-data paths, fixture invocations and rollback. Do not guess flags, reuse the live profile, patch Hermes, or automatically restart failed reviewer jobs.

## VS Code observations and corrections

Runtime observations apply to theme revision `4529f3165234f16c8e1fb36f5ee09c1faa9fe63c`. Subsequent review changes harden JSON parsing and update documentation/tests; palettes, exports, artwork and legacy files remain byte-identical to that revision.

- Two contexts were used: an Extension Development Host and a normal window with a passive extension copied into a private extension directory. Neither altered the normal user profile. This is not VSIX or Marketplace acceptance.
- Tokencat's **84** authored colors and token rules matched cached runtime data exactly, as did Carbonfox (Legacy)'s **50** colors and token rules. Switching left no residual Tokencat map entries in legacy. All 84 authored Tokencat CSS-variable values matched before and after cold restart.
- A built-in JSON-setting hover was captured with foreground `rgb(242, 244, 248)` and background `rgb(40, 40, 40)`. This may use default roles rather than authored hover overrides. Editor selection was captured and computed as `rgb(42, 42, 42)`, matching `#2a2a2a`.
- Normal folder-mode status bar computed as background `#0d0d0d`, foreground `#dfdfe0`, including after restart. A later folder-mode screenshot attempt did not complete; this is computed-style evidence.
- A normal no-folder window used fallback `statusBar.noFolderBackground` `#68217a`. The earlier blanket attribution of purple status bars to development-host debugging was not established. No override was added to hide this distinction.
- Earlier captures show diffs, search/menu states and ANSI16. All 16 authored ANSI RGB values were found in the terminal screenshot. The owner approved those seven captures; later hover/selection captures have not received separate visual approval. Neither establishes complete accessibility.
- Terminal-selection input timed out, and subsequent capture transport failed. No genuinely disabled menu entry was established. Neither state is counted as passed; exact CSS-variable equality does not prove every effective component or canvas state.
- Both normal-window process trees and the inspection listener were closed. Fingerprints confirmed approved historical captures, live settings and unrelated Hermes work unchanged. Raw profiles/screenshots/process details/machine paths remain private.

**Corrections:** earlier missing-ShellCheck and no-Stage-B statements were stale; isolated VS Code now has partial runtime evidence. Other-surface gates remain open. Strict JSON now also rejects exponent overflow to infinity, not just nonstandard `NaN`/`Infinity` constants; theme colors did not change.

## Rollback

Carbonfox files remain unchanged and separately selectable. Hermes: keep both skins and choose `carbonfox` (or restore the user's recorded prior skin). Windows Terminal: choose the retained `carbonfox` scheme only for the intended profile. VS Code: choose **Carbonfox (Legacy)**, restoring any explicitly merged customization keys first. Dashboard: restore the exact previous dashboard choice; no legacy dashboard variant exists. No live rollback was needed because only isolated test settings changed.
