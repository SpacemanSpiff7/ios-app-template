# Gotchas — bugs already paid for

Each line: symptom → cause → rule. Add via `/docs-debrief`. Sources: CurlBro, Airlock and CalorieTracker (2026).

## SwiftUI
- Competing sheet presenters produce ambiguous presentation state. **Rule:** one `sheet(item:)` destination enum per presenter.
- `.swipeActions` / `.contextMenu` on a row nested inside a composite `List` row → SwiftUI stacks them onto the parent (doubled swipe buttons). **Rule:** the composite row owns the single action surface; children get long-press only.
- Keyboard `.toolbar` on a `TabView` silently dropped. **Rule:** needs a `NavigationStack` ancestor; attach once at the container level, never per row (one bar per visible row otherwise).
- `NavigationPath` has no `removeAll()`. **Rule:** coordinator `popToRoot()` sets `path = NavigationPath()`.
- `NavigationStack` inside a view that may be pushed inside another `NavigationStack`. **Rule:** content/wrapper split — wrapper adds the stack only when presented standalone.
- `@State` seeded from a model can desync on external updates. **Rule:** refresh clean drafts; preserve dirty drafts and detect conflicts at Save.
- Overlay positioned from the container size drifts when the keyboard rises. **Rule:** anchor from `GeometryProxy.safeAreaInsets`.
- `if isRunning || isFocused { TextField } else { Text }` → view-switch loop crash on focus. **Rule:** branch on one condition.
- Toolbar badge / count clipping in iOS 26. **Rule:** use the native `.badge()` on toolbar items.
- Custom button wrappers obscured standard behavior. **Rule:** native Button styles, one prominent action, shared PrimaryActionBar where appropriate.
- `.font(.system(size:))` and `Color(hex:)` do not adapt to Dynamic Type/dark mode. **Rule:** semantic system colors and text styles; lint errors.
- iOS 26 tab bar minimises on scroll; overlays attached to screen coordinates detach. **Rule:** attach tab-bar decorations to the UIKit tab button, or don't decorate the tab bar.

## SwiftData
- `modelContext.insert()` traps `EXC_BREAKPOINT` → a `@Model` missing from the schema. **Rule:** `Schema(AppSchema.current.models)` everywhere.
- In-memory container traps in the app-host test target. **Rule:** file-backed store per test (`FileBackedContainer`), cleanup `.store` `-shm` `-wal`.
- Fetch traps on first use in a test → container deallocated (repository holds only the context). **Rule:** helpers return the container; test keeps `_ = container`.
- `@Attribute(.unique)` breaks CloudKit. Relationship set in `init()` crashes. **Rule:** insert, then link.
- Parallel SwiftData test suites corrupt each other. **Rule:** `@Suite(.serialized)` + `-parallel-testing-enabled NO`.

## Build / tooling
- `xcodebuild -quiet` hides `** BUILD SUCCEEDED **`. **Rule:** check exit code + grep for `error:`.
- `** TEST SUCCEEDED **` can hide per-test crashes or missing execution. **Rule:** match structured xcresult identities to source declarations; reject failures/skips and count parameter executions separately.
- `-only-testing:` matches the suite **struct** name; function-level filters match nothing.
- `-scheme <TestTarget>` fails — test targets aren't schemes.
- Two parallel Xcode/simulator drives caused crashes. **Rule:** shared OS lock in build/simulator/device helpers; the agent hook is advisory.
- `swift build` on an iOS-only package builds for macOS and fails.
- Editing `Info.plist` by hand: XcodeGen overwrites it; keys vanish (`CFBundleDisplayName` in an extension → archive validation error). **Rule:** `project.yml` `info.properties` only.
- SourceKit "No such module 'UIKit'" in SPM sources is editor noise if `xcodebuild` succeeds. Don't `#if os(iOS)` it away.
- Worker builds interfered with integration. **Rule:** only the orchestrator runs Xcode builds, serially.
- Backticks / `\b` in `pgrep -f` patterns silently fail on macOS BSD tools. Use `([[:space:]]|$)`.

## Concurrency
- `@concurrent` on a sync function → compile error; on a MainActor instance method reading `self` → isolation error. **Rule:** `static` `@concurrent` funcs with parameters.
- Live Activity `startOrReplace` cancelling in-flight tasks kills an early-scheduled expiry. **Rule:** schedule expiry after the replace completes.

## App Review
- 2.5.1: capability declared (`UIRequiredDeviceCapabilities` / HealthKit) but feature not visible → rejection. Surface the feature or remove the capability.
- 2.1(b): IAP checkout error on reviewer device, twice, not reproducible locally. Human sandbox test on a physical device is a hard gate; ship Release-safe diagnostics.

## Process
- "rename X → Y" commit that only changed comments stranded work for weeks. **Rule:** grep visible strings + screenshot.
- Lint rules disabled "until a style sweep" never get re-enabled; excluded legacy files never get split. **Rule:** budgets on from commit 1, no exclusion list.
- Root CLAUDE.md grew to 44 KB. **Rule:** < 150 lines; `paths:`-scoped rules; nested module CLAUDE.md.

## CalorieTracker corrections — 2026-11-13
- Number fields had inconsistent focus/keyboard behavior and small targets. **Rule:** shared NumericFieldRow and keyboard toolbar; verify actual focus and VoiceOver separately from renders.
- A late result replaced a newer draft. **Rule:** operation revision guards and a stale-original check at Save.
- Fallbacks hid a rejected credential behind no results. **Rule:** preserve typed failures and recovery; Saved means local storage, not verified access.
- Nested timers used all recovery time. **Rule:** one shared deadline with an explicit attempt limit and recovery reserve.
- Optional malformed fields discarded usable results. **Rule:** validate independent fields at the boundary and retain useful values.
- An installed app predated the final patch. **Rule:** bind source and artifact fingerprints to build/install/launch evidence; rebuild when either changes.
- iPhone-only project settings were overridden by target presets. **Rule:** set the family on each target and inspect the built UIDeviceFamily.
