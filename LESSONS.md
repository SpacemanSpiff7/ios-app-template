# Lessons behind the template

Updated 2026-11-13. Sources: Airlock, CurlBro, CalorieTracker and owner feedback from After Six.
This file explains choices; executable configuration and linked contracts own the current rules.

| Lesson and observed evidence | Prevention |
|---|---|
| Large files became lint exclusions and stayed large. | Size budgets from the first commit; split rather than grandfather source. |
| Flat targets hid UI/domain leakage. | Layered SPM targets, import lint and a written dependency graph. |
| Regeneration lost plist keys; an iPhone-only archive inherited iPad from XcodeGen's target preset. | project.yml owns generated files; inspect target settings and the final bundle's UIDeviceFamily. |
| CalorieTracker's bootstrap had to remove mandatory custom buttons, palettes and animation wrappers. | Native controls and semantic styles by default; branding is a product decision with narrow policy changes. |
| Repeated number-entry fixes added select-all, row focus, 44-point targets, keyboard navigation and AX reflow. | Shared NumericFieldRow/keyboard toolbar; locale, zero, invalid text and precision checks; actual interaction remains a gate. |
| Add disappeared or became less useful after the first record; review flows accumulated duplicate acceptance screens. | Walk the primary task early in both empty/populated states, with one review and explicit Save. |
| Cancel, nested edits and late results risked changing accepted data. | EDITING.md, independent drafts, stable IDs, explicit commit and stale-original guards. |
| Provider cascades and equal attempt/overall timers obscured errors and left no recovery time. | ASYNC_WORK.md: one operation owner, monotonic deadline, bounded eligible recovery and cancellation. |
| An expired stored key returned 401; a saved credential and a fake transport had implied live readiness. | Stored/verified status is explicit; typed failures retain causes; live compatibility is separate from fixtures. |
| One bad optional recipe discarded useful parent results; generated URLs appeared to verify facts. | Tolerant optional mapping; provenance, estimates and measured truth remain distinct. |
| TEST SUCCEEDED and checkmark counts hid missing/crashed execution. | Match source declarations and structured xcresult identities; reject skips/failures; count parameter executions separately. |
| A signed installation could predate the last patch. | Source and app-tree fingerprints bind build/install/launch manifests; changed source or artifacts block reuse. |
| Successful renders were mistaken for keyboard, VoiceOver, camera or accuracy checks. | Separate static, render, interaction, live-service, signed-device and measured-accuracy evidence. |
| Hardcoded toolchain versions, simulator names and sed replacement of symlinks required bootstrap repairs. | Detect and validate the toolchain, select an available compatible UDID, preserve AGENTS.md and smoke-test a fresh app. |
| Root instructions and old plans grew stale; automatic task stops interrupted authorized work. | Short contract, scoped references, one current STATUS, explicit supersession and the user's requested cadence. |
| Owner feedback from After Six (2026-11-13): remove unrequested home copy and preview; add YAGNI for speculative infrastructure and assumed compliance work. | Requested/approved scope, optional ideas proposed separately, a concrete current need for new systems, and verified applicability before compliance-specific work. This is an owner preference. |
| Local lessons stayed in an app after the starter had already diverged. | /docs-debrief classifies corrections, compares the source template and proposes a verified reusable change. |

CalorieTracker evidence: docs/progress.md (2026-09-23 execution checks; 2026-09-24 device-family fix;
2026-10-01 shared editing; 2026-11-09 expired key; 2026-11-11 unified lookup; 2026-11-12 native polish;
2026-11-13 exact-source deployment). Its food/provider schemas and model policy are intentionally app-specific.

The source template update is checked by scripts/validate-template.sh, including the copied app's full gate.
Tooling regressions exercise missing/skipped identities, forged success summaries, stale artifacts, bootstrap
validation and shared locks. Native screens still require observed interaction evidence for focus and VoiceOver.
