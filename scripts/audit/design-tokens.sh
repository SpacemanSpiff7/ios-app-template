#!/usr/bin/env bash
# Native defaults: semantic colors/text styles; standard button styles are allowed.
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 scripts/audit/native-style.py
