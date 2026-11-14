#!/usr/bin/env bash
# destination | build | launch | shot [name] | ax3 | reset-text | dark | light
set -euo pipefail
cd "$(dirname "$0")/.."
if [ "${1:-}" = destination ]; then
  exec python3 scripts/simulator.py "$@"
fi
exec scripts/with-ios-lock.sh python3 scripts/simulator.py "$@"
