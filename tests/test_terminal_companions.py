import copy
import json
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

from test_theme_regressions import contrast_ratio

from scripts import export_contract

ROOT = Path(__file__).resolve().parents[1]
ZELLIJ_ROLES = {
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


class TerminalCompanionTests(unittest.TestCase):
    def _wezterm_text_pairs(self, colors):
        pairs = [
            ("body", colors["foreground"], colors["background"]),
            ("selection", colors["selection_fg"], colors["selection_bg"]),
            ("cursor", colors["cursor_fg"], colors["cursor_bg"]),
        ]
        for state in (
            "active_tab",
            "inactive_tab",
            "inactive_tab_hover",
            "new_tab",
            "new_tab_hover",
        ):
            tab = colors["tab_bar"][state]
            pairs.append((state, tab["fg_color"], tab["bg_color"]))
        return pairs

    def _assert_text_pairs_clear_aa(self, pairs):
        for name, foreground, background in pairs:
            self.assertGreaterEqual(contrast_ratio(foreground, background), 4.5, name)

    def _zellij_text_pairs(self, roles):
        return [
            (role + ":" + foreground, colors[foreground], colors["background"])
            for role, colors in roles.items()
            if role != "multiplayer_user_colors"
            for foreground in ("base", "emphasis_0", "emphasis_1", "emphasis_2", "emphasis_3")
        ]

    def test_wezterm_emitted_tab_selection_text_clears_aa(self):
        colors = tomllib.loads((ROOT / "wezterm/tokencat.toml").read_text(encoding="utf-8"))[
            "colors"
        ]
        self._assert_text_pairs_clear_aa(self._wezterm_text_pairs(colors))

    def test_wezterm_state_guard_detects_each_low_contrast_foreground(self):
        original = tomllib.loads((ROOT / "wezterm/tokencat.toml").read_text(encoding="utf-8"))[
            "colors"
        ]
        for name, _, background in self._wezterm_text_pairs(original):
            with self.subTest(state=name):
                colors = copy.deepcopy(original)
                if name in {"body", "selection", "cursor"}:
                    key = {
                        "body": "foreground",
                        "selection": "selection_fg",
                        "cursor": "cursor_fg",
                    }[name]
                    colors[key] = background
                else:
                    colors["tab_bar"][name]["fg_color"] = background
                with self.assertRaisesRegex(AssertionError, name):
                    self._assert_text_pairs_clear_aa(self._wezterm_text_pairs(colors))

    def test_zellij_emitted_selected_ribbon_emphasis_text_clears_aa(self):
        roles = export_contract.parse_companion_export(
            Path("zellij/tokencat.kdl"),
            (ROOT / "zellij/tokencat.kdl").read_text(encoding="utf-8"),
        )["themes"]["tokencat"]
        self._assert_text_pairs_clear_aa(self._zellij_text_pairs(roles))

    def test_zellij_state_guard_detects_each_low_contrast_foreground(self):
        original = export_contract.parse_companion_export(
            Path("zellij/tokencat.kdl"),
            (ROOT / "zellij/tokencat.kdl").read_text(encoding="utf-8"),
        )["themes"]["tokencat"]
        for name, _, background in self._zellij_text_pairs(original):
            with self.subTest(state=name):
                role, foreground = name.split(":")
                roles = copy.deepcopy(original)
                roles[role][foreground] = background
                with self.assertRaisesRegex(AssertionError, name):
                    self._assert_text_pairs_clear_aa(self._zellij_text_pairs(roles))

    def test_new_exports_are_required_and_palette_mapped(self):
        for relative in ("wezterm/tokencat.toml", "zellij/tokencat.kdl"):
            with self.subTest(relative=relative):
                self.assertIn(relative, export_contract.EXPORT_FILES)
                self.assertTrue((ROOT / relative).is_file())
        self.assertEqual(export_contract.validate_exports(ROOT), [])

    def test_wezterm_scheme_has_name_complete_ansi_and_safe_selection(self):
        data = tomllib.loads((ROOT / "wezterm/tokencat.toml").read_text(encoding="utf-8"))
        self.assertEqual(data["metadata"]["name"], "Tokencat")
        colors = data["colors"]
        self.assertEqual(len(colors["ansi"]), 8)
        self.assertEqual(len(colors["brights"]), 8)
        self.assertEqual(colors["foreground"], "#f2f4f8")
        self.assertEqual(colors["background"], "#161616")
        self.assertEqual(colors["selection_fg"], "#f2f4f8")
        self.assertEqual(colors["selection_bg"], "#2a2a2a")
        windows = json.loads((ROOT / "windows-terminal/tokencat.scheme.json").read_text())
        names = ("black", "red", "green", "yellow", "blue", "purple", "cyan", "white")
        self.assertEqual(colors["ansi"], [windows[name] for name in names])
        self.assertEqual(colors["brights"], [windows["bright" + name.title()] for name in names])

    def test_zellij_modern_roles_and_complete_multiplayer_colors(self):
        data = export_contract.parse_zellij_theme(
            (ROOT / "zellij/tokencat.kdl").read_text(encoding="utf-8")
        )
        roles = data["themes"]["tokencat"]
        self.assertEqual(set(roles), ZELLIJ_ROLES)
        standard = {"base", "background", "emphasis_0", "emphasis_1", "emphasis_2", "emphasis_3"}
        for name in ZELLIJ_ROLES - {"multiplayer_user_colors"}:
            self.assertEqual(set(roles[name]), standard)
        self.assertEqual(
            set(roles["multiplayer_user_colors"]), {f"player_{index}" for index in range(1, 11)}
        )
        self.assertEqual(roles["text_selected"]["base"], "#f2f4f8")
        self.assertEqual(roles["ribbon_selected"]["base"], "#161616")
        self.assertEqual(roles["ribbon_selected"]["background"], "#78a9ff")

    def test_zellij_subset_rejects_duplicates_bad_rgb_and_unbalanced_blocks(self):
        for text in (
            "themes {\n tokencat {\n base 0 0 0\n base 1 1 1\n }\n}\n",
            "themes {\n tokencat {\n base 256 0 0\n }\n}\n",
            "themes {\n tokencat {\n base 0 0 0\n }\n",
            "themes {\n tokencat {\n base -1 0 0\n }\n}\n",
            "themes {\n tokencat {\n base 0 0\n }\n}\n",
            "themes {\n tokencat {\n base 0 0 0; exec command\n }\n}\n",
        ):
            with self.subTest(text=text), self.assertRaises(ValueError):
                export_contract.parse_zellij_theme(text)

    def test_zellij_rgb_rejects_non_ascii_decimal_digits(self):
        for channels in ("٢٤٢ ٢٤٤ ٢٤٨", "२४२ २४४ २४८", "２４２ ２４４ ２４８", "2٤2 244 248"):
            text = "themes {\n tokencat {\n base " + channels + "\n }\n}\n"
            with self.subTest(channels=channels), self.assertRaises(ValueError):
                export_contract.parse_zellij_theme(text)

    def test_native_structure_checks_reject_missing_wezterm_ansi(self):
        source = (ROOT / "wezterm/tokencat.toml").read_text(encoding="utf-8")
        with self.assertRaises(ValueError):
            export_contract.parse_companion_export(
                Path("wezterm/tokencat.toml"), source.replace("ansi = [", "other = [", 1)
            )

    def test_native_structure_checks_reject_missing_zellij_role(self):
        source = (ROOT / "zellij/tokencat.kdl").read_text(encoding="utf-8")
        with self.assertRaises(ValueError):
            export_contract.parse_companion_export(
                Path("zellij/tokencat.kdl"), source.replace("frame_selected {", "other {", 1)
            )

    def test_scope_includes_new_theme_directories(self):
        from scripts.validate_theme import _distributable_files

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for relative in ("wezterm/theme.toml", "zellij/theme.kdl"):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("color", encoding="utf-8")
                self.assertIn(path, _distributable_files(root))

    def test_zellij_parse_does_not_invoke_a_process(self):
        source = (ROOT / "zellij/tokencat.kdl").read_text(encoding="utf-8")
        with patch("subprocess.run", side_effect=AssertionError("unexpected subprocess")):
            self.assertIsInstance(export_contract.parse_zellij_theme(source), dict)
