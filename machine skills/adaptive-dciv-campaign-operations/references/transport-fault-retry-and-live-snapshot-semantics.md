# Transport-fault retries and race-safe live snapshots

Use this reference when a batched DC-IV campaign encounters NATS EOF/flush failures around candidate or health operations, or when plots are requested while the campaign continues.

## Classify by dispatch boundary, not by the final exception

A `FlushTimeoutError`, EOF, or failed lifecycle `COMPLETE` can occur at several different boundaries. Inspect the batch ledger, operation receipts, wire journal, edge log, and dispatch marker before deciding what to retry.

- **Candidate already committed:** if the batch ledger is `COMPLETE` with exact native rows/counts, do not recover or replay it merely because the supervisor later crashed.
- **Post-dispatch response fault:** if the acquisition command was dispatched and the caller lacks a receipt, keep UNKNOWN until an exact published response or retained native buffer is reconciled.
- **Pre-dispatch fault:** if route/preflight ran but no acquisition command appears in the wire journal, classify the attempt as zero exposure, preserve it, and retry with fresh operation IDs.
- **Health-only fault:** completed candidate batches remain valid. Reconcile or rerun only the missing health operation.

A supervisor traceback alone is not the scientific state.

## Exact response before retained-buffer recovery

After a client EOF, the edge may later publish the complete response to JetStream even though the caller has already timed out. Check for a matching durable response envelope keyed by run ID and command before opening the SMU directly. If no usable envelope is available, follow the retained-`defbuffer1` workflow from `native-instrument-acquisition-recovery`.

Do not dump multi-megabyte response lines into the conversation. Parse logs programmatically and emit only run ID, timestamps, command, count, completion/publication state, and hashes.

## Zero-exposure retry semantics

A zero-exposure attempt must remain in history but must not advance physical or verified counters. A fresh attempt at the same logical batch uses new operation IDs and the same physical/verified cycle range.

If a ledger guard rejects any operation whose `state != COMPLETE`, represent proven zero exposure as:

```json
{
  "state": "COMPLETE",
  "complete": false,
  "trace_energy_J": 0.0,
  "unknown_exposure": false,
  "reconciliation": {"zero_exposure": true, "no_replay": true},
  "original_fault_history": {"state": "UNKNOWN"}
}
```

Do not add energy. Clear the device UNKNOWN flag only after scanning all operations for another unresolved state.

## Health retry guard

A zero-exposure health intent is not a completed health measurement. A retry guard should block only when a health record at that cycle boundary has `state == COMPLETE`.

Preserve the zero-exposure health record and use a fresh operation ID for the replacement. Never rerun the candidate batch merely because its post-batch health command failed before dispatch.

## Preparation continuation

When forming has completed and passed but conditioning fails before dispatch:

1. preserve the forming receipt and criterion;
2. prove the conditioning intent had no acquisition dispatch;
3. preserve the current verified pose;
4. resume the missing conditioning sweep with a fresh ID;
5. carry total stress and health counters forward;
6. do not repeat pre-approach or forming.

## Race-safe live plotting

A live campaign may finish another batch while the plotting script reads the ledger. Snapshot by explicit verified-cycle boundary, not by asserting the ledger has exactly the requested total.

For a request such as cycles 1–20:

- include only COMPLETE operations/metrics whose verified cycle is in `[1, 20]`;
- require the filtered set to contain exactly that full contiguous range;
- exclude preparation, superseded attempts, zero-exposure records, and later cycles;
- annotate the figure as a frozen snapshot through cycle 20;
- leave acquisition running.

This prevents a newly completed Batch 3 from invalidating or contaminating a requested cycles 1–20 plot.
