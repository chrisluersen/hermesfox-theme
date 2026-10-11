import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_HASHES = {
    "palette.json": "6b8bad4bee75826b3fc30721b2e48d9c980ea6f9ebdbe4c662a98ca8dd67e358",
    "hermes/skins/carbonfox.yaml": "c13f01310eab6a06d620f812bbcc48b507bee83855b4621a733c569f1998c84b",
    "windows-terminal/scheme.json": "f6f9d2c2125edd6073cb5cd0ba56e1391d9b17e8d2210c5496666900bd1cd92b",
    "vscode/carbonfox.vscode-theme.json": "5d7672b4732170bff19f40d09ae49cb2be14ebed33496033d51ded145beb3d4a",
    "vscode/vscode-color-customizations.json": "3ae0d7df5f5844f33fe069654407888f17dbb4786de767f6388b2b1d4159f78e",
    "ascii-art/token-cat-29x11.txt": "d06c4247dae80cfb8238edd3084f542498a000d67e4f2c462a04467046fae1bf",
    "ascii-art/token-cat-two-tone.rich.txt": "2e35d14903e8e4f7e7b55028b0c160a3524224b4ecb71a6dd6a8680e23ce94bf"
}


class LegacyVariantTests(unittest.TestCase):
    def test_original_payloads_remain_unchanged(self):
        for relative, expected in LEGACY_HASHES.items():
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertEqual(hashlib.sha256(text.encode("utf-8")).hexdigest(), expected)

    def test_upgrade_has_distinct_files_and_identities(self):
        required = (
            "palettes/tokencat.json", "hermes/skins/tokencat.yaml",
            "windows-terminal/tokencat.scheme.json", "vscode/tokencat.vscode-theme.json",
            "vscode/tokencat-color-customizations.json",
        )
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)
        palette = json.loads((ROOT / "palettes/tokencat.json").read_text(encoding="utf-8"))
        scheme = json.loads((ROOT / "windows-terminal/tokencat.scheme.json").read_text(encoding="utf-8"))
        theme = json.loads((ROOT / "vscode/tokencat.vscode-theme.json").read_text(encoding="utf-8"))
        self.assertEqual(palette["name"], "tokencat")
        self.assertEqual(scheme["name"], "tokencat")
        self.assertEqual(theme["name"], "Tokencat")
        self.assertEqual((ROOT / "hermes/skins/tokencat.yaml").read_text(encoding="utf-8").splitlines()[0], "name: tokencat")
        legacy = json.loads((ROOT / "palette.json").read_text(encoding="utf-8"))["base"]
        for token, color in legacy.items():
            self.assertEqual(palette["base"][token], color, token)
