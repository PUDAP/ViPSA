---
name: native-instrument-acquisition-recovery
description: Use when native instrument acquisition fails mid-run.
version: 1.0.0
metadata:
  hermes:
    tags: [lab-automation, instrumentation, recovery, native-list, ledger]
    related_skills: [lab-instrument-run-recovery, vipsa-electrical-measurements, puda-operations]
---

# Native Instrument Acquisition Recovery

## Scope

Use for native buffered/list acquisitions that fail during preflight, verification, execution, cleanup, or orchestration. The objective is to distinguish **zero exposure**, **completed acquisition**, and **unknown/partial exposure**, preserve scientific accounting, repair the narrow defect, and resume only at the first missing operation.

This skill complements the broader `lab-instrument-run-recovery` skill. It specializes in source-list/buffer behavior, durable wire journals, energy ledgers, and exact branch-level continuation.

## Invariants

- Never infer non-execution from a missing CSV or controller exception.
- Never replay completed stress.
- Never clear UNKNOWN from cleanup alone; establish what happened during acquisition.
- Preserve exact requested arrays, native replies, command/run IDs, returned rows, energy, and cleanup evidence.
- Keep buffer capacity, waveform length, and returned measurement count as separate concepts.
- A recipe-specific failure is not proof of irreversible physical failure.

## Classification workflow

Classify the operation from durable evidence:

1. **Completed:** native command returned success, expected ordered rows are present, energy is finite/accounted, and cleanup is verified.
2. **Zero exposure:** rejection is proven before output enable, output was already OFF, no rows exist, and later cleanup independently confirms OFF/open.
3. **Unknown or partial exposure:** output may have enabled, rows are incomplete/ambiguous, or the journal lacks enough evidence.
4. **Completed but cleanup acknowledgement uncertain:** rows and energy are complete, hardware readback proves OFF/open, but a redundant cleanup command acknowledgement timed out. Reconcile cleanup without replay only when independent readbacks support it.

## Durable-evidence order

Inspect evidence in this order:

1. Permanent operation ledger.
2. Raw wire journal, keyed by exact instrument run ID and command name.
3. Per-operation receipt/intent files.
4. Controller terminal/progress summary.
5. Fresh harmless readbacks: output state, matrix channels, error queue, mechanical position.

A later lifecycle `complete` error can overwrite the ledger's more informative native-command error envelope. Recover the original failure from the wire journal rather than trusting only the final stored exception.

## Short native source lists

Some instruments enforce a minimum trace-buffer capacity even for shorter valid source lists. Treat these independently:

```text
buffer_capacity = max(instrument_minimum, len(commanded_values))
commanded waveform = original values, unchanged
required returned rows = len(commanded_values)
```

For Keithley 2450, the observed minimum capacity is 10. A five-point RESET list must remain five points; configure `:TRAC:POIN 10`, then require exactly five measurements. Do not pad the voltage waveform with repeated endpoints merely to satisfy buffer capacity.

Regression-test both sides:

- short list: 5 commands → buffer capacity 10;
- normal list: 89 commands → buffer capacity 89;
- returned-row validation remains 5 and 89 respectively.

## Zero-exposure reconciliation

Only use this path when all conditions hold:

- exact failing native reply is preserved;
- verifier states output was OFF before failure;
- failure occurred before `OUTP ON`/trigger execution;
- no rows were returned;
- operation cleanup proves output OFF and matrix open;
- final controller cleanup independently proves the same state;
- no other unresolved operation exists.

Then retain the failed operation and original error, annotate `zero_exposure=true` and `no_replay=true`, charge `0 J`, clear device UNKNOWN only after rechecking the whole ledger, repair/test/deploy the narrow defect, run a fresh output-OFF proof, and resume at the missing branch only. If any condition is missing, keep UNKNOWN.

## Completed acquisition with cleanup timeout

If native rows and finite energy are already committed but a redundant OFF acknowledgement times out:

1. Verify the operation's subsequent output readback is explicitly OFF.
2. Verify matrix readback is explicitly open/`nil`.
3. Require an independent final cleanup with the same readbacks.
4. Preserve the timeout in history.
5. Reconcile only cleanup state; do not re-charge energy or replay acquisition.

## Continuation construction

A continuation controller must explicitly bind prior completed operation IDs, reconciliation artifacts, starting stress counter, next health boundary, frozen recipe hash/arrays, first missing branch, and fresh OFF/open/error/position gates.

When SET and a due health read completed but RESET was zero exposure, resume cycle 1 at RESET only. Compute cycle-1 metrics from the preserved SET receipt plus the new RESET receipt, then begin cycle 2. Never reset energy accounting or health counters.

## Edge disconnect and stale USB ownership

After a NATS EOF/timeout, the edge process may remain alive while holding the VISA/USB interface even though the machine appears offline. Before restarting, identify the exact old process by PID and CWD; terminate only that stale edge. Launch the replacement with the known working instrument interpreter/environment (not an isolated environment that lacks `pyvisa-py`), then require a fresh idle/null state, loaded-driver fingerprint, output OFF, matrix open, and empty error queue. Do not restart NATS or unrelated edges.

## Verification before reporting success

- Correct expected row count and order.
- Finite energy charged exactly once.
- All device operations resolved; device UNKNOWN false.
- Fresh output OFF, matrix open, and acceptable error queue.
- No duplicate completed branch or motion.
- Cycle/sweep counters include preserved history correctly.
- A fresh run directory links every reused/reconciled artifact.

## Reporting

State what completed, exposure classification, what was not replayed, the tested fix, cleanup evidence, and exact continuation boundary.

## Reference

- `references/keithley-short-list-and-contact-correction-session.md` — tested five-point buffer fix, wire-journal reconciliation, cleanup-timeout reconciliation, and branch-level continuation details.
