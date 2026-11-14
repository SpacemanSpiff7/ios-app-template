#!/bin/bash
# Advisory agent guard; scripts/with-ios-lock.sh enforces shared serialization.
set -u
input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty' 2>/dev/null) || exit 0
if printf '%s' "$cmd" | grep -Eq '(^|[[:space:]/])xcodebuild([[:space:]]|$)'; then
  if pgrep -x xcodebuild >/dev/null 2>&1; then
    echo "BLOCKED: another xcodebuild is running; wait for it to finish." >&2
    exit 2
  fi
fi
