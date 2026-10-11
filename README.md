# Tokencat

A Carbonfox-derived dark theme for Hermes and companion apps, with an unchanged **Carbonfox (Legacy)** variant for switching back. The repository remains `chrisluersen/hermesfox-theme`; `tokencat-theme` is a proposed future name, not a completed rename or a publication claim.

This is a local candidate. Repository checks and Rich markup tests are not proof of rendered CLI, Ink TUI, dashboard, desktop, Windows Terminal or VS Code compatibility. See [the per-surface evidence matrix](docs/compatibility.md), [palette lineage](docs/palette.md), [validation](docs/validation.md), and [rights/attribution](NOTICE.md).

## Shipped variants

| Surface | Upgraded Tokencat | Preserved Carbonfox |
|---|---|---|
| Palette | `palettes/tokencat.json` | `palette.json` |
| Hermes CLI / TUI / desktop skin | `hermes/skins/tokencat.yaml`, name `tokencat` | `hermes/skins/carbonfox.yaml`, name `carbonfox` |
| Dashboard | `hermes/dashboard-themes/tokencat.yaml` | No previous dashboard export existed |
| Windows Terminal | `windows-terminal/tokencat.scheme.json`, name `tokencat` | `windows-terminal/scheme.json`, name `carbonfox` |
| VS Code theme | `vscode/tokencat.vscode-theme.json`, label **Tokencat** | `vscode/carbonfox.vscode-theme.json`, label **Carbonfox (Legacy)** |
| VS Code merge fragment | `vscode/tokencat-color-customizations.json` | `vscode/vscode-color-customizations.json` |

`vscode/package.json` contributes both themes in one minimal, code-free local extension. Its declared baseline is VS Code `^1.136.2`; older versions are not claimed supported. Local construction does not establish Marketplace ownership or publishing rights.

All original base values, original exports and the cat sources are hash-guarded against revision `793dcd583c873a7512c6d2a5222d4d0b697f704c`. New aliases and readability overrides exist only in the upgrade. Legacy intentionally retains its previous visual limitations; rollback does not mean it has passed new contrast targets.

## Safe installation and rollback — only when separately authorized

No app was activated as part of building this candidate. First validate the exact app/version in an isolated context. Back up only the target files/keys, record prior selections, and never replace a whole profile, `config.yaml`, VS Code User Settings, or Windows Terminal `settings.json`. Use artifacts from the reviewed local checkout; the new files are not yet available from the public default branch.

### Hermes CLI, TUI and desktop

1. Explicitly identify the target Hermes home; do not assume `~/.hermes` on Windows or change another profile. Back up any existing `skins/tokencat.yaml`, `skins/carbonfox.yaml`, and the prior `display.skin` value.
2. Copy the two repository skin files into that home's `skins` directory. Keep both names. Do not overwrite an existing customized file without preserving it.
3. After authorization, in a shell with `TARGET_HERMES_HOME` explicitly set, use the supported writer:

```bash
: "${TARGET_HERMES_HOME:?Choose the explicit approved target home first}"
env HERMES_HOME="$TARGET_HERMES_HOME" hermes skin list
env HERMES_HOME="$TARGET_HERMES_HOME" hermes config set display.skin tokencat
env HERMES_HOME="$TARGET_HERMES_HOME" hermes config get display.skin
```

Verify the actual CLI, TUI and desktop independently. Desktop Appearance may have its own selection flow; shared skin parsing alone is not proof that it rendered. Keep the active single-span-per-row token-cat. `banner_logo: " "` is a renderer workaround, not a general hide API; startup artwork may require a restart. Do not enable the alternate two-tone cat until its exact TUI renderer passes the documented gate.

Switch back to the retained Carbonfox selection when desired:

```bash
: "${TARGET_HERMES_HOME:?Choose the explicit approved target home first}"
env HERMES_HOME="$TARGET_HERMES_HOME" hermes config set display.skin carbonfox
env HERMES_HOME="$TARGET_HERMES_HOME" hermes config get display.skin
```

For complete rollback, restore the recorded prior selection (which may not have been Carbonfox) and only the specific overwritten files from the backup. No Hermes source patch or plugin is needed or supplied.

### Dashboard — a separate format and selection

Copy `hermes/dashboard-themes/tokencat.yaml` to the explicitly selected home's `dashboard-themes` directory only after authorization. Refresh and choose **Tokencat** in the dashboard theme picker. Verify `/api/dashboard/themes` and the browser's computed colors: a backend that drops `colorOverrides` or `palette.warmGlow` blocks full-fidelity acceptance. Merely seeing a named theme in the picker is insufficient.

The skin file in `skins/` does not theme the dashboard. Roll back to the exact previous dashboard selection; no legacy Carbonfox dashboard entry is promised. This artifact ships no CSS injection, remote fonts, external assets or dashboard plugin, and does not invent a token-cat slot.

### Windows Terminal

Back up the settings file, then merge both scheme objects into its existing `schemes` array **by unique name**. Do not replace the whole array or create duplicate names. Change only the intended profile's `colorScheme`: `tokencat` for the upgrade, `carbonfox` for legacy. Verify all 16 ANSI colors, truecolor, selection/cursor and glyphs in that profile. For full rollback restore its prior `colorScheme` and only keys changed by the merge. No font change is required.

### VS Code

Prefer the supplied theme-only extension manifest in an isolated Extension Development Host with fresh user-data/extensions directories. Select **Tokencat**, **Carbonfox (Legacy)**, then **Tokencat**, and verify the actual workbench, syntax, diff, status bar and integrated terminal states.

Alternatively, merge the selected `*-color-customizations.json` fragment into a backed-up settings object. Merge the two named customization objects, preserving unrelated existing keys. Explicit customization keys override a selected theme, so selecting Carbonfox alone will not undo a Tokencat merge: restore the recorded prior values (or remove only keys that did not exist before). Do not replace complete User Settings or assume the generated fragment is a comment-bearing JSONC parser.

## Artwork, optional fonts and scope

Both skins share the unchanged 29×11 token-cat from [ascii-art](ascii-art/README.md). The owner reports verbal permission to use/modify Hayley Jane Wakenshaw's artwork; see [NOTICE](NOTICE.md). An Internet archive is not a blanket redistribution license.

`fonts/install-hack-nerd-font.sh` remains optional and unchanged. It targets Nerd Fonts `v3.5.1`, verifies its pinned digest before extraction, and installs only Mono TTFs. Do not run it merely to use the palette. If registry registration fails, copied fonts remain and require deliberate recovery. The test suite uses temporary supplied ZIPs and a fail-closed fake-`reg` guard; it never invokes real registration or downloads fonts.

WezTerm, Zellij and Neovim configurations are not shipped or claimed supported. The retired gist [`16349ada05bdf04399aa328fd0231184`](https://gist.github.com/16349ada05bdf04399aa328fd0231184) is historical; it does not supply the new variant or a migration for whole workstation settings.

## Rights

No blanket license is granted for original repository material. Upstream-derived Nightfox material retains its [complete MIT notice](licenses/nightfox-MIT.txt). The local VS Code package remains `UNLICENSED`; no font binaries are vendored. See [NOTICE.md](NOTICE.md) for the unchanged artwork permission boundary.
