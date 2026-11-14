---
name: analytics-privacy
description: PLACEHOLDER — analytics-privacy workflow. Fill in once the product decision is made (see docs/PRODUCT.md § Open decisions).
disable-model-invocation: true
---
Not yet defined. When this area is decided:
1. Write the decision as an ADR (`/adr`).
2. Replace this file with concrete steps, commands, and the gates that must pass.
3. Remove `disable-model-invocation` so the skill can auto-trigger.

Seed notes from previous apps:
- Both previous apps shipped zero analytics, "Data Not Collected". If you add any SDK: privacy manifest, App Privacy labels, and a `check_no_sensing`-style CI script that fails on forbidden imports.
