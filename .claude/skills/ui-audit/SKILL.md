---
name: ui-audit
description: Inspect a screen or primary-task flow from actual screenshots and available interaction evidence. Use for UI audits and visual checks.
argument-hint: <screen or flow>
---
1. Read DESIGN, EDITING and the task's acceptance criteria. Select the simulator with scripts/sim.sh destination.
2. Serialize build/install/launch and captures. Use scripts/sim.sh; capture default and AX3, light and dark,
   plus Reduce Motion for changed animations. Save evidence under .scratch/ui-audit/<date>/.
3. Open each PNG. Check hierarchy, primary action in empty/populated states, editable affordances, exits,
   44-point targets, clipping and large-text scrolling. Report exact findings with severity and affected surface.
4. Use an available interaction driver for focus, keyboard navigation, discard, Save/reopen and recovery.
   A still image, accessibility tree or render test alone cannot establish those interactions or VoiceOver.
5. Fix findings within the authorized scope, recapture changed states, and report remaining gates.
   Restore the simulator's appearance and text size after inspection.
