---
name: new-screen
description: Add a native SwiftUI screen with state ownership, navigation, draft behavior and accessible controls. Use for a new screen or view.
argument-hint: <ScreenName> <FeatureModule>
---
1. Read the linked spec, DESIGN.md and EDITING.md. Extend an existing feature target unless a new boundary is needed.
2. Create a view with a body under 60 lines; split sections/subviews. Reuse a stack-free content view when a screen
   may be pushed and presented. Add previews for empty, populated, editing and failure states.
3. Delegate operations to the owning @Observable store. Add the route or one sheet(item:) destination case.
4. Use native controls. Reuse NumericFieldRow, .withKeyboardToolbar(), PrimaryActionBar and fullRowHitTarget()
   where they fit. Keep the primary action reachable after the first item exists.
5. Apply EDITING.md to Save/Cancel, dirty dismissals and nested Apply. Supply an accessibility label for icon-only
   controls and a stable identifier for the primary action when interaction tests use it.
6. Test the introduced logic and persistence boundaries; avoid empty stubs. Run the full gate and inspect
   normal/AX3, light/dark. Exercise the task if an interaction driver is available; report unverified behavior.
