# Earlier-device re-probe after campaign closure

Use when a user returns to a previously tested device after an initial campaign has closed, especially when the prior record contains a verified prefix plus unresolved dispatched operations.

## Preserve two cycle axes

Maintain both:

- **physical operation slot** — monotonically advances across every dispatched batch, including UNKNOWN exposure;
- **verified cycle ordinal** — advances only after a full SET+RESET cycle has native evidence and verified cleanup.

If verified cycles 1–30 exist and dispatched physical slots 31–40 are UNKNOWN, a new retest must not reuse 31–40. Start at physical slot 41 while the verified ordinal resumes at 31. If a later batch 51–60 becomes UNKNOWN, quarantine it and continue no earlier than physical 61 while keeping the verified ordinal unchanged.

## Separate retest namespace

- Create a dedicated retest directory and ledger; do not rewrite the initial-screening runner, BO package, or original permanent ledger.
- Bind the frozen recipe hash, original verified prefix, original energy, UNKNOWN ranges, alignment evidence, and independent cleanup records.
- Re-probing authorizes fresh alignment/approach but does not imply forming or conditioning should be repeated. Reuse prior preparation only when the user explicitly requests it and the prior prepared/contact Z is established.
- Use fresh operation IDs. Never relabel, delete, or replay UNKNOWN branch intents.

## Pre-dispatch versus post-dispatch faults

- Parse matrix routes with the canonical token parser; valid routes may be delimited by commas or semicolons.
- A controller-side route/parser rejection can be reconciled as zero exposure only when the wire journal proves the acquisition command was never sent and independent OFF/open/error cleanup succeeds. Retain the failed attempt as non-counted history.
- Once the acquisition command is sent, missing replies, transport EOF, timeout, or edge loss leave the whole dispatched batch UNKNOWN unless complete native rows are recovered. Independent cleanup establishes present safety, not past exposure.
- Continue only in a new non-overlapping physical-slot range after preserving an UNKNOWN-history record and fresh output-OFF, matrix-open, empty-error, driver-fingerprint, and pose proofs.

## Long-running retest operation

- Keep full batches atomic: durable INTENT before dispatch, exact native point/order validation, metrics, health operation, then verified cleanup.
- Failure uses verified full cycles only. UNKNOWN slots do not count toward the consecutive-failure window.
- Do not mutate optimizer state or start another device during a targeted retest.

## Storage-closure pitfall

Before deleting `/tmp` campaign coordination state, persist all source needed to reproduce or extend the campaign—not only runner/ledger/audit JSON. Archive controller scripts and imported helper modules, or install them under a durable campaign/workspace path. A later targeted retest should not depend on reconstructing deleted temporary orchestration code.