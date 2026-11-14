---
name: iap-tips
description: PLACEHOLDER — iap-tips workflow. Fill in once the product decision is made (see docs/PRODUCT.md § Open decisions).
disable-model-invocation: true
---
Not yet defined. When this area is decided:
1. Write the decision as an ADR (`/adr`).
2. Replace this file with concrete steps, commands, and the gates that must pass.
3. Remove `disable-model-invocation` so the skill can auto-trigger.

Seed notes from previous apps:
- StoreKit 2 consumables with Apple's `ProductView`; local `.storekit` config + separate test scheme (`storeKitConfiguration`).
- App Review rejected twice under 2.1(b) for a checkout error on the reviewer's device; add a Release-safe diagnostic logger and a TestFlight sandbox walkthrough as a human gate before submitting IAP.
- Cosmetic unlocks from tips: persisted locally, never a restorable entitlement; refunds don't revoke.
