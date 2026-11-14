#!/usr/bin/env python3
"""Bind signed build/install/launch evidence to exact source and local artifact."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import plistlib
import subprocess
import sys
from project_config import ROOT, config
from source_identity import source_identity, tree_digest

LOGS = ROOT / ".scratch/logs"


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def run(args, log):
    with log.open("w") as stream:
        subprocess.run(args, cwd=ROOT, check=True, stdout=stream, stderr=subprocess.STDOUT)


def verified_build(manifest):
    if manifest.get("status") != "passed" or not manifest.get("signature_verified"):
        raise ValueError("There is no verified signed build.")
    if manifest["source"] != source_identity():
        raise ValueError("Source changed since the signed build. Build again before installing/launching.")
    app = Path(manifest["app"])
    if not app.is_dir() or tree_digest(app) != manifest["app_tree_sha256"]:
        raise ValueError("The app artifact changed since signing verification. Build again.")
    return app


def build(values, prefix):
    before = source_identity()
    derived = ROOT / os.environ.get("IOS_DEVICE_DERIVED_DATA_PATH", ".scratch/DerivedData-device")
    run(["xcodegen", "generate"], Path(str(prefix) + "-project.log"))
    run(["xcodebuild", "build", "-scheme", values["scheme"], "-destination", "generic/platform=iOS",
         "-derivedDataPath", str(derived), "-quiet"], Path(str(prefix) + "-build.log"))
    app = derived / "Build/Products/Debug-iphoneos" / (values["scheme"] + ".app")
    run([sys.executable, "scripts/audit/built-app.py", str(app)], Path(str(prefix) + "-bundle.log"))
    run(["codesign", "--verify", "--deep", "--strict", str(app)], Path(str(prefix) + "-signature.log"))
    if before != source_identity():
        raise ValueError("Source changed during the device build. Rebuild the final source.")
    with (app / "Info.plist").open("rb") as stream:
        info = plistlib.load(stream)
    manifest = {"status": "passed", "at": datetime.now(timezone.utc).isoformat(),
                "source": before, "app": str(app), "app_tree_sha256": tree_digest(app),
                "bundle": info["CFBundleIdentifier"], "version": info["CFBundleShortVersionString"],
                "build": info["CFBundleVersion"], "signature_verified": True}
    path = Path(str(prefix) + "-build.json")
    write(path, manifest)
    write(LOGS / "device-last-build.json", {"manifest": str(path)})
    return path


def install_or_launch(command, values, prefix):
    device = os.environ.get("IOS_DEVICE_ID")
    if not device:
        raise ValueError("Set IOS_DEVICE_ID from xcrun devicectl list devices.")
    pointer = json.loads((LOGS / "device-last-build.json").read_text())
    build_path = Path(pointer["manifest"])
    manifest = json.loads(build_path.read_text())
    app = verified_build(manifest)
    run(["codesign", "--verify", "--deep", "--strict", str(app)], Path(str(prefix) + "-signature.log"))
    if command == "launch":
        installed = json.loads((LOGS / "device-last-install.json").read_text())
        if installed.get("build_manifest") != str(build_path) or installed.get("device") != device:
            raise ValueError("Install this exact signed build on this device before launching.")
        args = ["xcrun", "devicectl", "device", "process", "launch", "--device", device, values["bundle"]]
    else:
        args = ["xcrun", "devicectl", "device", "install", "app", "--device", device, str(app)]
    run(args, Path(str(prefix) + f"-{command}.log"))
    report = {"status": "passed", "at": datetime.now(timezone.utc).isoformat(), "device": device,
              "build_manifest": str(build_path), "app_tree_sha256": manifest["app_tree_sha256"],
              "source": manifest["source"], "operation": command,
              "unverified": ["physical interaction", "VoiceOver", "live services", "accuracy"]}
    path = Path(str(prefix) + f"-{command}.json")
    write(path, report)
    if command == "install":
        write(LOGS / "device-last-install.json", report)
    return path


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command not in {"build", "install", "launch"}:
        sys.exit("Usage: device.sh build|install|launch")
    LOGS.mkdir(parents=True, exist_ok=True)
    prefix = LOGS / f"device-{datetime.now():%Y%m%d-%H%M%S-%f}"
    values = config()
    path = build(values, prefix) if command == "build" else install_or_launch(command, values, prefix)
    print(f"{command} passed. Evidence: {path}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        sys.exit(f"Device step failed: {error}")
