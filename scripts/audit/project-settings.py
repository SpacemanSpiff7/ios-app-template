#!/usr/bin/env python3
"""Inspect actual generated target settings, not only project-level intentions."""
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project_config import ROOT, config

values = config()
project = ROOT / f"{values['scheme']}.xcodeproj/project.pbxproj"
data = json.loads(subprocess.check_output(["plutil", "-convert", "json", "-o", "-", str(project)]))
objects = data["objects"]
project = objects[data["rootObject"]]
project_configs = {
    objects[key]["name"]: objects[key]["buildSettings"]
    for key in objects[project["buildConfigurationList"]]["buildConfigurations"]
}
checked = 0
for target in objects.values():
    if target.get("isa") != "PBXNativeTarget":
        continue
    if target.get("productType") not in {
        "com.apple.product-type.application", "com.apple.product-type.app-extension",
        "com.apple.product-type.bundle.unit-test", "com.apple.product-type.bundle.ui-testing",
    }:
        continue
    configs = objects[target["buildConfigurationList"]]["buildConfigurations"]
    for identifier in configs:
        settings = objects[identifier]["buildSettings"]
        if str(settings.get("TARGETED_DEVICE_FAMILY")) != "1":
            sys.exit(f"{target['name']}: set TARGETED_DEVICE_FAMILY=1 on the target in project.yml.")
        inherited = project_configs[objects[identifier]["name"]]
        minimum = settings.get("IPHONEOS_DEPLOYMENT_TARGET", inherited.get("IPHONEOS_DEPLOYMENT_TARGET"))
        if str(minimum) != values["minimum_ios"]:
            sys.exit(f"{target['name']}: generated deployment target differs from project.yml.")
        checked += 1
package = (ROOT / "Packages/AppKit/Package.swift").read_text()
if f'.iOS("{values["minimum_ios"]}")' not in package:
    sys.exit("Package.swift and project.yml minimum iOS differ.")
if not re.search(r"^// swift-tools-version: \d+\.\d+", package):
    sys.exit("Missing configured Swift tools version.")
if not (ROOT / "AGENTS.md").is_symlink() or (ROOT / "AGENTS.md").readlink() != Path("CLAUDE.md"):
    sys.exit("Restore AGENTS.md -> CLAUDE.md.")
if not checked:
    sys.exit("No generated iOS targets were inspected.")
print(f"Checked {checked} generated target configurations, package minimum and instruction symlink.")
