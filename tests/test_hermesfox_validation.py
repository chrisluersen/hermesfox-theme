"""The standalone validator must protect Hermesfox, not just the test suite."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_theme import validate_repository

ROOT = Path(__file__).resolve().parents[1]


class HermesfoxValidationTests(unittest.TestCase):
    def test_missing_hermesfox_artifacts_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "fixture"
            shutil.copytree(
                ROOT, root, ignore=shutil.ignore_patterns(".git", ".hermes", "__pycache__")
            )
            self.assertEqual(validate_repository(root), [])
            for relative in (
                "hermes/skins/hermesfox.yaml",
                "windows-terminal/hermesfox.scheme.json",
            ):
                (root / relative).unlink()
            violations = validate_repository(root)
            for relative in (
                "hermes/skins/hermesfox.yaml",
                "windows-terminal/hermesfox.scheme.json",
            ):
                self.assertTrue(any(relative in message for message in violations), relative)

    def test_corrupt_hermesfox_payloads_are_rejected(self):
        mutations = (
            ("hermes/skins/hermesfox.yaml", lambda text: text.replace("#7f8489", "#97999b")),
            (
                "hermes/skins/hermesfox.yaml",
                lambda text: text.replace('agent_name: "Hermesfox"', 'agent_name: "Wrong"'),
            ),
            ("hermes/skins/hermesfox.yaml", lambda text: text.replace("$TOKENS", "$WRONG")),
            ("hermes/skins/hermesfox.yaml", lambda text: "[]\n"),
            (
                "windows-terminal/hermesfox.scheme.json",
                lambda text: text.replace("#161616", "#ffffff"),
            ),
            (
                "windows-terminal/hermesfox.scheme.json",
                lambda text: text.replace('"hermesfox"', '"Wrong"'),
            ),
            ("windows-terminal/hermesfox.scheme.json", lambda text: "{broken"),
            (
                "vscode/package.json",
                lambda text: json.dumps({**json.loads(text), "contributes": {"themes": []}}),
            ),
        )
        for relative, mutate in mutations:
            with (
                self.subTest(path=relative, mutation=mutate),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory) / "fixture"
                shutil.copytree(
                    ROOT, root, ignore=shutil.ignore_patterns(".git", ".hermes", "__pycache__")
                )
                self.assertEqual(validate_repository(root), [])
                path = root / relative
                before = path.read_text(encoding="utf-8")
                after = mutate(before)
                self.assertNotEqual(after, before)
                path.write_text(after, encoding="utf-8")
                self.assertTrue(validate_repository(root), relative)
