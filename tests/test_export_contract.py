import json
import shutil
import tempfile
import unittest
from pathlib import Path


from scripts.export_contract import validate_exports

ROOT = Path(__file__).resolve().parents[1]
ANSI = (
    "Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White",
    "BrightBlack", "BrightRed", "BrightGreen", "BrightYellow", "BrightBlue",
    "BrightMagenta", "BrightCyan", "BrightWhite",
)


class ExportContractTests(unittest.TestCase):
    def test_vscode_exports_have_identical_workbench_colors(self):
        theme = json.loads((ROOT / "vscode/tokencat.vscode-theme.json").read_text(encoding="utf-8"))
        settings = json.loads((ROOT / "vscode/tokencat-color-customizations.json").read_text(encoding="utf-8"))
        self.assertEqual(theme["colors"], settings["workbench.colorCustomizations"])
        for name in ANSI:
            self.assertIn(f"terminal.ansi{name}", theme["colors"])
        for key in ("diffEditor.insertedLineBackground", "diffEditor.removedLineBackground"):
            self.assertEqual(len(theme["colors"][key]), 7)

    def test_real_exports_obey_palette(self):
        self.assertEqual(validate_exports(ROOT), [])

    def _errors_after(self, mutate):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            shutil.copytree(
                ROOT, root,
                ignore=shutil.ignore_patterns(".git", ".hermes", ".venv", "venv", "__pycache__", ".ruff_cache"),
            )
            self.assertEqual(validate_exports(root), [])
            mutate(root)
            return validate_exports(root)

    def _change_json(self, root, relative, mutate):
        path = root / relative
        data = json.loads(path.read_text(encoding="utf-8"))
        mutate(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def test_changed_color_is_detected(self):
        errors = self._errors_after(lambda root: self._change_json(
            root, "windows-terminal/tokencat.scheme.json", lambda data: data.update(blue="#000000")
        ))
        self.assertTrue(any("/blue: palette drift" in item for item in errors))

    def test_removed_color_is_detected(self):
        errors = self._errors_after(lambda root: self._change_json(
            root, "windows-terminal/tokencat.scheme.json", lambda data: data.pop("brightBlue")
        ))
        self.assertTrue(any("coverage mismatch" in item for item in errors))

    def test_malformed_json_has_file_diagnostic(self):
        errors = self._errors_after(
            lambda root: (root / "windows-terminal/tokencat.scheme.json").write_text("{", encoding="utf-8")
        )
        self.assertTrue(any(item.startswith("windows-terminal/tokencat.scheme.json:") for item in errors))

    def test_duplicate_json_keys_are_rejected(self):
        def mutate(root):
            path = root / "windows-terminal/tokencat.scheme.json"
            text = path.read_text(encoding="utf-8")
            path.write_text(text.replace("{", '{"blue":"#000000",', 1), encoding="utf-8")
        errors = self._errors_after(mutate)
        self.assertTrue(any("duplicate JSON key: blue" in item for item in errors))

    def test_invalid_hex_is_rejected(self):
        errors = self._errors_after(lambda root: self._change_json(
            root, "windows-terminal/tokencat.scheme.json", lambda data: data.update(blue="#gggggg")
        ))
        self.assertTrue(any("/blue: invalid or missing color" in item for item in errors))

    def test_missing_export_is_rejected(self):
        errors = self._errors_after(lambda root: (root / "windows-terminal/tokencat.scheme.json").unlink())
        self.assertTrue(any(item.startswith("windows-terminal/tokencat.scheme.json:") for item in errors))

    def test_unknown_base_token_is_rejected(self):
        def mutate_palette(data):
            data["exports"]["windows-terminal/tokencat.scheme.json"]["/blue"] = "does_not_exist"
        errors = self._errors_after(lambda root: self._change_json(root, "palettes/tokencat.json", mutate_palette))
        self.assertTrue(any("/blue: unknown base token" in item for item in errors))

    def test_extra_unmapped_color_is_rejected(self):
        errors = self._errors_after(lambda root: self._change_json(
            root, "windows-terminal/tokencat.scheme.json", lambda data: data.update(unexpected="#ffffff")
        ))
        self.assertTrue(any("color mapping coverage mismatch" in item for item in errors))

    def test_missing_exports_contract_is_rejected(self):
        errors = self._errors_after(lambda root: self._change_json(
            root, "palettes/tokencat.json", lambda data: data.pop("exports")
        ))
        self.assertTrue(any(item.startswith("invalid export contract:") for item in errors))

    def test_wrong_exports_type_is_rejected(self):
        errors = self._errors_after(lambda root: self._change_json(
            root, "palettes/tokencat.json", lambda data: data.update(exports=[])
        ))
        self.assertTrue(any("base/exports must be objects" in item for item in errors))

    def test_wrong_base_value_type_is_rejected(self):
        errors = self._errors_after(lambda root: self._change_json(
            root, "palettes/tokencat.json", lambda data: data["base"].update(blue=12)
        ))
        self.assertTrue(any("base tokens must be hex strings" in item for item in errors))
