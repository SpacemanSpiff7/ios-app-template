#!/usr/bin/env bash
# One shared lock across generated apps, CI commands, simulator and device helpers.
set -euo pipefail
exec python3 "$(dirname "$0")/ios-lock.py" "$@"
