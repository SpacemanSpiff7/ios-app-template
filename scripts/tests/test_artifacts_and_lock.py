import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import device_helper
from source_identity import tree_digest
from simulator import select_device

ROOT = Path(__file__).resolve().parents[2]
(ROOT / ".scratch/tests").mkdir(parents=True, exist_ok=True)


class ArtifactTests(unittest.TestCase):
    def test_modified_source_and_artifact_are_rejected(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch/tests") as folder:
            app = Path(folder) / "Example.app"
            app.mkdir()
            binary = app / "Example"
            binary.write_bytes(b"original")
            source = {"tree_sha256": "source"}
            manifest = {"status": "passed", "signature_verified": True, "source": source,
                        "app": str(app), "app_tree_sha256": tree_digest(app)}
            with patch.object(device_helper, "source_identity", return_value=source):
                self.assertEqual(device_helper.verified_build(manifest), app)
                binary.write_bytes(b"changed")
                with self.assertRaisesRegex(ValueError, "artifact changed"):
                    device_helper.verified_build(manifest)
            with patch.object(device_helper, "source_identity", return_value={"tree_sha256": "new"}):
                with self.assertRaisesRegex(ValueError, "Source changed"):
                    device_helper.verified_build(manifest)

    def test_lock_rejects_parallel_command_and_releases_after_exit(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch/tests") as folder:
            env = {key: value for key, value in os.environ.items() if key != "IOS_LOCK_HELD"}
            env["TMPDIR"] = folder
            command = [sys.executable, str(ROOT / "scripts/ios-lock.py"), sys.executable, "-c"]
            holder = subprocess.Popen(command + ["import sys; print('locked', flush=True); sys.stdin.read(1)"],
                                      stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, env=env)
            try:
                self.assertEqual(holder.stdout.readline().strip(), "locked")
                blocked = subprocess.run(command + ["print('unexpected')"], capture_output=True, text=True, env=env)
                self.assertNotEqual(blocked.returncode, 0)
                self.assertIn("owns the lock", blocked.stderr)
            finally:
                holder.communicate(input="x", timeout=5)
            released = subprocess.run(command + ["print('released')"], capture_output=True, text=True, env=env)
            self.assertEqual((released.returncode, released.stdout.strip()), (0, "released"))

    def test_simulator_selection_requires_compatible_available_iphone(self):
        devices = {
            "com.apple.CoreSimulator.SimRuntime.iOS-25-0": [
                {"udid": "old", "name": "Old", "isAvailable": True, "state": "Booted",
                 "deviceTypeIdentifier": "com.apple.CoreSimulator.SimDeviceType.iPhone-Old"}],
            "com.apple.CoreSimulator.SimRuntime.iOS-27-0": [
                {"udid": "ipad", "name": "iPad", "isAvailable": True, "state": "Booted",
                 "deviceTypeIdentifier": "com.apple.CoreSimulator.SimDeviceType.iPad"},
                {"udid": "phone", "name": "iPhone", "isAvailable": True, "state": "Shutdown",
                 "deviceTypeIdentifier": "com.apple.CoreSimulator.SimDeviceType.iPhone-New"}],
        }
        self.assertEqual(select_device(devices, "26.0")["udid"], "phone")
        self.assertIsNone(select_device(devices, "26.0", "old"))
        self.assertIsNone(select_device(devices, "28.0"))
