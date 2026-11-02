# Retained-buffer recovery and zero-exposure ledger schemas

Use this note for multi-device DC-IV campaigns that combine continuous native batches, mandatory post-batch health reads, append-only candidate ledgers, and a stricter shared hardware ledger.

## Post-dispatch response loss

A client EOF or NATS publication timeout after dispatch is UNKNOWN, not a failed acquisition. Before any edge or USB reset:

1. Stop the supervisor/child so it cannot advance.
2. Match the exact run ID and commanded segment sequence in the wire and edge logs.
3. If acquisition finished but response publication failed, stop only the idle instrument edge; do **not** USB-reset or clear trace buffers.
4. Extract the retained native buffer and require the exact expected point count and voltage sequence, finite strictly increasing timestamps, source/output status on every point, trigger idle, output OFF, correct terminals, and an empty error queue.
5. Hash the retained payload, restart only the affected edge, obtain fresh OFF/open/error/pose proof, and atomically reconcile rows, metrics, and energy exactly once.
6. Preserve original UNKNOWN history and mark the recovery `no_replay=true`; run only the missing post-batch health operation.

## Pre-dispatch zero exposure

No dispatch marker plus no native acquisition request in the wire journal can prove zero exposure. Keep every abandoned operation ID and retry with fresh IDs. Zero-exposure attempts advance neither physical nor verified cycle counters.

Separate three decisions:

- exposure classification;
- scientific progress;
- current hardware safety.

A zero-exposure classification does not excuse unverified cleanup. If the normal transport path is unhealthy, prove 2450 safety directly (`:ABOR`, `:OUTP OFF`, output/terminal/error readbacks), prove the 707B matrix open through a bounded peer probe, verify absolute XY and authoritative stage/no-pending-motion state, restart only the stale edge, and require idle/no active run ID.

## Ledger-state compatibility

A candidate ledger may preserve abandoned attempts as append-only `ZERO_EXPOSURE`. If a shared hardware ledger blocks every state other than `COMPLETE`, represent the same proven non-exposure as:

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

Do not add energy. Clear the device UNKNOWN latch only after scanning all operations for that device.

## Health retry guard

A zero-exposure health intent does not satisfy the health requirement. Treat health as already present only when the same boundary has a `COMPLETE` health record. Preserve the failed intent and retry the missing health read with a fresh operation ID before advancing to the next candidate batch.
