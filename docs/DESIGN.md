# Design contract

## North star

A small native utility: clear task, readable information and predictable controls.
Replace this paragraph with the product's agreed direction; preserve the interaction and accessibility requirements.

## Style choice

Default: native. Use List, Form, NavigationStack, TabView, ContentUnavailableView, Menu and standard sheets.
Use semantic system colors, system text styles with Dynamic Type and SF Symbols.
Custom branding is opt-in: record the purpose, reference, affected surfaces and dark/AX3 behavior in an ADR.
Add only the required assets/components and narrowly update style checks; keep the architecture and size budgets.

## Controls and hierarchy

- One prominent primary action per screen; standard Button styles. PrimaryActionBar owns bottom actions.
- The primary task remains reachable in both empty and populated states.
- NumericFieldRow provides a visible number field, row-tap focus, a unit label and AX reflow.
- .withKeyboardToolbar() attaches once inside the screen's NavigationStack; focused editors supply FieldNavigation.
- Menus and icon-only buttons have labels and 44-point targets. Use one row action surface per composite row.
- One sheet(item:) destination enum per presenter. Pushed content does not create a second NavigationStack.
- Present the useful result before optional sources and technical detail. Collapse secondary explanations.
- System chrome handles navigation; content uses native rows/sections rather than decorative cards or glass.
- See EDITING.md for draft ownership, explicit Save, failure preservation and discard confirmation.

## Copy and truth

Labels name the action and consequence. Use one noun per concept, sentence case and localized source strings.
Keep implementation detail in controlled Technical Details, rather than making it part of the primary task.
A stored credential is Saved; only an actual service check can say Verified, with its time and result.
A successful request does not prove output accuracy. Keep estimates, unknown values and source provenance distinct.
Failure copy gives the known cause and a recovery action; it retains input and never disguises an error as no results.

## Verification

Inspect normal and Accessibility 3 text in light and dark, with empty, populated, editing and failure states.
Confirm a reachable primary action, readable hierarchy, scrollability, visible field affordances and unclipped exits.
Exercise keyboard focus/select-all/previous-next, Save/Cancel/reopen and failure recovery in an actual interaction run.
Check VoiceOver separately: labels, order, values and each action exposed once. Screenshots do not establish it.
Use Reduce Motion for animated screens. Record observed checks and their limits in STATUS/RELEASE evidence.
