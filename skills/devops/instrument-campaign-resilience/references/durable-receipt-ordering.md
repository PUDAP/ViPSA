# Durable Receipt Ordering After Ledger Commit

Use this ordering for any ledger-backed instrument acquisition:

1. `adapter.acquire(...)` returns a COMPLETE ledger-backed receipt.
2. Atomically persist that raw receipt immediately, before host validation.
3. Validate the persisted receipt against the frozen operation and native proof.
4. Attach campaign metadata and atomically replace it with the validated form.
5. Generate metrics and reconcile health/failure counters.
6. Compact only when the exact operation has one unique durable receipt.

A host validator failure must leave a receipt plus a validation fault—not a missing receipt after real exposure. A compactor exception is a post-cycle archival/control fault; it must not overwrite an already-established electrical cycle status or trigger replay.

For Keithley modern native-list proofs, compare each list readback with the corresponding stored configuration's recalled level. Do not independently apply host `.6g` rounding to unrestricted requested values. Retain `.6g` only for legacy fixtures that lack per-index stored/recalled evidence.

If an older controller still fails after ledger commit but before receipt writing:

- freeze retries;
- verify output OFF, matrix open, and errors empty;
- locate the exact COMPLETE ledger operation;
- deep-copy its native rows and cleanup evidence without synthesizing data;
- run the corrected validator;
- write the missing receipt with `reconstructed_from_permanent_ledger=true` and `no_replay=true`;
- regenerate cycle metrics and counters;
- compact only afterward;
- resume at the first genuinely missing branch or cycle.
