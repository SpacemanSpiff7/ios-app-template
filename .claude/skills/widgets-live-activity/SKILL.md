---
name: widgets-live-activity
description: PLACEHOLDER — widgets-live-activity workflow. Fill in once the product decision is made (see docs/PRODUCT.md § Open decisions).
disable-model-invocation: true
---
Not yet defined. When this area is decided:
1. Write the decision as an ADR (`/adr`).
2. Replace this file with concrete steps, commands, and the gates that must pass.
3. Remove `disable-model-invocation` so the skill can auto-trigger.

Seed notes from previous apps:
- Widget extension `Info.plist` keys (`CFBundleDisplayName`) got stripped by regeneration → archive validation failed. Keep them in `project.yml` `info.properties`.
- Live Activity + expiry task race: a `startOrReplace` that cancels running tasks silently kills early-scheduled expiry work.
- Deep-link back into the app via a URL scheme with the entity id.
