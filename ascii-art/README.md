# Canonical artwork

`ascii-art/` contains the artwork referenced by the portable theme or retained
as explicit archive material:

| File | Role | Provenance |
|---|---|---|
| `token-cat-29x11.txt` | Active `banner_hero` | Hayley Jane Wakenshaw (Flump), ASCII Art Archive entry `8c5113000921d06a`; repository owner states verbal permission was granted — see `NOTICE.md` |
| `token-cat-two-tone.rich.txt` | Gated `banner_hero` candidate: cat purple→pink, box blue→teal; enable once the TUI keeps multi-colour rows intact | Same token-cat artwork |
| `swan-banner-logo.txt` | Archived `banner_logo` artwork | Retained as owner artwork; not embedded in the skin |

The active token-cat source is preserved because it is the current appearance;
the repository owner states that verbal permission was granted to use and
modify it. Do not add artwork from public galleries without recording a license
or direct permission first.

The former `banner-art/` experiment archive was removed from the repository. It
contained generated previews, duplicate copies, backups, stale patch bundles,
and unattributed or uncertain experiments that were not needed to install or
verify the theme.

## Renderer evidence and limits

Both `carbonfox` (legacy) and `tokencat` embed the unchanged single-span-per-row cat; their source hashes are tested. Rich 14.3.3 renders the active and alternate markup to the exact 11-row, maximum-29-column source, including backslashes and `$TOKENS`. Tests check escaped bracket handling and preserve the one-space logo workaround.

Rich success does not prove Ink/TUI row parsing, narrow-terminal layout or desktop startup behavior. [Issue #129481](https://github.com/NousResearch/hermes-agent/issues/129481) and [issue #46773](https://github.com/NousResearch/hermes-agent/issues/46773) remained open at the candidate audit. Keep the two-tone art opt-in and unactivated until the exact stock renderer passes. Restart after startup-art changes; do not promise hot reload. The dashboard has no documented token-cat hero slot, so this bundle adds no CSS or plugin to invent one.
