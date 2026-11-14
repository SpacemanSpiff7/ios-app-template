---
name: plan-feature
description: Turn an idea into a feature spec and backlog acceptance criteria. Use when planning or specifying a feature.
argument-hint: <feature>
---
1. Read PRODUCT, DESIGN, ARCHITECTURE and BACKLOG. Extend the existing product boundaries.
2. Write docs/specs/<date>-<feature>.md with: Job; primary-task walkthrough; screens and empty/populated/editing/
   error states; data and migration; operation/store owner; native controls; out of scope; observable acceptance
   criteria; verification; and any unresolved product decision.
3. Include entry → input → review → Save → edit → recovery. Identify keyboard/dismissal requirements,
   stale-result risks, and the distinction between repository, rendered, live and physical-device evidence.
4. Add coherent BACKLOG entries linked to the spec. If implementation was requested, continue within that scope;
   if the request was planning only, present the concrete spec and stop without implementing.
