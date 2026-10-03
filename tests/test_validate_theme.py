import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_theme import (
    CANONICAL_COLOR_KEYS,
    SEMANTIC_MAPPINGS,
    validate_repository,
)


ROOT = Path(__file__).resolve().parents[1]


class ThemeValidationTests(unittest.TestCase):
    def test_canonical_skin_and_palette_parse_with_required_colors(self):
        violations = validate_repository(ROOT)
        self.assertNotIn("hermes/skins/carbonfox.yaml: invalid YAML", violations)
        self.assertNotIn("palette.json: invalid JSON", violations)
        skin = (ROOT / "hermes/skins/carbonfox.yaml").read_text(encoding="utf-8")
        palette = json.loads((ROOT / "palette.json").read_text(encoding="utf-8"))
        self.assertTrue(all(f"{key}:" in skin for key in CANONICAL_COLOR_KEYS))
        self.assertTrue(all(mapping["palette"] in palette["base"] for mapping in SEMANTIC_MAPPINGS))

    def test_token_cat_source_matches_hero_after_documented_wrappers(self):
        violations = validate_repository(ROOT)
        self.assertNotIn("banner_hero does not match token-cat source", violations)

    def test_palette_mapping(self):
        palette = json.loads((ROOT / "palette.json").read_text(encoding="utf-8"))
        self.assertIn("base", palette)
        self.assertIn("mappings", palette)
        self.assertIn("hermes", palette["mappings"])
        self.assertEqual(palette["mappings"]["hermes"]["ui_warn"], "orange")
        self.assertEqual(palette["mappings"]["hermes"]["syntax_string"], "green")
        self.assertEqual(palette["mappings"]["hermes"]["ui_tool"], "cyan_bright")
        self.assertEqual(
            set(palette["mappings"]["hermes"]),
            set(CANONICAL_COLOR_KEYS),
        )
        self.assertNotIn("warning", palette["mappings"]["hermes"])

    def test_compatibility_banner_logo_is_exactly_one_space(self):
        violations = validate_repository(ROOT)
        self.assertNotIn('banner_logo must be exactly one space', violations)

    def test_distributable_assets_reject_user_paths_and_placeholders(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "hermes/skins").mkdir(parents=True)
            (root / "hermes/skins/carbonfox.yaml").write_text(
                'name: carbonfox\ncolors: {}\nbranding: {}\nbanner_logo: " "\nbanner_hero: "hero"\n',
                encoding="utf-8",
            )
            (root / "palette.json").write_text("{\"path\": \"C:\\\\Users\\\\example\"}", encoding="utf-8")
            (root / "README.md").write_text("C:\\Users\\example", encoding="utf-8")
            violations = validate_repository(root)
            self.assertTrue(any("C:\\Users\\example" in item for item in violations))

    def test_skin_palette_drift_is_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "hermes/skins").mkdir(parents=True)
            skin = (ROOT / "hermes/skins/carbonfox.yaml").read_text(encoding="utf-8")
            (root / "hermes/skins/carbonfox.yaml").write_text(
                skin.replace('ui_tool: "#3ddbd9"', 'ui_tool: "#000000"'), encoding="utf-8")
            (root / "palette.json").write_text(
                (ROOT / "palette.json").read_text(encoding="utf-8"), encoding="utf-8")
            violations = validate_repository(root)
            self.assertTrue(any(v.startswith("skin/palette drift: ui_tool") for v in violations))

    def test_two_tone_hero_matches_token_cat_source(self):
        import re
        hero = (ROOT / "ascii-art/token-cat-two-tone.rich.txt").read_text(encoding="utf-8")
        plain = [re.sub(r"\[[^]]*\]", "", row).rstrip() for row in hero.splitlines()]
        source = (ROOT / "ascii-art/token-cat-29x11.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(plain, [row.replace("hjw", "$TOKENS").rstrip() for row in source])

    def test_jsonc_settings_are_parsed(self):
        violations = validate_repository(ROOT)
        self.assertNotIn("vscode/settings.json: invalid JSON/JSONC", violations)


if __name__ == "__main__":
    unittest.main()
