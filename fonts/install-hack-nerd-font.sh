#!/usr/bin/env bash
# Install Hack Nerd Font Mono (Chris's theme font) on Windows (git-bash / MSYS).
# Downloads the patched font from the official Nerd Fonts GitHub release and
# installs it per-user (no admin needed).
#
# Usage:
#   bash fonts/install-hack-nerd-font.sh
#
# The live configs reference the family name "Hack Nerd Font Mono":
#   - WezTerm:  font = wezterm.font('Hack Nerd Font Mono')
#   - Windows Terminal: "face": "Hack Nerd Font Mono"
#   - VS Code:  editor.fontFamily: "'Hack Nerd Font Mono', ..."
#   - nvim:     (uses the terminal's font)

set -euo pipefail

# Nerd Fonts releases are per-patch: Hack.zip is the Hack Mono/Propo bundle.
# Pin a release tag; "latest" is resolved below via the GitHub API.
RELEASE_TAG="${HACK_NERD_FONT_VERSION:-latest}"

if [ "$RELEASE_TAG" = "latest" ]; then
  RELEASE_TAG="$(curl -fsSL https://api.github.com/repos/ryanoasis/nerd-fonts/releases/latest \
    | grep -o '"tag_name": *"[^"]*"' | head -1 | sed 's/.*"\(.*\)"/\1/')"
fi

echo ">> Downloading Hack Nerd Font $RELEASE_TAG ..."
ZIP="$TMPDIR/hack-nerd-font.zip"
curl -fsSL -o "$ZIP" "https://github.com/ryanoasis/nerd-fonts/releases/download/${RELEASE_TAG}/Hack.zip"

STAGING="$(mktemp -d)"
unzip -qo "$ZIP" -d "$STAGING"

# Per-user font install dir (Windows 10/11, no admin).
FONT_DIR="$LOCALAPPDATA/Microsoft/Windows/Fonts"

# We install the Mono variants (HackNerdFontMono-*.ttf) plus the standard
# HackNerdFont-*.ttf set, mirroring what's live in the user fonts dir.
COUNT=0
for f in "$STAGING"/HackNerdFont*.ttf; do
  [ -e "$f" ] || continue
  cp -f "$f" "$FONT_DIR/"
  COUNT=$((COUNT+1))
done

rm -rf "$STAGING" "$ZIP"
echo ">> Installed $COUNT Hack Nerd Font TTF files into $FONT_DIR"

# Register per-user fonts in the registry so apps pick them up without reboot.
reg add "HKCU\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" \
  /v "Hack Nerd Font Mono (TrueType)" /t REG_SZ \
  /d "HackNerdFontMono-Regular.ttf" /f >/dev/null 2>&1 || true
reg add "HKCU\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" \
  /v "Hack Nerd Font (TrueType)" /t REG_SZ \
  /d "HackNerdFont-Regular.ttf" /f >/dev/null 2>&1 || true

echo ">> Done. Restart your terminal apps to pick up the font."
