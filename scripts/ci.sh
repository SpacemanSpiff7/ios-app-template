#!/usr/bin/env bash
# Source templates validate a fresh copy; configured apps verify themselves.
set -euo pipefail
cd "$(dirname "$0")/.."
if grep -q '__APP_NAME__' project.yml; then
  exec scripts/validate-template.sh
fi
exec scripts/test-gate.sh
