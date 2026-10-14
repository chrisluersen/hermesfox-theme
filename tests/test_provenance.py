import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProvenanceTests(unittest.TestCase):
    def test_complete_pinned_upstream_license_is_shipped(self):
        path = ROOT / "licenses/nightfox-MIT.txt"
        self.assertTrue(path.is_file())
        self.assertEqual(
            hashlib.sha256(path.read_text(encoding="utf-8").encode()).hexdigest(),
            "280a27a527db4e93e03d525a1226ee66ca96a2cbaedb3517eccfba40ac0d7a9f",
        )

    def test_upgrade_records_full_pinned_source_chain(self):
        import json

        data = json.loads((ROOT / "palettes/tokencat.json").read_text(encoding="utf-8"))
        lineage = data["derived_from"]
        prefix = "https://github.com/EdenEast/nightfox.nvim/blob/4dacd3f0185a2227bdf3b6c0975a8f0bf87cac9a/"
        expected = {
            "lualine_source": "lua/lualine/themes/carbonfox.lua",
            "lualine_adapter": "lua/nightfox/util/lualine.lua",
            "palette_source": "lua/nightfox/palette/carbonfox.lua",
            "license_source": "LICENSE",
        }
        for key, suffix in expected.items():
            self.assertEqual(lineage.get(key), prefix + suffix)
