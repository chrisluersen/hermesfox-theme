"""Validate the portable Hermesfox theme bundle."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

CANONICAL_COLOR_KEYS = (
    "background", "banner_border", "banner_title", "banner_accent", "banner_dim",
    "banner_text", "ui_accent", "ui_label", "ui_ok", "ui_error", "ui_warn",
    "ui_tool", "ui_thinking", "diff_added", "diff_removed", "diff_added_word",
    "diff_removed_word", "syntax_string", "syntax_number", "syntax_keyword",
    "syntax_comment", "prompt", "input_rule", "response_border", "status_bar_bg",
    "status_bar_text", "status_bar_strong", "status_bar_dim", "status_bar_good",
    "status_bar_warn", "status_bar_bad", "status_bar_critical", "session_label",
    "session_border", "voice_status_bg", "selection_bg", "completion_menu_bg",
    "completion_menu_current_bg", "completion_menu_meta_bg",
    "completion_menu_meta_current_bg",
)

# The palette file is the single source of truth for the Hermes mapping contract.
SEMANTIC_MAPPINGS = tuple(
    {"skin": skin, "palette": palette}
    for skin, palette in {
        "background": "background", "banner_border": "blue", "banner_title": "foreground",
        "banner_accent": "blue", "banner_dim": "muted", "banner_text": "foreground",
        "ui_accent": "blue", "ui_label": "cyan", "ui_ok": "green", "ui_error": "red",
        "ui_warn": "orange", "ui_tool": "cyan", "ui_thinking": "purple",
        "diff_added": "background", "diff_removed": "background", "diff_added_word": "green",
        "diff_removed_word": "red", "syntax_string": "cyan", "syntax_number": "purple",
        "syntax_keyword": "blue", "syntax_comment": "muted", "prompt": "foreground",
        "input_rule": "blue", "response_border": "blue", "status_bar_bg": "background",
        "status_bar_text": "foreground_alt", "status_bar_strong": "foreground",
        "status_bar_dim": "muted", "status_bar_good": "green", "status_bar_warn": "orange",
        "status_bar_bad": "red", "status_bar_critical": "red", "session_label": "blue",
        "session_border": "muted", "voice_status_bg": "background", "selection_bg": "surface_selected",
        "completion_menu_bg": "background", "completion_menu_current_bg": "surface_selected",
        "completion_menu_meta_bg": "background", "completion_menu_meta_current_bg": "surface_selected",
    }.items()
)

USER_MARKERS = (r"C:\Users\chris", "C:/Users/chris", "<USER>")
JSON_FILES = ("palette.json", "vscode/carbonfox.vscode-theme.json", "vscode/vscode-color-customizations.json", "windows-terminal/scheme.json")
JSONC_FILES = ("vscode/settings.json",)


def _parse_jsonc(text: str) -> Any:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"(^|\s)//.*", r"\1", text)
    text = re.sub(r",(\s*[}\]])", r"\1", text)
    return json.loads(text)


def _parse_skin(text: str) -> dict[str, Any]:
    """Parse the small scalar/map subset used by the distributable skin."""
    result: dict[str, Any] = {"colors": {}}
    section = None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("colors:"):
            section = "colors"
            continue
        if line.startswith("banner_logo:"):
            result["banner_logo"] = line.split(":", 1)[1].strip().strip('"')
            section = None
            continue
        if line.startswith("banner_hero:"):
            section = "banner_hero"
            result[section] = ""
            continue
        if section == "banner_hero" and line.startswith("  "):
            result[section] += line[2:] + "\n"
            continue
        if section == "colors" and line.startswith("  ") and ":" in line:
            key, value = line.strip().split(":", 1)
            result["colors"][key] = re.sub(r"\s+#.*$", "", value).strip().strip('"')
            continue
        section = None
    if not result["colors"]:
        raise ValueError("missing colors map")
    return result


def _plain_hero(hero: str) -> list[str]:
    return [re.sub(r"\[[^]]*\]", "", row).rstrip() for row in hero.splitlines()]


def _source_hero(root: Path) -> list[str] | None:
    source_path = root / "ascii-art/token-cat-29x11.txt"
    if not source_path.exists():
        return None
    source = source_path.read_text(encoding="utf-8").splitlines()
    return [row.replace("hjw", "$TOKENS").rstrip() for row in source]


def _distributable_files(root: Path) -> list[Path]:
    """Discover shipped text assets; archives and generated artwork are excluded by location."""
    excluded = {".git", ".venv", "__pycache__", "banner-art", "tests", "scripts"}
    files = []
    for path in root.rglob("*"):
        if path.is_file() and not any(part in excluded for part in path.relative_to(root).parts):
            files.append(path)
    return files


def validate_repository(root: Path) -> list[str]:
    violations: list[str] = []
    skin_path = root / "hermes/skins/carbonfox.yaml"
    palette_path = root / "palette.json"
    try:
        skin_text = skin_path.read_text(encoding="utf-8")
        skin = _parse_skin(skin_text)
    except (OSError, ValueError) as exc:
        violations.append(f"hermes/skins/carbonfox.yaml: invalid skin ({exc})")
        skin = {}
    try:
        palette = json.loads(palette_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        violations.append(f"palette.json: invalid JSON ({exc})")
        palette = {}
    colors = skin.get("colors", {}) if isinstance(skin, dict) else {}
    for key in CANONICAL_COLOR_KEYS:
        if key not in colors:
            violations.append(f"skin missing required color: {key}")
    if isinstance(skin, dict) and skin.get("banner_logo") != " ":
        violations.append('banner_logo must be exactly one space')
    if isinstance(skin, dict) and "banner_hero" in skin:
        expected = _source_hero(root)
        if expected is not None and _plain_hero(str(skin["banner_hero"])) != expected:
            violations.append("banner_hero does not match token-cat source")
    palette_base = palette.get("base", {}) if isinstance(palette, dict) else {}
    palette_hermes = palette.get("mappings", {}).get("hermes", {}) if isinstance(palette, dict) else {}
    if set(palette_hermes) != set(CANONICAL_COLOR_KEYS):
        violations.append("palette Hermes mapping must cover every canonical skin color")
    for mapping in SEMANTIC_MAPPINGS:
        token = palette_hermes.get(mapping["skin"])
        if token not in palette_base:
            violations.append(f"palette missing mapped base token: {mapping['skin']} -> {token}")
        elif mapping["skin"] in colors and colors[mapping["skin"]] != palette_base[token]:
            violations.append(f"semantic mapping drift: {mapping['skin']} != {token}")
    for name in JSON_FILES:
        path = root / name
        if path.exists():
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                violations.append(f"{name}: invalid JSON ({exc})")
    for name in JSONC_FILES:
        path = root / name
        if path.exists():
            try:
                _parse_jsonc(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                violations.append(f"{name}: invalid JSON/JSONC ({exc})")
    for path in _distributable_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for marker in USER_MARKERS:
            if marker in text:
                violations.append(f"{path.relative_to(root)}: contains non-portable marker {marker}")
    return violations


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    violations = validate_repository(args.root.resolve())
    if violations:
        print("\n".join(f"FAIL: {item}" for item in violations))
        return 1
    print("PASS: hermesfox theme validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
