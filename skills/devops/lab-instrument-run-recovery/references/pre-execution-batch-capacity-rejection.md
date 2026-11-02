# Pre-execution batch-capacity rejection recovery

Use when a continuous electrical batch is rejected because the compiled native point count exceeds an instrument or driver configuration-list limit.

## Classification gate

Treat the intended operations as **zero exposure / failed before hardware action** only when all of the following are present:

- the native response explicitly rejects the request during validation or trigger-model construction;
- no result envelope, trace rows, receipt, or acquisition summary exists for any intended branch;
- completed-cycle count remains zero;
- cleanup reports output OFF and matrix open;
- a fresh independent readback again confirms output `0`/OFF, matrix `nil`/open, and no instrument errors.

A dispatched request plus a timeout, missing reply, partial trace, or unknown native status is **not** zero-exposure evidence.

## Ledger reconciliation

- Preserve every pre-registered operation ID.
- Mark each abandoned intent COMPLETE only as a reconciliation record with `complete=false`, `trace_energy_J=0`, `zero_exposure=true`, `candidate_cycle_counted=false`, and `replacement_batch_required=true`.
- Clear the device UNKNOWN flag only after confirming there are no remaining UNKNOWN operations and fresh safety readback passes.
- Generate new operation IDs for the replacement batch; never overwrite or reuse the abandoned IDs.
- Prefix validators must exclude reconciled zero-exposure intents from scientific operation counts while still requiring their state, zero-energy value, and provenance to remain valid.

## Capacity planning before replacement

Compute the exact native point total before dispatch. If one native list has a hard capacity but the experiment requires one continuous output-ON interval, do not silently reduce cycle count or insert an OFF boundary. A valid multi-list implementation must be tested to prove:

- every individual configuration list remains within its native capacity;
- all lists are constructed and size-read back while output is OFF;
- the trigger model contains exactly one output-ON block and one final output-OFF block;
- transitions between lists occur only at explicit zero-voltage segment boundaries;
- all returned trace rows contain native source-status evidence showing output ON;
- any compile, runtime, trace, or cleanup failure forces output OFF.

Do not record a multi-list driver change as operationally proven until both fake-driver regression tests and a real harmless/native preflight pass. Keep autonomous continuation paused for the first live batch using the new execution path.
