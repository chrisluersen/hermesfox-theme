import hashlib
import os
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "fonts" / "install-hack-nerd-font.sh"


class FontInstallerTests(unittest.TestCase):
    def make_fixture(self, files):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        archive = root / "Hack.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            for name, data in files.items():
                zf.writestr(name, data)
        font_dir = root / "fonts"
        bin_dir = root / "bin"
        bin_dir.mkdir()
        (bin_dir / "reg").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        (bin_dir / "reg").chmod(0o755)
        return temp, root, archive, font_dir, bin_dir

    def run_installer(self, archive, font_dir, bin_dir, **extra):
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        env = os.environ.copy()
        env.update(
            PATH=f"{bin_dir}{os.pathsep}{env['PATH']}",
            FONT_DIR=str(font_dir),
            HACK_NERD_FONT_ZIP=str(archive),
            HACK_NERD_FONT_SHA256=digest,
            HACK_NERD_FONT_VERSION="test",
        )
        env.update(extra)
        bash = shutil.which("bash") or "C:/Program Files/Git/usr/bin/bash.exe"
        return subprocess.run(
            [bash, str(INSTALLER)],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
        )

    def test_installs_only_mono_fonts_into_created_destination(self):
        temp, root, archive, font_dir, bin_dir = self.make_fixture(
            {"HackNerdFontMono-Regular.ttf": "mono", "HackNerdFont-Regular.ttf": "regular"}
        )
        with temp:
            result = self.run_installer(archive, font_dir, bin_dir)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual([p.name for p in font_dir.iterdir()], ["HackNerdFontMono-Regular.ttf"])
            self.assertIn("Copied 1", result.stdout)
            self.assertIn("registry: success", result.stdout)

    def test_rejects_bad_checksum_before_extracting(self):
        temp, root, archive, font_dir, bin_dir = self.make_fixture({"HackNerdFontMono-Regular.ttf": "mono"})
        with temp:
            result = self.run_installer(archive, font_dir, bin_dir, HACK_NERD_FONT_SHA256="0" * 64)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("checksum", result.stderr.lower())
            self.assertFalse(font_dir.exists())

    def test_fails_when_archive_has_no_mono_fonts(self):
        temp, root, archive, font_dir, bin_dir = self.make_fixture({"HackNerdFont-Regular.ttf": "regular"})
        with temp:
            result = self.run_installer(archive, font_dir, bin_dir)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no HackNerdFontMono", result.stderr)

    def test_requires_font_dir_or_localappdata(self):
        temp, root, archive, font_dir, bin_dir = self.make_fixture({"HackNerdFontMono-Regular.ttf": "mono"})
        with temp:
            env = os.environ.copy()
            env.pop("FONT_DIR", None)
            env.pop("LOCALAPPDATA", None)
            env.update(
                PATH=f"{bin_dir}{os.pathsep}{env['PATH']}",
                HACK_NERD_FONT_ZIP=str(archive),
                HACK_NERD_FONT_SHA256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                HACK_NERD_FONT_VERSION="test",
            )
            bash = shutil.which("bash") or "C:/Program Files/Git/usr/bin/bash.exe"
            result = subprocess.run([bash, str(INSTALLER)], cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FONT_DIR or LOCALAPPDATA must be set", result.stderr)

    def test_registry_failure_is_reported_after_copy(self):
        temp, root, archive, font_dir, bin_dir = self.make_fixture({"HackNerdFontMono-Regular.ttf": "mono"})
        with temp:
            (bin_dir / "reg").write_text("#!/bin/sh\nexit 9\n", encoding="utf-8")
            result = self.run_installer(archive, font_dir, bin_dir)
            self.assertEqual(result.returncode, 9)
            self.assertIn("registry: failed", result.stderr)
            self.assertTrue((font_dir / "HackNerdFontMono-Regular.ttf").exists())


if __name__ == "__main__":
    unittest.main()
