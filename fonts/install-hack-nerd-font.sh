#!/usr/bin/env bash
# Install Hack Nerd Font Mono per-user on Windows (git-bash / MSYS).
set -euo pipefail

RELEASE_TAG="${HACK_NERD_FONT_VERSION:-v3.5.1}"
EXPECTED_SHA256="${HACK_NERD_FONT_SHA256:-fa24da7de7cefe7766614d27762570b20453c852fc1d5b657111666df9a5e449}"
DOWNLOAD_DIR="${TMPDIR:-${TEMP:-.}}"
ZIP="${HACK_NERD_FONT_ZIP:-$DOWNLOAD_DIR/hack-nerd-font-$RELEASE_TAG.zip}"
STAGING=""
FONT_DIR="${FONT_DIR:-$LOCALAPPDATA/Microsoft/Windows/Fonts}"

cleanup() {
  [ -n "$STAGING" ] && rm -rf "$STAGING"
  [ -n "${HACK_NERD_FONT_ZIP:-}" ] || rm -f "$ZIP"
}
trap cleanup EXIT

if [ -z "${HACK_NERD_FONT_ZIP:-}" ]; then
  echo ">> Downloading Hack Nerd Font $RELEASE_TAG ..."
  curl -fsSL -o "$ZIP" "https://github.com/ryanoasis/nerd-fonts/releases/download/${RELEASE_TAG}/Hack.zip"
fi

actual_sha256="$(sha256sum "$ZIP" | cut -d' ' -f1 | tr -d '\\r')"
if [ "$actual_sha256" != "$EXPECTED_SHA256" ]; then
  echo "font archive checksum mismatch: expected $EXPECTED_SHA256, got $actual_sha256" >&2
  exit 1
fi

STAGING="$(mktemp -d)"
unzip -qo "$ZIP" -d "$STAGING"
mkdir -p "$FONT_DIR"

count=0
for font in "$STAGING"/HackNerdFontMono-*.ttf; do
  [ -e "$font" ] || continue
  cp -f "$font" "$FONT_DIR/"
  count=$((count + 1))
done
if [ "$count" -eq 0 ]; then
  echo "no HackNerdFontMono TTF files found in archive" >&2
  exit 1
fi
echo ">> Copied $count HackNerdFontMono TTF file(s) into $FONT_DIR"

registry_status=0
if command -v reg >/dev/null 2>&1; then
  reg add "HKCU\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts" \
    /v "Hack Nerd Font Mono (TrueType)" /t REG_SZ \
    /d "HackNerdFontMono-Regular.ttf" /f >/dev/null 2>&1 || registry_status=$?
else
  registry_status=127
fi
if [ "$registry_status" -eq 0 ]; then
  echo ">> registry: success"
else
  echo ">> registry: failed (status $registry_status)" >&2
  exit "$registry_status"
fi

echo ">> Done. Restart terminal apps to pick up the font."
