# __APP_NAME__ iOS

<!-- Keep under 150 lines. File-specific rules live in .claude/rules/; knowledge lives in docs/. -->

## Identity
- __ONE_LINE_PRODUCT_DESCRIPTION__ (product truth: docs/PRODUCT.md).
- SwiftUI + SwiftData, local-first. Toolchain: project.yml and Packages/AppKit/Package.swift.
- XcodeGen owns targets, plist keys, entitlements and versions. Edit project.yml, then regenerate.
- .scratch/ holds logs, screenshots and reports. Git history holds completed work.

## Scope and YAGNI
- Deliver the requested behavior and agreed UI with the smallest complete change; routine work stays autonomous.
- Limit visible copy, sections, summaries, controls and flows to requested or approved UI and essentials for
  the requested functionality or accessibility. Explanatory copy and convenience summaries are optional.
- Propose optional additions separately and implement them after the user accepts them; keep authorized work moving.
- Treat requested removals as lasting decisions; reintroduce them only when the user asks.
- YAGNI: build for current requirements. Add abstractions, infrastructure, configurability and validation only
  for a concrete current need; leave speculative future use cases as proposals.
- Before compliance, legal, platform or security obligations justify extra code, validators, gates or process,
  identify the current authoritative requirement and why the app's actual behavior makes it applicable.
  Distinguish verified requirements from recommendations and unresolved assumptions.
- Match verification to changed behavior and concrete failure modes. Reuse existing checks, complete applicable
  required gates, and add or broaden checks when the change, a failure or an unresolved concrete risk warrants it.
- Review the visible result and diff against the request; each UI addition or new system needs that basis.

## Boundaries
- App/: entry point, navigation and dependency wiring.
- Packages/AppKit/: Core → nothing; Domain/Persistence → Core; DesignSystem → SwiftUI/UIKit.
- Features/* → Core, Domain, DesignSystem, plus Persistence when the feature owns storage.
- Value models cross boundaries as Sendable structs; SwiftData @Model stays inside Persistence.
- @Observable stores own operations. Views present state and delegate actions.
- Add a protocol when a second conformer needs it; test fakes count.
- App/UI targets default to MainActor; Core/Domain/Persistence default to nonisolated.
- Use static async @concurrent functions with parameters for heavy parsing, I/O and computation.
- NavigationPath reset: path = NavigationPath(). Presented and pushed content share a stack-free content view.

## Read when relevant
- Every task: docs/STATUS.md, docs/BACKLOG.md and the linked spec. Product decisions: docs/PRODUCT.md.
- UI: docs/DESIGN.md and .claude/rules/design-system.md. Motion: docs/DELIGHT.md.
- Tests/builds/scripts: .claude/rules/testing.md. Storage: .claude/rules/swiftdata.md.
- Network/long-running work: docs/ASYNC_WORK.md. Draft editing: docs/EDITING.md.
- New Apple APIs: docs/api/README.md; ground signatures in installed SDK interfaces or existing code.
- Release/device deployment: docs/RELEASE.md. Visible renames: .claude/rules/rename-verification.md.
- Corrections or changed rules: /docs-debrief; durable traps: docs/GOTCHAS.md.
- First use of the template: README.md and /setup.

## Native defaults
- Use system controls, semantic colors, system text styles, SF Symbols and Dynamic Type.
- A screen has one prominent primary action. Use PrimaryActionBar for a bottom action.
- NumericFieldRow and .withKeyboardToolbar() provide shared number entry and keyboard navigation.
- Reuse an existing component before adding one. Extend the closest component rather than forking.
- Custom branding is a product choice recorded in DESIGN.md and an ADR, including scoped lint changes.
- Icon-only controls have accessibility labels and 44-point targets; inspect normal/AX3, light/dark.

## Budgets
- File ≤ 400 lines (error 600), type ≤ 250 (error 350), function ≤ 40 (error 80).
- SwiftUI body > 60 lines: extract subviews. Split source rather than excluding it from lint.
- Swift Testing only. File-backed SwiftData app-host tests retain the container and serialize suites.

## Workflow
1. Read the current status, product contract and acceptance criteria; choose the smallest coherent change.
2. State the files, observable behavior and verification. Implement the authorized scope to completion.
3. Establish the primary task early: entry, input, review, Save, edit and recovery, in empty and populated states.
4. Run scripts/test-gate.sh. One build/simulator driver at a time; only the orchestrator runs Xcode builds.
5. Inspect UI at normal/AX3, light/dark. Interaction and VoiceOver checks are separate from rendered images.
6. Review the diff against the spec and boundaries. When delegated review is available, use a fresh read-only
   post-task-review agent; UI work also uses design-critic on actual screenshots. Fix concrete findings.
7. Capture lessons and remove invalidated guidance; update BACKLOG/STATUS at the verified milestone.
8. Report changes, evidence and remaining gates. Commit only when requested or authorized by project workflow.

Work through the user's authorized scope without per-task approval stops. If they request review between steps,
use that review cadence. Ask only for a missing decision, expanded scope or required external authorization.
Parallel workers implement disjoint briefs; the orchestrator integrates and verifies, with no parallel Xcode builds.

## Guardrails
- Never edit generated pbxproj, Info.plist or entitlements; declare them in project.yml.
- Use xcodebuild for the iOS package, not swift build/test.
- Use @Observable, not ObservableObject/@Published. Link SwiftData relationships after insertion.
- Avoid @Attribute(.unique) in CloudKit-compatible schemas.
- Preserve drafts on validation/save failure. Add/Save is the persistence boundary.
- Never rm -rf, git reset --hard, git clean or git push. Move retired files to .scratch/trash/.
- Repository changes cannot establish signing, Apple-portal, physical-device, purchase or submission gates.
- Conventional commit subjects explain intent. A rename must change the visible label and be inspected.
