#!/usr/bin/env python3
"""Validate first, configure a copied template, and verify its generated targets."""
import argparse
from datetime import date
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".scratch", ".build", "DerivedData", "__pycache__", "scripts"}


def run(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()


def version(text, pattern):
    match = re.search(pattern, text)
    if not match:
        raise ValueError(f"Cannot detect toolchain from: {text}")
    return match[1]


def prepare(args):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9 _-]*", args.name):
        raise ValueError("App name must start with a letter and contain letters, numbers, spaces, _ or -.")
    name = re.sub(r"[^A-Za-z0-9]", "", args.name)
    if not re.fullmatch(r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", args.bundle):
        raise ValueError("Use a reverse-DNS bundle identifier, such as com.example.coolapp.")
    if args.team != "-" and not re.fullmatch(r"[A-Z0-9]{10}", args.team):
        raise ValueError("Team must be a 10-character identifier, or - for simulator-only work.")
    required = ["xcodebuild", "xcrun", "xcodegen", "swiftlint", "jq"]
    if not args.no_git:
        required.append("git")
    missing = [tool for tool in required if not shutil.which(tool)]
    if missing:
        raise ValueError("Install required tools first: " + ", ".join(missing))
    xcode = version(run("xcodebuild", "-version"), r"Xcode (\d+\.\d+)")
    swift = version(run("xcrun", "swift", "-version"), r"Swift version (\d+\.\d+)")
    sdk = run("xcrun", "--sdk", "iphonesimulator", "--show-sdk-version")
    minimum = args.minimum or sdk.split(".")[0] + ".0"
    if not re.fullmatch(r"\d+\.\d+", minimum):
        raise ValueError("Minimum iOS must be major.minor, for example 26.0.")
    pair = lambda text: tuple(int(part) for part in text.split(".")[:2])
    if pair(swift) < (6, 2) or pair(minimum) < (26, 0) or pair(minimum) > pair(sdk):
        raise ValueError(f"Requires Swift >= 6.2 and 26.0 <= minimum iOS <= installed SDK {sdk}.")
    agents = ROOT / "AGENTS.md"
    if agents.is_symlink() and os.readlink(agents) != "CLAUDE.md":
        raise ValueError("AGENTS.md must link to CLAUDE.md; preserve the existing custom instructions.")
    if agents.exists() and not agents.is_symlink() and agents.read_bytes() != (ROOT / "CLAUDE.md").read_bytes():
        raise ValueError("AGENTS.md has independent instructions; reconcile it before bootstrap.")
    existing = ROOT / ".template-origin.json"
    identity = {"name": name, "display_name": args.name, "bundle": args.bundle, "team": args.team,
                "minimum_ios": minimum, "xcode": xcode, "swift_tools": swift}
    if existing.exists():
        previous = json.loads(existing.read_text())
        if any(previous.get(key) != value for key, value in identity.items()):
            raise ValueError("This copy is already configured. Change its project.yml explicitly or use a fresh copy.")
    elif "__APP_NAME__" not in (ROOT / "project.yml").read_text():
        raise ValueError("Project is already configured without bootstrap metadata; use a fresh template copy.")
    return identity


def configure(identity, args):
    replacements = {
        "__APP_NAME__": identity["name"], "__DISPLAY_NAME__": identity["display_name"],
        "__BUNDLE_ID__": identity["bundle"], "__BUNDLE_PREFIX__": identity["bundle"].rsplit(".", 1)[0],
        "__TEAM_ID__": "" if identity["team"] == "-" else identity["team"],
        "__MIN_IOS__": identity["minimum_ios"], "__XCODE_VERSION__": identity["xcode"],
        "__SWIFT_TOOLS_VERSION__": identity["swift_tools"], "__URL_SCHEME__": identity["name"].lower(),
        "__DATE__": date.today().isoformat(),
    }
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if path.is_symlink() or not path.is_file() or any(p in SKIP or p.endswith(".xcodeproj") for p in relative.parts):
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        changed = text
        for token, value in replacements.items():
            changed = changed.replace(token, value)
        if changed != text:
            path.write_text(changed)
    agents = ROOT / "AGENTS.md"
    if not agents.is_symlink():
        if agents.exists():
            agents.unlink()
        agents.symlink_to("CLAUDE.md")
    candidate = args.template_source or os.environ.get("IOS_TEMPLATE_SOURCE")
    origin = ROOT / ".template-origin.json"
    if not candidate and origin.exists():
        candidate = json.loads(origin.read_text()).get("source_template")
    sibling = ROOT.parent / "ios-app-template"
    if not candidate and sibling.is_dir() and sibling != ROOT:
        candidate = str(sibling)
    metadata = dict(identity, template="ios-app-template", revision="2026-11-13",
                    source_template=str(Path(candidate).resolve()) if candidate else None)
    (ROOT / ".template-origin.json").write_text(json.dumps(metadata, indent=2) + "\n")
    for folder in ("scripts", ".claude/hooks"):
        for path in (ROOT / folder).rglob("*"):
            if path.is_file() and (path.suffix in {".sh", ".py"} or path.name == "pre-commit"):
                path.chmod(path.stat().st_mode | 0o111)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name")
    parser.add_argument("bundle")
    parser.add_argument("team", nargs="?", default="-")
    parser.add_argument("minimum", nargs="?")
    parser.add_argument("--no-git", action="store_true")
    parser.add_argument("--template-source")
    args = parser.parse_args()
    try:
        identity = prepare(args)
        configure(identity, args)
        if not args.no_git:
            if not (ROOT / ".git").exists():
                subprocess.run(["git", "init", "-q"], cwd=ROOT, check=True)
            subprocess.run(["git", "config", "--local", "core.hooksPath", "scripts/git-hooks"], cwd=ROOT, check=True)
        print(run("xcodegen", "generate"))
        subprocess.run([sys.executable, "scripts/audit/project-settings.py"], cwd=ROOT, check=True)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        sys.exit(f"Bootstrap failed: {error}")
    print(f"Configured {identity['name']}: Xcode {identity['xcode']}, Swift {identity['swift_tools']}, "
          f"iOS {identity['minimum_ios']}. Next: scripts/test-gate.sh")


if __name__ == "__main__":
    main()
