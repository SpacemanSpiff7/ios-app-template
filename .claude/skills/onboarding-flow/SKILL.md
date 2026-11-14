---
name: onboarding-flow
description: PLACEHOLDER — onboarding-flow workflow. Fill in once the product decision is made (see docs/PRODUCT.md § Open decisions).
disable-model-invocation: true
---
Not yet defined. When this area is decided:
1. Write the decision as an ADR (`/adr`).
2. Replace this file with concrete steps, commands, and the gates that must pass.
3. Remove `disable-model-invocation` so the skill can auto-trigger.

Seed notes from previous apps:
- One continuous, skippable journey: intro → permission → selection → first real state. Returning from a task restores the task that started it.
- Permission prompts only at the moment of need, with the in-app explanation first.
