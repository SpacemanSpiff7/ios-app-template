#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
for audit in file-size a11y-labels design-tokens; do
  scripts/audit/"$audit".sh
done
python3 scripts/audit/project-settings.py
