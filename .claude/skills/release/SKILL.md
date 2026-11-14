---
name: release
description: Prepare a verified build and release evidence, then perform only authorized distribution actions. Use for TestFlight, shipping or submission.
argument-hint: [testflight|appstore]
---
1. Read RELEASE.md and the requested distribution scope. Complete all independent code, checks, metadata and
   reviewable release notes before asking for an external action or missing human-only evidence.
2. Bump version/build in project.yml when requested; regenerate. Run scripts/test-gate.sh and analyze.
3. Build with scripts/device.sh build; inspect its source/artifact manifest. Install and launch only within the
   authorized device scope. Keep signing, install, launch and actual feature interaction evidence distinct.
4. Walk every RELEASE gate. Record observed results, dates and manifest links; keep unavailable gates open.
   Request only the missing human-only step or authorization, explaining its source. Existing approval persists.
5. Present the exact source/build, verification, notes and open gates. Archive/upload/submit only if authorized.
