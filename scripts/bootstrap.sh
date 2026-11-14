#!/usr/bin/env bash
# bootstrap.sh "Cool App" com.example.coolapp TEAM_OR_DASH [minimum-ios] [--no-git]
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/bootstrap.py "$@"
