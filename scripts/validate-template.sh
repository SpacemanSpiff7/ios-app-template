#!/usr/bin/env bash
# Fresh-app check: excludes caches, generated projects and local evidence.
set -euo pipefail
cd "$(dirname "$0")/.."
grep -q '__APP_NAME__' project.yml || { echo "Run this from the source template, not a configured app."; exit 1; }
mkdir -p .scratch/template-validation
sample="$PWD/.scratch/template-validation/$(date +%Y%m%d-%H%M%S)-$$/app"
python3 - "$PWD" "$sample" <<'PY'
from pathlib import Path
import shutil
import sys
source, destination = map(Path, sys.argv[1:])
shutil.copytree(source, destination, symlinks=True,
                ignore=shutil.ignore_patterns(".git", ".scratch", ".build", "DerivedData", "__pycache__",
                                              "*.xcodeproj", "Info.plist", "*.entitlements", ".template-origin.json"))
PY
(
  cd "$sample"
  args=("TemplateCheck" "com.example.templatecheck" "-")
  if [ -n "${IOS_TEMPLATE_MIN_IOS:-}" ]; then args+=("$IOS_TEMPLATE_MIN_IOS"); fi
  IOS_TEMPLATE_SOURCE="$OLDPWD" scripts/bootstrap.sh "${args[@]}" --no-git
  scripts/test-gate.sh
)
printf 'Fresh sample verified: %s\n' "$sample"
