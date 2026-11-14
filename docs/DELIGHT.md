# Motion and feedback

Use native feedback where it explains a consequence. A signature animation is optional.

- Native buttons already respond to touches; preserve their standard behavior.
- .contentTransition(.numericText()) may connect a changing value to the action that changed it.
- .sensoryFeedback(.success/.selection/.error, trigger:) may acknowledge a matching user action.
- Keep destructive confirmation native. Running work uses ProgressView and a Cancel action.
- Respect accessibilityReduceMotion when adding motion; avoid recurring attention effects.
- Add an effect only after the task and controls work. Document its purpose and fallback in DESIGN.md.

Inspect the changed screen with Reduce Motion on. Describe interaction and haptic checks separately from still renders.
