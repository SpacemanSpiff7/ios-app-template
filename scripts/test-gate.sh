#!/usr/bin/env bash
# Full verification, serialized with all other template-generated iOS helpers.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ "${IOS_GATE_RUNNING:-}" != "$PWD" ]; then
  export IOS_GATE_RUNNING="$PWD"
  exec scripts/with-ios-lock.sh bash scripts/test-gate.sh "$@"
fi
if pgrep -x xcodebuild >/dev/null 2>&1; then
  echo "Another xcodebuild is active. Wait for it to finish." >&2; exit 1
fi
mkdir -p .scratch/logs
stamp="$(date +%Y%m%d-%H%M%S)-$$"
prefix=".scratch/logs/gate-$stamp"
result=".scratch/gate-$stamp.xcresult"
scheme=$(python3 scripts/project-config.py scheme)
derived=${IOS_DERIVED_DATA_PATH:-.scratch/DerivedData-gate}
destination=${IOS_TEST_DESTINATION:-$(scripts/sim.sh destination)}
python3 scripts/evidence.py capture "$prefix-source.json"
xcodegen generate > "$prefix-project.log" 2>&1
python3 scripts/audit/project-settings.py
if ! xcodebuild test -scheme "$scheme" -destination "$destination" -derivedDataPath "$derived" \
  -parallel-testing-enabled NO -collect-test-diagnostics never -resultBundlePath "$result" \
  -quiet CODE_SIGNING_ALLOWED=NO "$@" > "$prefix.log" 2>&1; then
  echo "Build/tests failed. See $prefix.log" >&2; exit 1
fi
xcrun xcresulttool get test-results summary --path "$result" --compact > "$prefix-summary.json"
xcrun xcresulttool get test-results tests --path "$result" --compact > "$prefix-tests.json"
python3 scripts/check-test-results.py "$result" "$prefix-summary.json" "$prefix-tests.json" --output "$prefix-check.json"
app="$derived/Build/Products/Debug-iphonesimulator/$scheme.app"
python3 scripts/audit/built-app.py "$app"
swiftlint lint --strict --no-cache > "$prefix-lint.log" 2>&1
scripts/audit/run-all.sh > "$prefix-audits.log" 2>&1
python3 -m unittest discover -s scripts/tests > "$prefix-contracts.log" 2>&1
python3 scripts/evidence.py gate "$prefix-verification.json" "$prefix-source.json" "$result" "$prefix-check.json" "$app"
printf 'Gate passed: %s\nEvidence: %s\n' "$result" "$prefix-verification.json"
