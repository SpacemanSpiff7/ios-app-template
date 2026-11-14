# ios-app-template

A native SwiftUI + SwiftData starter, distilled from Airlock, CurlBro and CalorieTracker.
It includes a small persistent Items example, shared editing controls, layered SPM targets, XcodeGen,
strict lint and a test gate that checks structured execution results.

## Start an app

1. Copy this folder into your new project directory.
2. Install Xcode, Python 3, xcodegen, swiftlint and jq.
3. Run `scripts/bootstrap.sh "Cool App" com.example.coolapp YOUR_TEAM_ID`.
   Use `-` as the team for simulator-only work. An optional fourth argument selects minimum iOS.
4. Run `scripts/test-gate.sh`, then `scripts/sim.sh build` and `scripts/sim.sh launch`.
5. Fill PRODUCT.md and use /setup to resolve remaining product choices, then replace the Items example.

Bootstrap detects the installed Xcode, Swift and iOS SDK. The default minimum is the installed SDK's major
version; the shared controls require iOS 26 or later and Swift tools 6.2 or later. It validates all inputs before
writing, preserves AGENTS.md → CLAUDE.md, and checks the generated target settings. It does not install tools.

## Defaults and choices

Native system controls, semantic colors, Dynamic Type and one prominent action are the default.
Custom branding is optional: record the decision and its narrow style/lint changes in docs/DESIGN.md.
The user's requested scope and review cadence govern the workflow; there is no automatic stop after each task.
The sample demonstrates a stored item, an unsaved editor, Save/Cancel, number entry and a persistent Add action.

## Main entry points

| Path | Purpose |
|---|---|
| CLAUDE.md / AGENTS.md | Short project contract, shared by agent tools |
| LESSONS.md | Evidence behind the defaults |
| project.yml | Project, signing, plist and version configuration |
| Packages/AppKit | Core, Domain, Persistence, DesignSystem and feature targets |
| docs/README.md | Product, editing, asynchronous work and verification contracts |
| scripts/test-gate.sh | Build/test, structured xcresult, lint, audits and source evidence |
| scripts/sim.sh | Explicit simulator selection, build/install, launch and captures |
| scripts/device.sh | Signed build, artifact/source verification, install and launch evidence |
| scripts/validate-template.sh | Generate a fresh sample, verify bootstrap and run its full gate |
| .claude/skills/docs-debrief | Capture corrections and propose reusable changes to this template |

Run `scripts/validate-template.sh` before distributing a template update. It copies only source files to a
fresh directory under .scratch/, uses simulator-only signing, and retains the generated app and verification logs.
CI validates a fresh copy in the source template and runs the full gate directly in configured apps.
Python tooling contracts run with `python3 -m unittest discover -s scripts/tests`.

## Replacing the example

Keep or rename the Core item, Persistence record/repository, HomeStore, HomeView and ItemEditor together.
Follow the primary-task checklist in PRODUCT.md before expanding the app. The reusable controls contain no
food, provider or nutrition behavior. Add modules or dependencies when the product needs them.
