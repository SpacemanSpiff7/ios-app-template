#!/usr/bin/env python3
"""Verify the final built bundle and all embedded extensions."""
from pathlib import Path
import plistlib
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_config import config

app = Path(sys.argv[1])
bundles = [app, *sorted(app.glob("PlugIns/*.appex"))]
for index, bundle in enumerate(bundles):
    with (bundle / "Info.plist").open("rb") as stream:
        info = plistlib.load(stream)
    if info.get("UIDeviceFamily") != [1]:
        sys.exit(f"{bundle}: expected iPhone-only UIDeviceFamily [1], got {info.get('UIDeviceFamily')}.")
    if index == 0 and info.get("CFBundleIdentifier") != config()["bundle"]:
        sys.exit(f"{bundle}: unexpected bundle identifier.")
    for key in ("CFBundleDisplayName", "CFBundleVersion", "CFBundleShortVersionString"):
        if not info.get(key):
            sys.exit(f"{bundle}: missing {key}.")
print(f"Checked identity, versions and UIDeviceFamily in {len(bundles)} built bundle(s).")
