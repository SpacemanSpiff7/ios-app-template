---
name: setup
description: Configure a fresh app from this template: identity, product task, native or custom style, review cadence and verification. Use for setup, init or a new app.
argument-hint: [app name]
---
Read README.md. Reuse decisions already provided in the request or spec. Ask one concise batch only for missing
choices that affect the product; continue independent setup work while waiting. Use the available input tool.

1. Identity: resolve app name, bundle id, signing team (or "-" for simulator only), and minimum iOS.
   Run scripts/bootstrap.sh with these values; it detects the toolchain and verifies generated settings.
2. Product: fill PRODUCT.md's one sentence, non-goals, vocabulary, information architecture and primary-task table.
   Record monetisation, persistence, onboarding and localisation only when the app needs the decision.
3. Style: keep native system controls by default. If custom branding was requested, record its reference, scope,
   accessibility and narrow lint changes in DESIGN.md plus an ADR. Palette and signature motion are optional.
4. Workflow: honor the user's authorized scope. Record a requested review cadence in PRODUCT.md; otherwise complete
   the task without approval after each step. Keep external distribution and human-only gates explicit.
5. Replace the Items example with the smallest complete primary task, or leave its replacement in BACKLOG if this
   request only covers setup. Cover empty/populated entry, input, review, Save, edit and recovery.
6. Run scripts/test-gate.sh, scripts/sim.sh build and scripts/sim.sh launch. Inspect the screenshots.
   Update STATUS with the exact evidence and remaining interaction/device gates. Commit only when authorized.
Report configured choices, verification, open work and the next concrete action.
