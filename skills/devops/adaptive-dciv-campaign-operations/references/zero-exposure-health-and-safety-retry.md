# Zero-exposure health and safety retry

Use when a DC-IV batch or mandatory post-batch health operation fails before native acquisition dispatch, especially during NATS lifecycle or cleanup transport faults.

## Separate the three decisions

Do not collapse these into one status:

1. **Exposure classification:** inspect the durable wire journal. Zero exposure requires no native acquisition request after the operation intent/preflight/route commands.
2. **Scientific progress:** only a complete candidate response advances physical and verified cycle counters. A zero-exposure attempt advances neither.
3. **Current hardware safety:** even wire-proven zero exposure cannot authorize continuation when final cleanup is unverified. Obtain fresh OFF/open/error/pose/no-motion proof first.

## Health retries

A failed zero-exposure health intent must not satisfy a generic “health already exists” condition. Reject only an already completed health record:

```python
any(h.get("after_cycle") == cycle and h.get("state") == "COMPLETE"
    for h in health_operations.values())
```

Preserve the failed health attempt and retry the same due boundary with a fresh operation ID. Do not dispatch the next candidate batch until health is `COMPLETE` and cleanup verifies.

## Ledger compatibility

If a shared ledger blocks any operation whose state is not `COMPLETE`, encode proven zero exposure as:

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

Do not change device energy. Clear the device UNKNOWN flag only after scanning all device operations.

## Fresh safety when cleanup transport fails

If the normal command path is unhealthy, split the proof across independent paths:

- stop only the idle instrument edge by verified PID and CWD; do not USB-reset;
- over direct VISA issue `:ABOR` and `:OUTP OFF`, then require output OFF, correct terminals, and an empty error queue;
- prove the matrix open through a bounded direct command probe, using another known NATS peer when necessary;
- verify authoritative stage state, absolute XY, and no pending motion;
- restart only the affected edge and require idle state with no active run ID.

Preserve the failed cleanup record and store the fresh safety proof separately.

## Retrying a logical batch

Preserve every abandoned operation ID. Append a fresh attempt under the same logical batch number with new operation IDs. Zero-exposure attempts do not advance physical or verified counters. Emit a dispatch marker immediately before the native acquisition command; its absence plus no acquisition request in the wire journal is valuable evidence.
