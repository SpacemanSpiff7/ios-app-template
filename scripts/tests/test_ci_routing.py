from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
(ROOT / ".scratch/tests").mkdir(parents=True, exist_ok=True)


class CIRoutingTests(unittest.TestCase):
    def test_source_and_generated_app_use_the_right_gate_and_propagate_failure(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch/tests") as folder:
            root = Path(folder)
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "ci.sh").write_text((ROOT / "scripts/ci.sh").read_text())
            for name, text in {
                "validate-template.sh": "#!/bin/bash\necho template\nexit 7\n",
                "test-gate.sh": "#!/bin/bash\necho app\n",
            }.items():
                path = scripts / name
                path.write_text(text)
                path.chmod(0o755)
            (root / "project.yml").write_text("name: __APP_NAME__\n")
            source = subprocess.run(["bash", "scripts/ci.sh"], cwd=root, capture_output=True, text=True)
            self.assertEqual((source.returncode, source.stdout.strip()), (7, "template"))
            (root / "project.yml").write_text("name: CoolApp\n")
            generated = subprocess.run(["bash", "scripts/ci.sh"], cwd=root, capture_output=True, text=True)
            self.assertEqual((generated.returncode, generated.stdout.strip()), (0, "app"))
