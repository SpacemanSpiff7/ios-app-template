#!/bin/bash
# Advisory reminder; never introduces a per-task approval gate.
set -u
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
git rev-parse --show-toplevel >/dev/null 2>&1 || exit 0
changed=$(git status --porcelain 2>/dev/null | grep -E '\.swift$' | wc -l | tr -d ' ')
[ "$changed" = "0" ] && exit 0
cat <<MSG
Definition of done ($changed Swift files changed):
  [ ] scripts/test-gate.sh with structured results and source evidence
  [ ] UI images inspected at normal/AX3, light/dark; interaction limits stated
  [ ] diff reviewed, concrete findings fixed; lessons and current status updated
MSG
