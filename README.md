# hermesfox-theme

A small, portable Carbonfox theme for Hermes and companion applications. The
canonical Hermes artifact is `hermes/skins/carbonfox.yaml`; `palette.json` is
the cross-application color reference. The palette originates from
[EdenEast/nightfox.nvim](https://github.com/EdenEast/nightfox.nvim), licensed
under MIT.

## What is shipped

- `hermes/skins/carbonfox.yaml` — canonical Hermes skin. `banner_hero` is the
  active token-cat artwork. `banner_logo: " "` is a stock-Hermes compatibility
  workaround that suppresses the classic CLI fallback on supported versions;
  it is not a guaranteed cross-renderer hide API. Restart the TUI after
  startup-art changes; palette changes may repaint live.
- `windows-terminal/scheme.json` — a mergeable scheme object.
- `vscode/carbonfox.vscode-theme.json` and
  `vscode/vscode-color-customizations.json` — portable VS Code exports.
- `ascii-art/` — canonical artwork sources; the swan/block lettering is
  archived and not embedded.
- `fonts/install-hack-nerd-font.sh` — optional per-user font installer.

Artwork rights and attribution are documented in [`NOTICE.md`](NOTICE.md). The
repository owner states that verbal permission was granted to use and modify
the active token-cat artwork.

## Safe installation

Back up target files before merging and copy only the artifact needed.

### Hermes

```bash
export HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
mkdir -p "$HERMES_HOME/skins"
curl -fsSL https://raw.githubusercontent.com/chrisluersen/hermesfox-theme/master/hermes/skins/carbonfox.yaml -o "$HERMES_HOME/skins/carbonfox.yaml"
hermes config set display.skin carbonfox
hermes config get display.skin
hermes skin list
```

On Windows Git Bash, use the profile's actual Hermes home if it differs from
`$HOME/.hermes`. Verify the downloaded file before activating it; do not
replace a complete profile or configuration directory.

### Companion applications

- **Windows Terminal:** back up `settings.json`, then merge
  `windows-terminal/scheme.json` into the existing `schemes` array. Do not
  replace the complete settings file or change a profile assignment implicitly.
- **VS Code:** back up User Settings, then merge
  `vscode/vscode-color-customizations.json`, or package the standalone theme in
  an extension. Do not replace complete User Settings.
- WezTerm, Zellij, and Neovim configurations are not shipped; keep personal
  workstation configuration separate.

The optional font script targets Nerd Fonts `v3.5.1`, verifies the pinned
SHA-256 before extraction, installs only Mono TTFs, and reports registry errors.
If registry registration fails, the copied font files remain in the per-user
font directory and can be removed manually before retrying.
Tests use temporary archives and a fake `reg` command; they never touch real
fonts or the Windows registry. It is not required for palette installation.

## Support boundary

| Surface | Status |
|---|---|
| Hermes skin / classic CLI | Supported when the installed Hermes accepts this skin schema; verify with `hermes skin list` |
| Hermes TUI startup art | Supported with the workaround; restart after startup-art changes |
| Windows Terminal scheme | Portable object; merge into existing settings |
| VS Code exports | Merge or package; never replace User Settings |
| WezTerm, Zellij, Neovim | Not shipped; outside support scope |
| Windows / Git Bash | Commands assume `curl`, `mkdir`, and Hermes; adapt the Hermes home path |

## Migration

The retired Carbonfox gist
[`16349ada05bdf04399aa328fd0231184`](https://gist.github.com/16349ada05bdf04399aa328fd0231184)
is superseded by this repository. Install the canonical skin here instead.

## License and provenance

Theme files are MIT-licensed unless a bundled source says otherwise. See
[`NOTICE.md`](NOTICE.md) for the per-artifact rights record. No font binaries
are vendored.
