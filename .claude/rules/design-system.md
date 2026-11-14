---
paths:
  - "Packages/AppKit/Sources/DesignSystem/**"
  - "Packages/AppKit/Sources/Features/**"
  - "App/**/*View*.swift"
---
# Native UI

Read DESIGN.md for style and accessibility, EDITING.md for drafts; read DELIGHT.md when adding motion.
Use system controls, semantic colors, text styles and SF Symbols. Custom branding follows the recorded ADR.
Reuse the existing controls before adding a variant. NumericFieldRow and .withKeyboardToolbar() own number entry.
Attach the keyboard toolbar once inside the screen's NavigationStack and supply ordered FieldNavigation.
Use one sheet(item:) enum per presenter; stack-free content supports pushed and presented wrappers.
Composite rows own their single swipe/context action surface. Icon-only controls have labels and 44-point targets.
Apply the editing contract to every exit and advanced editor. Preserve drafts on errors and late completions.
Inspect empty/populated/editing/failure at normal/AX3, light/dark; interaction and VoiceOver need separate evidence.
