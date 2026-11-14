#!/usr/bin/env python3
"""Static subset of native style checks; custom branding requires scoped policy changes."""
from pathlib import Path
import re
import sys

checks = {
    "Use a semantic system color": r"Color\(\s*(?:red:|hex:|\.sRGB)|#colorLiteral",
    "Use a system text style": r"\.font\(\s*\.system\(\s*size:|Font\.custom\(|UIFont\(name:",
}
failed = []
for root in ("App", "Packages/AppKit/Sources"):
    for path in Path(root).rglob("*.swift"):
        for label, pattern in checks.items():
            for match in re.finditer(pattern, path.read_text()):
                line = path.read_text().count("\n", 0, match.start()) + 1
                failed.append(f"{path}:{line}: {label}")
print("\n".join(failed) if failed else "Native color/type checks passed.")
sys.exit(bool(failed))
