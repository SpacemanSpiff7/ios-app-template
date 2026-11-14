---
name: docs-debrief
description: Capture durable lessons after a correction, bug fix or changed rule; propose reusable improvements to the source iOS template.
---
1. Inspect the actual correction, root cause, failing behavior and verification evidence. Read GOTCHAS, DESIGN,
   CLAUDE.md and scoped rules before adding a duplicate.
2. Classify each candidate: personal preference, app-specific behavior, or reusable engineering lesson.
   Record a source link/commit, date and confidence limit; separate observations from explanations.
3. Choose the smallest effective home: a default, existing shared component, executable check, scoped rule,
   GOTCHAS entry or ADR. Propose deletions for guidance the evidence invalidated.
4. For reusable lessons, find the source template recorded by bootstrap in .template-origin.json. Compare its
   current implementation. Propose a table: lesson | evidence | destination | exact change | verification.
   Keep product schemas, provider choices and app-specific policy in the app.
5. Apply local changes already covered by the user's request. Changes to the source template require that
   destination to be authorized; when it is, prepare the full diff and run its fresh-app validation.
   Otherwise present the concrete proposal without writing to another project.
6. Update the single relevant truth and link the evidence. Keep STATUS short and BACKLOG limited to open work.
   A template change is complete only after a fresh copy bootstraps and passes its gate.
