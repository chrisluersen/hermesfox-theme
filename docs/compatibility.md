# Compatibility evidence — local candidate

**Status: implementation candidate; Stage A quality gate still blocked by unavailable ShellCheck. Stage B was not entered.** No application was activated, no stock-runtime installation was created, and no GitHub Actions run was dispatched. The repository branch and exact candidate SHA are in the local closeout receipt; this page does not claim publication.

## Pinned comparison targets

- Latest stable observed: Hermes `v0.21.6`, commit `818c13be1dc4fd28987e1e881a9408224afd4535`.
- Main source snapshot: `4eba3ebed1513d1efe45802f396a11679fff02cf` (an observation, not a claim about future main).
- Installed VS Code discovered: `1.136.2`; manifest baseline `^1.136.2`.
- Nerd Fonts latest observed: `v3.5.1`; unchanged optional installer already targets it. No fonts were installed.

Source files were read from these pinned public references without executing them or modifying the installed Hermes checkout. The candidate defines all **44** current shared skin color tokens, with no missing/extra entries, and covers the stable Python skin engine's built-in color-key union. This is **source-contract evidence**, not runtime acceptance.

## Per-surface matrix

| Surface | Repository / source evidence | Runtime status and exact missing gate |
|---|---|---|
| Classic CLI | Strict skin parsing, explicit aliases, semantic-role/color checks; actual Rich 14.3.3 markup renders both art variants to the source; stable Python color-key coverage | **Unverified**: clean approved stock launcher, isolated home, real TTY widths 40/80/120, startup, status/diff/completion fixtures and switch-back captures |
| Ink TUI | Main shared-token coverage; main resolver reads supplied aliases; active art remains one span per source row | **Unverified**: clean stock build plus isolated TTY, cold start/restart, hover/focus/diff/tool/reasoning states and switch-back. Two-tone issues [#129481](https://github.com/NousResearch/hermes-agent/issues/129481) / [#46773](https://github.com/NousResearch/hermes-agent/issues/46773) remain open; alternate art not activated |
| Dashboard | Separate YAML, strict duplicate-key parsing, mapped hex colors and explicit transparent-glow/layout assertions. Read stable/main normalizer source: it retains `colorOverrides` and `warmGlow`, and accepts all authored override keys | **Unverified**: real isolated `/api/dashboard/themes` roundtrip, picker selection, computed styles, cards/forms/table/code/diff states and rollback. Do not repeat the earlier dropped-fields concern as a confirmed blocker for these snapshots |
| Desktop | Main resolver source consumes `ui_text`/`ui_border` and derives native CSS roles; candidate has every shared color token | **Unverified**: approved clean desktop artifact and proven user-data/home separation from the live instance, JSON-RPC skin readback, startup/controls/state captures and switch-back |
| Windows Terminal | Both distinct scheme names and all schema fields/16 ANSI colors verified as data; legacy scheme hash unchanged | **Unverified**: isolated settings/profile context, actual ANSI/truecolor/glyph/selection/cursor display and profile readback |
| VS Code | Two exact label-to-file contributions, matching workbench exports, complete ANSI colors and immutable legacy files; installed version discovered | **Unverified**: fresh Extension Development Host user-data/extensions contexts, full workbench/syntax/diff/state captures, no residual overrides on switch-back |

## Executed local gates

On Windows with Python **3.11.15**, PyYAML **6.0.3**, Rich **14.3.3** and existing Ruff **0.15.10**:

- Ruff lint and formatting checks pass.
- Full repository unit suite passes; exact current count and command outputs are recorded in the final local receipt. Tests include data mutation, strict parsing, legacy hashes, source art/geometry, contrast, provenance, both selector identities, and guarded font fixtures.
- Validator passes as both direct script and package entry point.
- `bash -n` and Git whitespace checks pass. These do not substitute for ShellCheck.
- Seven LF-normalized legacy hashes pass. The optional font installer itself is unchanged.
- CI workflow is parsed/contract-tested and action commit references resolve. Linux Python 3.11 and Windows Python 3.14 lanes are **configured, not executed**.

## Remaining gates and stopping decision

ShellCheck is not installed/on PATH or present in the searched existing tool locations. Installation was prohibited, so its warning/error gate remains blocked. No linter requirement was weakened or skipped in CI to hide this.

The inspected installed Hermes checkout has unrelated modifications and is not proof of an unmodified stock build. It was neither reset nor patched. No approved, already-isolated desktop/dashboard acceptance context was established. Because the Stage A gate is incomplete, no Stage B app launch was attempted, including VS Code or Windows Terminal. Do not infer that a missing capture proves an app defect; these are acceptance gaps.

The private readiness packet in `.hermes/evidence/` records the concrete local discovery. Before future runtime work, record exact launch/stop commands, stock provenance, separate home/user-data paths, fixture invocations and rollback. Do not guess flags, reuse the live profile, patch Hermes, or automatically restart failed reviewer jobs.

## Rollback

Carbonfox files remain unchanged and separately selectable. Hermes: keep both skins and choose `carbonfox` (or restore the user's recorded prior skin). Windows Terminal: choose the retained `carbonfox` scheme only for the intended profile. VS Code: choose **Carbonfox (Legacy)**, restoring any explicitly merged customization keys first. Dashboard: restore the exact previous dashboard choice; no legacy dashboard variant exists. No live rollback is currently needed because no app settings changed.
