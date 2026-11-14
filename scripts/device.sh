#!/usr/bin/env bash
# build | install | launch. Set IOS_DEVICE_ID for install/launch.
set -euo pipefail
cd "$(dirname "$0")/.."
exec scripts/with-ios-lock.sh python3 scripts/device_helper.py "$@"
