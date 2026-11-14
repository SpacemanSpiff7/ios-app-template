# Network and asynchronous work

Read when adding remote services, search, imports, media processing or other cancellable operations.
These are contracts, not a requirement to add a network layer to an offline app.

## Ownership and time

One observable store owns the visible operation, its Task, input, progress, result and typed failure.
Use a revision/generation guard so cancellation, a new selection or an edit invalidates late completions.
One monotonic deadline covers attempts, waits, repair and post-processing. Reserve time for recovery.
State retry eligibility and maximum attempts explicitly. Invalid requests, credentials, billing and permissions
require a corrective action; transient rate/transport/service failures may retry within the same deadline.
Honor Retry-After only within that budget. Cancellation stops underlying work and preserves input.
Choose foreground/background behavior deliberately; persisted queues and provider cascades need a demonstrated job.

## Results and writes

Stage successful output as an editable draft; Save/Add remains the persistence boundary.
Preserve useful independent items when an optional field is invalid. Keep unknown values distinct from zero.
Validate transport shape and domain constraints at the boundary; optional enrichment cannot erase usable results.
Distinguish recorded facts, estimates, consulted links and measured truth. A URL is not verification.
Check the exact endpoint/options/schema combination in a live smoke check before claiming service readiness;
public capability flags and fake transports prove different things.

## Failure and diagnostics

Keep typed categories for local validation/storage, credentials, billing/permission, rate limit, network,
timeout, remote failure, cancellation and unusable output. No results is a completed lookup with no usable result.
Show the known cause plus one recovery action. Retain the original input and selected context.
Copy Diagnostics uses controlled category, status, attempt count, elapsed time, operation and correlation IDs.
Keep credentials, headers, user input/media and raw service prose out of copied logs.
Saved means stored locally; connection verification is explicit, timestamped and separate.

## Checks

Cover success, no results, partial output, permanent/transient failure, cancellation, backgrounding, stale results,
duplicate Save and failed local persistence. Run one successful live request with the exact shipping combination.
Report fixtures, live compatibility, latency samples and accuracy evaluation as separate evidence.
