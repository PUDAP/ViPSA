# Retained-prefix preparation recovery after transport faults

Use this pattern when a multi-sweep ViPSA preparation run faults after some forming/conditioning operations are permanently COMPLETE, especially after NATS timeout, `RUN_ID_MISMATCH`, or cleanup-readback loss.

## Recovery contract

1. Pause autonomous schedulers that could acquire the same hardware.
2. Inventory the interrupted terminal record and permanent electrical ledger.
3. Retain only operations with exact native evidence and permanent `COMPLETE` state. Never replay them.
4. Fail closed until fresh SMU output-OFF, matrix `nil`/open, and empty error-queue readbacks succeed.
5. If the affected edge rejects harmless commands with `RUN_ID_MISMATCH`, confirm the edge process/log and reset only that PUDA machine state. Do not restart NATS or unrelated edges.
6. Re-run the OFF/open proof after reset.
7. Query live Stage-Z and Zaber X/Y before constructing the continuation.

## Motion-before-sweep boundary

A forming controller may execute the next guarded `Z+step` motion and then fail before the corresponding electrical sweep is committed. Therefore:

- completed sweep count does **not** determine live Z;
- compare the live pose to every saved motion intent/completion artifact;
- if live Z already includes the move for missing sweep N, resume sweep N at that live Z **without another move**;
- subsequent attempts resume the normal move-then-sweep sequence;
- if the pose is ambiguous, do not move or stress.

## Continuation artifact

Write a fresh recovery directory. Seed its aggregate terminal record with the retained operation IDs/receipts, initialize the health counter to the retained stress-sweep count, and append only newly completed operations. The final preparation record should represent the full retained prefix plus continuation while preserving links to the interrupted run.

## Verification

Before candidate dispatch, verify:

- all aggregate preparation operation IDs are unique and `COMPLETE` in the permanent ledger;
- forming/conditioning/health counts match the aggregate terminal record;
- device UNKNOWN is false;
- final pose equals live readback;
- cleanup is verified with explicit output `0`, matrix `nil`, and no instrument errors;
- recipe publication points to the aggregate recovery terminal, not the interrupted terminal.
