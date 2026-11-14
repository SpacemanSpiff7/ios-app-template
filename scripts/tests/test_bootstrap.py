import argparse
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bootstrap

ROOT = Path(__file__).resolve().parents[2]
(ROOT / ".scratch/tests").mkdir(parents=True, exist_ok=True)


class BootstrapTests(unittest.TestCase):
    def args(self, **changes):
        values = dict(name="Cool App", bundle="com.example.coolapp", team="-", minimum="26.0",
                      no_git=True, template_source=None)
        return argparse.Namespace(**(values | changes))

    def fixture(self, root):
        (root / "project.yml").write_text('name: __APP_NAME__\n')
        (root / "CLAUDE.md").write_text('# __APP_NAME__\n')
        (root / "AGENTS.md").symlink_to("CLAUDE.md")
        package = root / "Packages/AppKit"
        package.mkdir(parents=True)
        (package / "Package.swift").write_text('// swift-tools-version: __SWIFT_TOOLS_VERSION__\n.iOS("__MIN_IOS__")\n')

    def tool_output(self, *args):
        return {("xcodebuild", "-version"): "Xcode 27.2",
                ("xcrun", "swift", "-version"): "Apple Swift version 6.4.2",
                ("xcrun", "--sdk", "iphonesimulator", "--show-sdk-version"): "27.2"}[args]

    def test_invalid_identity_is_rejected_before_mutation(self):
        with patch.object(bootstrap, "run") as run:
            for args in (self.args(name="3Bad"), self.args(bundle="bad"), self.args(team="invalid")):
                with self.assertRaises(ValueError):
                    bootstrap.prepare(args)
            run.assert_not_called()

    def test_sdk_boundaries_and_toolchain_detection(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch/tests") as folder:
            root = Path(folder)
            self.fixture(root)
            with patch.object(bootstrap, "ROOT", root), patch.object(bootstrap.shutil, "which", return_value="/tool"):
                with patch.object(bootstrap, "run", side_effect=self.tool_output):
                    detected = bootstrap.prepare(self.args(minimum=None))
                    self.assertEqual((detected["minimum_ios"], detected["swift_tools"]), ("27.0", "6.4"))
                    for minimum in ("17.0", "28.0", "27;bad"):
                        with self.assertRaises(ValueError):
                            bootstrap.prepare(self.args(minimum=minimum))

    def test_configuration_preserves_symlink_and_records_source(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch/tests") as folder:
            root = Path(folder)
            self.fixture(root)
            args = self.args(template_source=str(ROOT))
            with patch.object(bootstrap, "ROOT", root), patch.object(bootstrap.shutil, "which", return_value="/tool"):
                with patch.object(bootstrap, "run", side_effect=self.tool_output):
                    identity = bootstrap.prepare(args)
                bootstrap.configure(identity, args)
                self.assertTrue((root / "AGENTS.md").is_symlink())
                self.assertEqual((root / "AGENTS.md").readlink(), Path("CLAUDE.md"))
                self.assertEqual((root / "CLAUDE.md").read_text(), "# CoolApp\n")
                self.assertIn('6.4', (root / "Packages/AppKit/Package.swift").read_text())
                bootstrap.configure(identity, self.args())
                self.assertIn(str(ROOT), (root / ".template-origin.json").read_text())
                with patch.object(bootstrap, "run", side_effect=self.tool_output):
                    with self.assertRaisesRegex(ValueError, "already configured"):
                        bootstrap.prepare(self.args(name="Another App"))
