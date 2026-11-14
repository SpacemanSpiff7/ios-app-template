---
paths:
  - "Packages/AppKit/Sources/Persistence/**"
---
# Persistence rules
- Versioned schema: `AppSchemaV1`, `V2`… in `Persistence/Schema/`; `AppSchema.current` is the single list every container uses (app + tests).
- Migration plan required for any model change that ships. Add a test that opens a fixture store from the previous version.
- No `@Attribute(.unique)` (breaks CloudKit). No relationship assignment in `@Model` `init`. Insert first, then link.
- Repositories expose Sendable value DTOs to features; @Model classes stay in Persistence. The sample repository
  is MainActor-bound and synchronous. Add a background actor only for measured work that needs one.
- Persist crash-recovery drafts only when the product requires resume; use atomic Codable files for transient
  recovery state. A new draft does not write a placeholder record.
