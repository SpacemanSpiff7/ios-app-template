---
name: localization
description: PLACEHOLDER — localization workflow. Fill in once the product decision is made (see docs/PRODUCT.md § Open decisions).
disable-model-invocation: true
---
Not yet defined. When this area is decided:
1. Write the decision as an ADR (`/adr`).
2. Replace this file with concrete steps, commands, and the gates that must pass.
3. Remove `disable-model-invocation` so the skill can auto-trigger.

Seed notes from previous apps:
- `SWIFT_EMIT_LOC_STRINGS=YES` + String Catalogs from day one; every string localized once at its source (`String(localized:)`); real plurals; no `replacingOccurrences` on user text.
