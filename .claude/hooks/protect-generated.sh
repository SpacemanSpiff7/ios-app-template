#!/bin/bash
# PreToolUse(Edit|Write): refuse edits to generated / single-source-of-truth files.
set -u
input=$(cat)
path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null) || exit 0
case "$path" in
  *.pbxproj|*.xcworkspacedata|*/Info.plist|*.entitlements)
    echo "BLOCKED: $path is generated from project.yml. Edit project.yml and run 'xcodegen generate'." >&2
    exit 2 ;;
  *Package.resolved)
    echo "BLOCKED: Package.resolved is managed by Xcode/SwiftPM." >&2
    exit 2 ;;
esac
exit 0
