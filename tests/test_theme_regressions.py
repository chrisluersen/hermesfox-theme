import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_theme import CANONICAL_COLOR_KEYS, _parse_skin, validate_repository

ROOT = Path(__file__).resolve().parents[1]


class ThemeRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(
            ROOT,
            self.root,
            ignore=shutil.ignore_patterns(
                ".git", ".hermes", ".venv", "venv", "__pycache__", ".ruff_cache"
            ),
        )

    def test_parser_rejects_duplicate_color_keys(self):
        text = 'name: tokencat\ncolors:\n  ui_text: "#ffffff"\n  ui_text: "#000000"\n'
        with self.assertRaises(ValueError):
            _parse_skin(text)

    def test_parser_accepts_real_yaml_and_preserves_hero(self):
        data = _parse_skin(
            "name: tokencat\ncolors: {ui_text: '#ffffff'}\n"
            "banner_logo: ' '\nbanner_hero: |\n  cat\n  box\n"
        )
        self.assertEqual(data["banner_logo"], " ")
        self.assertEqual(data["banner_hero"], "cat\nbox\n")

    def test_parser_rejects_non_string_colors(self):
        with self.assertRaises(ValueError):
            _parse_skin("name: tokencat\ncolors:\n  ui_text: 12\n")

    def test_parser_rejects_list_root(self):
        with self.assertRaises(ValueError):
            _parse_skin("- tokencat\n")

    def test_duplicate_palette_json_is_rejected(self):
        path = self.root / "palettes/tokencat.json"
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace("{", '{"name":"duplicate",', 1), encoding="utf-8")
        self.assertTrue(
            any("duplicate JSON key: name" in item for item in validate_repository(self.root))
        )

    def test_nonfinite_palette_metadata_is_rejected(self):
        path = self.root / "palettes/tokencat.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["audit_probe"] = float("nan")
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(
            any("non-finite JSON constant" in item for item in validate_repository(self.root))
        )

    def test_palette_wrong_shape_returns_violations(self):
        for value in ([], {"base": [], "mappings": {}}, {"base": {}, "mappings": []}):
            with self.subTest(value=value):
                (self.root / "palettes/tokencat.json").write_text(
                    json.dumps(value), encoding="utf-8"
                )
                self.assertTrue(validate_repository(self.root))

    def test_missing_source_art_is_rejected(self):
        (self.root / "ascii-art/token-cat-29x11.txt").unlink()
        self.assertIn(
            "missing required artifact: ascii-art/token-cat-29x11.txt",
            validate_repository(self.root),
        )

    def test_missing_json_export_is_rejected(self):
        (self.root / "windows-terminal/tokencat.scheme.json").unlink()
        self.assertIn(
            "missing required artifact: windows-terminal/tokencat.scheme.json",
            validate_repository(self.root),
        )

    def test_missing_hero_is_rejected(self):
        path = self.root / "hermes/skins/tokencat.yaml"
        path.write_text(
            path.read_text(encoding="utf-8").split("banner_hero: |", 1)[0], encoding="utf-8"
        )
        self.assertIn("skin missing required banner_hero", validate_repository(self.root))

    def test_private_plan_is_not_a_distributable(self):
        before = validate_repository(self.root)
        path = self.root / ".hermes/plans/private.md"
        path.parent.mkdir(parents=True)
        path.write_text("/home/example/private", encoding="utf-8")
        self.assertEqual(validate_repository(self.root), before)

    def test_all_shared_aliases_are_explicit(self):
        skin = _parse_skin((ROOT / "hermes/skins/tokencat.yaml").read_text(encoding="utf-8"))
        palette = json.loads((ROOT / "palettes/tokencat.json").read_text(encoding="utf-8"))
        for key in ("ui_primary", "ui_text", "ui_border"):
            with self.subTest(key=key):
                self.assertIn(key, CANONICAL_COLOR_KEYS)
                self.assertIn(key, skin["colors"])
                self.assertIn(key, palette["mappings"]["hermes"])

    def test_dashboard_has_explicit_color_and_safe_layout_contract(self):
        from scripts.theme_io import strict_yaml

        self.assertTrue((ROOT / "hermes/dashboard-themes/tokencat.yaml").is_file())
        data = strict_yaml(
            (ROOT / "hermes/dashboard-themes/tokencat.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(data["name"], "tokencat")
        self.assertEqual(data["palette"]["background"]["hex"], "#161616")
        self.assertEqual(data["palette"]["midground"]["hex"], "#f2f4f8")
        self.assertEqual(data["palette"]["background"]["alpha"], 1.0)
        self.assertEqual(data["palette"]["midground"]["alpha"], 1.0)
        self.assertEqual(data["palette"]["foreground"], {"hex": "#78a9ff", "alpha": 0.0})
        self.assertEqual(data["layout"], {"radius": "0.5rem", "density": "comfortable"})
        self.assertEqual(data["layoutVariant"], "standard")
        self.assertEqual(data["palette"]["warmGlow"], "rgba(0, 0, 0, 0)")
        self.assertEqual(data["palette"]["noiseOpacity"], 0.0)
        required = {
            "card",
            "cardForeground",
            "popover",
            "popoverForeground",
            "primary",
            "primaryForeground",
            "secondary",
            "secondaryForeground",
            "muted",
            "mutedForeground",
            "accent",
            "accentForeground",
            "destructive",
            "destructiveForeground",
            "success",
            "warning",
            "border",
            "input",
            "ring",
        }
        self.assertEqual(set(data["colorOverrides"]), required)
        self.assertNotIn("fontUrl", data["typography"])
        self.assertNotIn("customCSS", data)
        self.assertNotIn("assets", data)


def contrast_ratio(first, second):
    def luminance(value):
        channels = [int(value[i : i + 2], 16) / 255 for i in (1, 3, 5)]
        linear = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in channels]
        return sum(x * weight for x, weight in zip(linear, (0.2126, 0.7152, 0.0722)))

    dark, light = sorted((luminance(first), luminance(second)))
    return (light + 0.05) / (dark + 0.05)


class ContrastTests(unittest.TestCase):
    def test_normal_text_pairs_clear_aa(self):
        base = json.loads((ROOT / "palettes/tokencat.json").read_text(encoding="utf-8"))["base"]
        pairs = (
            ("foreground", "background"),
            ("foreground", "surface"),
            ("foreground", "border"),
            ("muted_accessible", "surface"),
            ("muted_accessible", "surface_selected"),
            ("thinking_accessible", "background"),
            ("thinking_accessible", "surface"),
            ("green", "background"),
            ("orange", "background"),
            ("red", "background"),
            ("foreground", "diff_add_bg"),
            ("foreground", "diff_remove_bg"),
        )
        for foreground, background in pairs:
            with self.subTest(foreground=foreground, background=background):
                self.assertGreaterEqual(contrast_ratio(base[foreground], base[background]), 4.5)

    def test_focus_accent_clears_nontext_contrast(self):
        base = json.loads((ROOT / "palettes/tokencat.json").read_text(encoding="utf-8"))["base"]
        self.assertGreaterEqual(contrast_ratio(base["blue"], base["surface"]), 3.0)

    def test_diff_word_backgrounds_keep_text_readable(self):
        base = json.loads((ROOT / "palettes/tokencat.json").read_text(encoding="utf-8"))["base"]
        for token in ("diff_add_word_bg", "diff_remove_word_bg"):
            with self.subTest(token=token):
                self.assertGreaterEqual(contrast_ratio(base["foreground"], base[token]), 4.5)
