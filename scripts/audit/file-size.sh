#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 - "$@" <<'PY'
from pathlib import Path
import sys
files = [Path(value) for value in sys.argv[1:]] or [
    path for root in ("App", "AppTests", "Packages/AppKit/Sources", "Packages/AppKit/Tests")
    for path in Path(root).rglob("*.swift")
]
failed = False
for path in files:
    count = len(path.read_text().splitlines())
    if count > 600:
        print(f"{path}: {count} lines; split the file (maximum 600).")
        failed = True
sys.exit(failed)
PY
