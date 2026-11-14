# Architecture

## Module graph

Core has value models and calculations, without UI imports.
Domain depends on Core. Persistence depends on Core and owns SwiftData records, schema and DTO mapping.
DesignSystem contains native UI controls without Core/Domain/Persistence dependencies.
Features depend on Core, Domain and DesignSystem; storage-owning features may also depend on Persistence.
App owns entry, root navigation and dependency wiring.

The Items example uses Core.Item, a private Persistence.ItemRecord, ItemRepository, HomeStore and ItemEditor.
ItemRepository owns a container and exposes values; HomeStore owns visible accepted state and save/delete actions.
The editor stages an ItemDraft until Save. Replace this example as one coherent product change.

## State and concurrency

Stores use @Observable; values cross boundaries as Sendable structs. Views delegate mutations to stores.
App/DesignSystem/Features default to MainActor; Core/Domain/Persistence default to nonisolated.
Persistence repository access is explicitly MainActor-bound. Parsing/heavy I/O uses async static @concurrent helpers.
See EDITING.md for transactions and ASYNC_WORK.md for cancellation, deadlines and diagnostics.

## Navigation and persistence

Use per-tab NavigationPath coordinators as the app gains tabs. Reset via path = NavigationPath().
Presented wrappers own NavigationStack; pushed content does not nest one.
Register every @Model in AppSchema.current; insert before assigning relationships.
Version migrations deliberately and preserve user snapshots/history rather than rewriting them on lookup changes.

## Adding a feature

Spec its primary task in PRODUCT/BACKLOG before adding targets. Update Package.swift and project.yml together.
Compile the interface before parallel implementation; workers own disjoint file briefs and do not run Xcode builds.
Regenerate with XcodeGen, run the full gate, and update this graph when a real boundary changes.
