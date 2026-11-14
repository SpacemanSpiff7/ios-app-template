---
paths:
  - "project.yml"
  - "docs/RELEASE.md"
  - "AppStore/**"
---
# Release rules
- Version/build live in project.yml. Bump with scripts/bump-build.sh, then regenerate; commit the source spec
  when authorized. The generated project stays ignored.
- Human gates (App Store Connect, signing, physical device, IAP sandbox) are cleared only with evidence recorded in `docs/RELEASE.md`. Never mark them done from repo state.
- Before every archive: run `docs/RELEASE.md` checklist top to bottom.
