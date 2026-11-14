#!/usr/bin/env python3
"""Select a compatible explicit device; keep build, install and launch failures distinct."""
from datetime import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from project_config import ROOT, config


def select_device(devices, minimum, requested=None):
    candidates = []
    version = lambda value: tuple(int(p) for p in value.split("."))
    for runtime, rows in devices.items():
        match = re.search(r"iOS-(\d+)-(\d+)", runtime)
        if not match or (int(match[1]), int(match[2])) < version(minimum):
            continue
        for row in rows:
            if row.get("isAvailable") and row.get("deviceTypeIdentifier", "").split(".")[-1].startswith("iPhone"):
                candidates.append(row)
    if requested:
        return next((d for d in candidates if d["udid"] == requested), None)
    candidates.sort(key=lambda row: (row.get("state") != "Booted", row["name"], row["udid"]))
    return candidates[0] if candidates else None


def run(*args, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, **kwargs)


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command not in {"destination", "build", "launch", "shot", "ax3", "reset-text", "dark", "light"}:
        sys.exit("Usage: sim.sh destination|build|launch|shot [name]|ax3|reset-text|dark|light")
    values = config()
    data = json.loads(subprocess.check_output(["xcrun", "simctl", "list", "devices", "available", "-j"]))
    device = select_device(data["devices"], values["minimum_ios"], os.environ.get("IOS_SIMULATOR_ID"))
    if not device:
        sys.exit("No compatible available iPhone simulator; install a runtime or set IOS_SIMULATOR_ID.")
    udid = device["udid"]
    if command == "destination":
        print(f"platform=iOS Simulator,id={udid}")
        return
    if device["state"] != "Booted":
        run("xcrun", "simctl", "boot", udid)
    run("xcrun", "simctl", "bootstatus", udid, "-b", stdout=subprocess.DEVNULL)
    logs = ROOT / ".scratch/logs"
    logs.mkdir(parents=True, exist_ok=True)
    derived = Path(os.environ.get("IOS_DERIVED_DATA_PATH", ".scratch/DerivedData-sim"))
    if command == "build":
        run("xcodegen", "generate", stdout=subprocess.DEVNULL)
        with (logs / "simulator-build.log").open("w") as stream:
            run("xcodebuild", "build", "-scheme", values["scheme"], "-destination",
                f"platform=iOS Simulator,id={udid}", "-derivedDataPath", str(derived),
                "-quiet", "CODE_SIGNING_ALLOWED=NO", stdout=stream, stderr=subprocess.STDOUT)
        app = derived / "Build/Products/Debug-iphonesimulator" / (values["scheme"] + ".app")
        run(sys.executable, "scripts/audit/built-app.py", str(app))
        run("xcrun", "simctl", "install", udid, str(app))
    elif command == "launch":
        subprocess.run(["xcrun", "simctl", "terminate", udid, values["bundle"]], capture_output=True)
        run("xcrun", "simctl", "launch", udid, values["bundle"])
    elif command == "shot":
        name = sys.argv[2] if len(sys.argv) > 2 else "screen"
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
            sys.exit("Screenshot name may contain only letters, numbers, _ and -.")
        path = ROOT / ".scratch/shots" / f"{name}-{datetime.now():%Y%m%d-%H%M%S}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        run("xcrun", "simctl", "io", udid, "screenshot", str(path))
        print(path)
    else:
        options = {"ax3": ("content_size", "accessibility-extra-large"),
                   "reset-text": ("content_size", "large"),
                   "dark": ("appearance", "dark"), "light": ("appearance", "light")}
        run("xcrun", "simctl", "ui", udid, *options[command])


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        sys.exit(f"Simulator command failed: {error}")
