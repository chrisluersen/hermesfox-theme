import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class CIContractTests(unittest.TestCase):
    def test_cross_platform_lint_and_validation_are_explicit(self):
        # BaseLoader keeps the YAML 1.1 word `on` a string without altering global loaders.
        workflow = yaml.load(
            (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8"),
            Loader=yaml.BaseLoader,
        )
        self.assertEqual(set(workflow["on"]), {"push", "pull_request"})
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        job = workflow["jobs"]["validate"]
        self.assertEqual(
            job["strategy"]["matrix"].get("include"),
            [
                {"os": "ubuntu-latest", "python": "3.11"},
                {"os": "windows-latest", "python": "3.14"},
            ],
        )
        commands = [step["run"] for step in job["steps"] if "run" in step]
        for required in (
            "python -m ruff check scripts tests",
            "python -m ruff format --check scripts tests",
            "python -B -m unittest discover -s tests -v",
            "python -B scripts/validate_theme.py",
            "bash -n fonts/install-hack-nerd-font.sh",
            "shellcheck fonts/install-hack-nerd-font.sh",
        ):
            self.assertIn(required, commands)
        for step in job["steps"]:
            if "uses" in step:
                self.assertRegex(step["uses"], r"^[^@]+@[0-9a-f]{40}$")
