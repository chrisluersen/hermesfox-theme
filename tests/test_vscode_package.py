import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class VSCodePackageTests(unittest.TestCase):
    def test_theme_extension_points_at_shipped_dark_theme(self):
        self.assertTrue((ROOT / "vscode/package.json").is_file())
        manifest = json.loads((ROOT / "vscode/package.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["categories"], ["Themes"])
        self.assertEqual(manifest["license"], "UNLICENSED")
        self.assertNotIn("main", manifest)
        self.assertNotIn("activationEvents", manifest)
        themes = manifest["contributes"]["themes"]
        self.assertEqual({item["label"] for item in themes}, {"Tokencat", "Carbonfox (Legacy)"})
        self.assertEqual(len(themes), 2)
        self.assertEqual(
            {theme["label"]: theme["path"] for theme in themes},
            {
                "Tokencat": "./tokencat.vscode-theme.json",
                "Carbonfox (Legacy)": "./carbonfox.vscode-theme.json",
            },
        )
        for theme in themes:
            self.assertEqual(theme["uiTheme"], "vs-dark")
            self.assertTrue((ROOT / "vscode" / theme["path"]).is_file())
