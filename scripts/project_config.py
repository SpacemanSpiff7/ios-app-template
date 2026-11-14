"""Read the small, generated identity fields without adding a YAML dependency."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def config():
    text = (ROOT / "project.yml").read_text()
    patterns = {
        "scheme": r"^name:\s*([^\n]+)",
        "bundle": r"PRODUCT_BUNDLE_IDENTIFIER:\s*([^\n]+)",
        "minimum_ios": r"iOS:\s*([^\n]+)",
    }
    result = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.MULTILINE)
        if not match:
            raise ValueError(f"Missing {key} in project.yml")
        value = match[1].strip().strip('"').strip("'")
        if "__" in value:
            raise ValueError("Run scripts/bootstrap.sh on a fresh copy first.")
        result[key] = value
    return result
