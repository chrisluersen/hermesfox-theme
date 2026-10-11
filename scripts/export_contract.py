"""Validate every mapped color in the shipped companion exports."""
import re
from pathlib import Path

if __package__:
    from .theme_io import strict_json, strict_yaml
else:
    from theme_io import strict_json, strict_yaml

EXPORT_FILES = ('windows-terminal/tokencat.scheme.json', 'vscode/tokencat.vscode-theme.json', 'vscode/tokencat-color-customizations.json', 'hermes/dashboard-themes/tokencat.yaml')
HEX = re.compile(r"#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?\Z")


def color_leaves(value, prefix=""):
    result = {}
    if isinstance(value, dict):
        for key, child in value.items():
            key = str(key).replace("~", "~0").replace("/", "~1")
            result.update(color_leaves(child, f"{prefix}/{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            result.update(color_leaves(child, f"{prefix}/{index}"))
    elif isinstance(value, str) and value.startswith("#"):
        result[prefix] = value
    return result


def validate_exports(root: Path):
    errors = []
    try:
        palette = strict_json((root / "palettes/tokencat.json").read_text(encoding="utf-8"))
        base = palette["base"]
        exports = palette["exports"]
        if not isinstance(base, dict) or not isinstance(exports, dict):
            raise ValueError("base/exports must be objects")
        if not base or not all(isinstance(v, str) and HEX.fullmatch(v) for v in base.values()):
            raise ValueError("base tokens must be hex strings")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [f"invalid export contract: {exc}"]
    if set(exports) != set(EXPORT_FILES):
        errors.append("export contract must cover every shipped color export")
    for relative in EXPORT_FILES:
        try:
            path = root / relative
            text = path.read_text(encoding="utf-8")
            data = strict_yaml(text) if path.suffix == ".yaml" else strict_json(text)
            if not isinstance(data, dict):
                raise ValueError("export must be an object")
            colors = color_leaves(data)
            mapping = exports.get(relative)
            if not isinstance(mapping, dict) or not mapping:
                raise ValueError("missing color mapping")
            if set(colors) != set(mapping):
                errors.append(f"{relative}: color mapping coverage mismatch")
            for pointer, token in mapping.items():
                actual = colors.get(pointer)
                if not isinstance(token, str) or token not in base:
                    errors.append(f"{relative}{pointer}: unknown base token")
                elif not isinstance(actual, str) or not HEX.fullmatch(actual):
                    errors.append(f"{relative}{pointer}: invalid or missing color")
                elif actual.lower() != base[token].lower():
                    errors.append(f"{relative}{pointer}: palette drift")
        except (OSError, ValueError, TypeError) as exc:
            errors.append(f"{relative}: {exc}")
    return errors
