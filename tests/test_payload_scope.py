import tempfile
import unittest
from pathlib import Path

from scripts.validate_theme import _distributable_files


class PayloadScopeTests(unittest.TestCase):
    def test_operational_plan_is_excluded_but_payloads_are_included(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            private = root / ".hermes/plans/private.md"
            public = root / "palettes/tokencat.json"
            private.parent.mkdir(parents=True)
            public.parent.mkdir(parents=True)
            private.write_text("/home/example/private", encoding="utf-8")
            public.write_text("{}", encoding="utf-8")
            files = _distributable_files(root)
            self.assertNotIn(private, files)
            self.assertIn(public, files)
