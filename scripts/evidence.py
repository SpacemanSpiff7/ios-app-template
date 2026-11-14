#!/usr/bin/env python3
"""Capture/check source identity or finish a successful gate manifest."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from source_identity import source_identity, tree_digest

command, path, *extra = sys.argv[1:]
path = Path(path)
if command == "capture":
    path.write_text(json.dumps(source_identity(), indent=2) + "\n")
elif command == "check":
    if json.loads(path.read_text()) != source_identity():
        sys.exit("Source changed after verification/build. Re-run the gate/build before claiming or installing it.")
elif command == "gate":
    before_path, result, report, app = extra
    before = json.loads(Path(before_path).read_text())
    if before != source_identity():
        sys.exit("Source changed during the gate; this run cannot verify the final source.")
    path.write_text(json.dumps({
        "status": "passed", "at": datetime.now(timezone.utc).isoformat(), "source": before,
        "result_bundle": str(Path(result).resolve()), "tests": json.loads(Path(report).read_text()),
        "built_app": str(Path(app).resolve()), "app_tree_sha256": tree_digest(Path(app)),
        "checks": ["xcodebuild test", "structured xcresult", "built app", "strict lint", "audits", "tool contracts"],
        "unverified": ["signed device build", "device interaction", "VoiceOver", "live services", "accuracy"],
    }, indent=2) + "\n")
else:
    sys.exit("Usage: evidence.py capture|check|gate path [gate arguments]")
