#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys
from project_config import ROOT, config
from test_results import check, declarations

parser = argparse.ArgumentParser(description="Validate full Swift test execution from structured xcresult.")
parser.add_argument("bundle")
parser.add_argument("summary")
parser.add_argument("tree")
parser.add_argument("--output", required=True)
args = parser.parse_args()
try:
    report = check(declarations(ROOT, config()["scheme"] + "Tests"),
                   json.loads(Path(args.summary).read_text()), json.loads(Path(args.tree).read_text()))
except ValueError as error:
    sys.exit(f"Incomplete gate: {error}\nInspect {args.bundle}")
Path(args.output).write_text(json.dumps(report, indent=2) + "\n")
print(f"{report['declared_tests']} declared/passed tests, {report['executions']} executions; zero failures/skips.")
