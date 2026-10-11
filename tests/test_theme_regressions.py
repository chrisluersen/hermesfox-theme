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
        self.assertTrue(any("duplicate JSON key: name" in item for item in validate_repository(self.root)))

    def test_nonfinite_palette_metadata_is_rejected(self):
        path = self.root / "palettes/tokencat.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["audit_probe"] = float("nan")
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(any("non-finite JSON constant" in item for item in validate_repository(self.root)))

    def test_palette_wrong_shape_returns_violations(self):
        for value in ([], {"base": [], "mappings": {}}, {"base": {}, "mappings": []}):
            with self.subTest(value=value):
                (self.root / "palettes/tokencat.json").write_text(json.dumps(value), encoding="utf-8")
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
        path.write_text(path.read_text(encoding="utf-8").split("banner_hero: |", 1)[0], encoding="utf-8")
        self.assertIn("skin missing required banner_hero", validate_repository(self.root))

    def test_private_plan_is_not_a_distributable(self):
        before = validate_repository(self.root)
        path = self.root / ".hermes/plans/private.md"
        path.parent.mkdir(parents=True)
        path.write_text("/home/example/private", encoding="utf-8")
        self.assertEqual(validate_repository(self.root), before)

