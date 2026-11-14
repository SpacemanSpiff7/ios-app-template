---
paths:
  - "AppTests/**"
  - "Packages/AppKit/Tests/**"
  - "scripts/**"
---
# Tests and builds

- Full gate: scripts/test-gate.sh. It regenerates, tests, checks structured xcresult, then strict lint and audits.
- Quick compile/install: scripts/sim.sh build. Logs and DerivedData remain in .scratch/.
- scripts/sim.sh destination selects an available compatible iOS simulator; override IOS_SIMULATOR_ID explicitly.
- Use xcodebuild for iOS. One build or simulator driver at a time; workers never run builds.
- A focused -only-testing:<Target>/<SuiteStructName> run is diagnostic, not the full gate.
- Success banners/checkmarks are not execution evidence. Inspect test identities, failures, skips and executions
  from xcresult; the gate rejects missing declarations and unexpected/missing identities.
- Use Swift Testing (@Test/#expect/#require). Keep parameterized executions distinct from test declarations.
- Add meaningful tests for new logic; avoid empty stubs and tests that restate low-impact implementation.
- Coverage goals: models 95%, logic 90%, stores 85%, views 70%; report measured coverage separately.
- App-host SwiftData tests use FileBackedContainer, retain the container and use @Suite(.serialized).
  Run with -parallel-testing-enabled NO. Register every model via Schema(AppSchema.current.models).
- Regenerate after project.yml changes. Use fresh DerivedData when evidence points to stale linked state;
  retain the failure log before replacing a cache.
- Entry/plist/extension change: build, install, launch, capture and inspect. scripts/audit/project-settings.py
  checks generated targets; scripts/audit/built-app.py checks the built identifier and UIDeviceFamily.
- Render/screenshot checks do not prove keyboard, VoiceOver, live service, signature or physical-device behavior.
