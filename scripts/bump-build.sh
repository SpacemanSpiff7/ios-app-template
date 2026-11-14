#!/usr/bin/env bash
# Bump CURRENT_PROJECT_VERSION (+1) and optionally MARKETING_VERSION in project.yml, then regenerate.
set -euo pipefail
cd "$(dirname "$0")/.."
cur=$(grep -E '^\s*CURRENT_PROJECT_VERSION:' project.yml | grep -oE '[0-9]+')
next=$((cur + 1))
sed -i '' -E "s/(CURRENT_PROJECT_VERSION: \")[0-9]+(\")/\1${next}\2/" project.yml
if [[ "${1:-}" == "--marketing" ]]; then
  sed -i '' -E "s/(MARKETING_VERSION: \")[^\"]+(\")/\1${2:?version}\2/" project.yml
fi
xcodegen generate >/dev/null
echo "build $cur → $next $( [[ "${1:-}" == "--marketing" ]] && echo "· marketing ${2}" )"
