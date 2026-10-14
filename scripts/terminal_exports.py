"""Parse the declarative terminal exports; the KDL reader is a bounded subset, not Zellij."""

import re
import tomllib
from pathlib import Path

if __package__:
    from .theme_io import strict_json, strict_yaml
else:
    from theme_io import strict_json, strict_yaml

ZELLIJ_ROLES = frozenset(
    {
        "text_unselected",
        "text_selected",
        "ribbon_selected",
        "ribbon_unselected",
        "table_title",
        "table_cell_selected",
        "table_cell_unselected",
        "list_selected",
        "list_unselected",
        "frame_selected",
        "frame_highlight",
        "exit_code_success",
        "exit_code_error",
        "multiplayer_user_colors",
    }
)
ZELLIJ_STANDARD_FIELDS = frozenset(
    {"base", "background", "emphasis_0", "emphasis_1", "emphasis_2", "emphasis_3"}
)
WEZTERM_FIELDS = frozenset(
    {
        "foreground",
        "background",
        "cursor_bg",
        "cursor_fg",
        "cursor_border",
        "selection_fg",
        "selection_bg",
        "scrollbar_thumb",
        "split",
        "ansi",
        "brights",
        "tab_bar",
    }
)


def parse_zellij_theme(text: str) -> dict:
    """Read only nested named blocks and three-integer RGB nodes, one per line.

    Reject all other KDL constructs. Native Zellij parsing/rendering remains an
    independent qualification; this is intentionally not a general KDL parser.
    """
    result = {}
    stack = [result]
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("//", 1)[0].strip()
        if not line:
            continue
        if line == "}":
            if len(stack) == 1:
                raise ValueError(f"KDL line {number}: unexpected closing block")
            stack.pop()
            continue
        block = re.fullmatch(r"([a-z][a-z_0-9]*)\s*\{", line)
        rgb = re.fullmatch(r"([a-z][a-z_0-9]*)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)", line)
        match = block or rgb
        if match is None:
            raise ValueError(f"KDL line {number}: unsupported syntax")
        key = match[1]
        if key in stack[-1]:
            raise ValueError(f"KDL line {number}: duplicate node {key}")
        if block:
            child = {}
            stack[-1][key] = child
            stack.append(child)
        else:
            channels = tuple(int(match[index]) for index in (2, 3, 4))
            if any(channel > 255 for channel in channels):
                raise ValueError(f"KDL line {number}: RGB channel outside 0..255")
            stack[-1][key] = "#" + "".join(f"{channel:02x}" for channel in channels)
    if len(stack) != 1:
        raise ValueError("KDL: unclosed block")
    return result


def _check_zellij_structure(data: dict) -> None:
    if set(data) != {"themes"} or not isinstance(data["themes"], dict):
        raise ValueError("Zellij export must contain only themes")
    themes = data["themes"]
    if set(themes) != {"tokencat"} or not isinstance(themes["tokencat"], dict):
        raise ValueError("Zellij export must contain only the tokencat theme")
    roles = themes["tokencat"]
    if set(roles) != ZELLIJ_ROLES:
        raise ValueError("Zellij export must contain every declared modern role")
    for role, colors in roles.items():
        fields = (
            {f"player_{index}" for index in range(1, 11)}
            if role == "multiplayer_user_colors"
            else ZELLIJ_STANDARD_FIELDS
        )
        if not isinstance(colors, dict) or set(colors) != fields:
            raise ValueError(f"Zellij {role}: missing or unexpected fields")
        if not all(isinstance(value, str) for value in colors.values()):
            raise ValueError(f"Zellij {role}: expected RGB color nodes")


def _check_wezterm_structure(data: dict) -> None:
    if set(data) != {"colors", "metadata"} or data["metadata"] != {"name": "Tokencat"}:
        raise ValueError("WezTerm export must be the declarative Tokencat scheme")
    colors = data["colors"]
    if not isinstance(colors, dict) or set(colors) != WEZTERM_FIELDS:
        raise ValueError("WezTerm export has missing or unexpected color fields")
    for key in ("ansi", "brights"):
        if not isinstance(colors[key], list) or len(colors[key]) != 8:
            raise ValueError(f"WezTerm {key}: expected eight colors")
    tabs = colors["tab_bar"]
    states = {"active_tab", "inactive_tab", "inactive_tab_hover", "new_tab", "new_tab_hover"}
    if not isinstance(tabs, dict) or set(tabs) != states | {"background"}:
        raise ValueError("WezTerm tab bar has missing or unexpected states")
    for state in states:
        if not isinstance(tabs[state], dict) or set(tabs[state]) != {"bg_color", "fg_color"}:
            raise ValueError(f"WezTerm {state}: expected background and foreground")


def parse_companion_export(path: Path, text: str) -> dict:
    if path.suffix == ".kdl":
        data = parse_zellij_theme(text)
        _check_zellij_structure(data)
        return data
    if path.suffix == ".toml":
        data = tomllib.loads(text)
        _check_wezterm_structure(data)
        return data
    return strict_yaml(text) if path.suffix == ".yaml" else strict_json(text)
