import re
import unittest
from pathlib import Path

from rich.text import Text

from scripts.validate_theme import _parse_skin

ROOT = Path(__file__).resolve().parents[1]


def rendered_rows(markup):
    return [Text.from_markup(row).plain.rstrip() for row in markup.splitlines()]


class ArtworkTests(unittest.TestCase):
    def setUp(self):
        self.source = (ROOT / "ascii-art/token-cat-29x11.txt").read_text(encoding="utf-8").splitlines()
        self.source = [row.rstrip() for row in self.source]
        self.skin = _parse_skin((ROOT / "hermes/skins/tokencat.yaml").read_text(encoding="utf-8"))

    def test_plain_source_geometry(self):
        self.assertEqual(len(self.source), 11)
        self.assertEqual(max(map(len, self.source)), 29)
        self.assertEqual(sum(row.count("$TOKENS") for row in self.source), 1)
        self.assertTrue(all(row.isascii() for row in self.source))

    def test_active_hero_renders_exact_source(self):
        self.assertEqual(rendered_rows(self.skin["banner_hero"]), self.source)
        self.assertEqual(self.skin["banner_logo"], " ")

    def test_default_art_remains_one_span_per_source_row(self):
        rows = self.skin["banner_hero"].splitlines()
        self.assertEqual(len(rows), 11)
        for row in rows:
            self.assertEqual(len(re.findall(r"\[#[0-9a-fA-F]{6}\]", row)), 1)
            self.assertEqual(row.count("[/]"), 1)

    def test_two_tone_is_valid_rich_but_not_default(self):
        alternate = (ROOT / "ascii-art/token-cat-two-tone.rich.txt").read_text(encoding="utf-8")
        self.assertEqual(rendered_rows(alternate), self.source)
        self.assertNotEqual(alternate.rstrip(), self.skin["banner_hero"].rstrip())

    def test_backslash_escape_regression_is_detectable(self):
        good = "[#78a9ff]box \\ [/]"
        bad = "[#78a9ff]box \\[/]"
        self.assertEqual(Text.from_markup(good).plain.rstrip(), "box \\")
        self.assertNotEqual(Text.from_markup(bad).plain.rstrip(), "box \\")
