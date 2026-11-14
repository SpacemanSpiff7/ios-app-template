#!/bin/bash
# PostToolUse(Edit|Write): advisory SwiftLint on the edited file. Always exit 0.
set -u
input=$(cat)
command -v swiftlint >/dev/null 2>&1 || exit 0
path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null) || exit 0
[[ "$path" == *.swift && -f "$path" ]] || exit 0
swiftlint lint --quiet "$path" 2>&1 | head -40 || true
lines=$(wc -l < "$path" | tr -d ' ')
[ "$lines" -gt 400 ] && echo "NOTE: $path is $lines lines (> 400 budget). Split before finishing this task."
exit 0
