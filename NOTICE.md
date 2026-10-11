# NOTICE

This repository distributes the preserved Carbonfox and upgraded Tokencat theme files and the explicitly identified artwork below. Redistribution status is recorded conservatively; an archive page or search result is not treated as a license.

| Path | Description / creator | Stable source | License or permission | Changes | Status |
|---|---|---|---|---|---|
| `palette.json`, `hermes/skins/carbonfox.yaml`, companion theme exports | Carbonfox palette by EdenEast / James Simpson | https://github.com/EdenEast/nightfox.nvim | MIT; preserve the upstream notice | Palette mapped to Hermes and companion formats | Redistributable with this notice |
| `ascii-art/token-cat-29x11.txt`, embedded `banner_hero` | Cat by Hayley Jane Wakenshaw (Flump) | https://asciiart.eu/animals/cats (2014-06-12, 29×11 entry; source id `8c5113000921d06a`) | The repository owner states that verbal permission was granted to use and modify the artwork; no written permission record is included | `hjw` was replaced by `$TOKENS` in the displayed source and the artwork is colored in the Hermes skin | Included under the stated verbal permission; original creator attribution is retained here |
| `ascii-art/swan-banner-logo.txt` | Swan/block-letter artwork created or selected by the repository owner | No external source claimed | Owner-created status is based on repository history/context, not an independent license record | Archived and not embedded | Retained as owner artwork; do not treat as a third-party license |
| `fonts/install-hack-nerd-font.sh` | Installer for Hack Nerd Fonts | https://github.com/ryanoasis/nerd-fonts/releases/tag/v3.5.1 and https://github.com/ryanoasis/nerd-fonts/blob/master/LICENSE | Nerd Fonts source code: MIT; downloaded font files: SIL OFL 1.1 and carry their own license requirements | Downloads, verifies, and installs upstream files; no font binaries are vendored | Script redistributable; downloaded fonts remain governed by upstream licenses |

The former `banner-art/` design archive is intentionally not part of this repository's release surface. Its external and unattributed artwork, generated previews, backups, and patch bundles did not have uniformly established redistribution rights or release value, so they were removed rather than reclassified as licensed.

This file is documentation, not legal advice. If a source does not provide a clear license or direct permission, treat redistribution as blocked.

## Tokencat variant and complete upstream notice

The upgraded `palettes/tokencat.json`, `hermes/skins/tokencat.yaml`, `hermes/dashboard-themes/tokencat.yaml`, `windows-terminal/tokencat.scheme.json`, and `vscode/tokencat*.json` derive from the preserved Carbonfox bundle. The pinned wrapper, adapter, palette and adaptations are documented in [docs/palette.md](docs/palette.md). The complete upstream MIT notice, copyright 2021 James Simpson, is included in [licenses/nightfox-MIT.txt](licenses/nightfox-MIT.txt); upstream-derived material remains subject to it.

The existing token-cat source is shared by both variants without changing its characters or permission status. The alternate two-tone file is valid Rich markup but remains gated for TUI use. This update obtains no new artwork rights and grants no blanket license for original repository material. `vscode/package.json` therefore retains `UNLICENSED`; the local manifest is not Marketplace ownership or publication permission. No font binaries are included.
