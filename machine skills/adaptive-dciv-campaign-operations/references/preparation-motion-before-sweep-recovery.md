# Preparation recovery when motion completed before the sweep

Use this pattern when forming/conditioning preparation faults after a guarded contact move but before the next electrical operation is durably receipted.

## Why this boundary matters

A preparation terminal record may show `completed_sweeps = N` even though the controller already executed the motion that positioned attempt `N+1`. Reconstructing pose as `initial_z + (N-1)*step` can therefore be wrong and can cause a duplicate contact move.

## Verified recovery sequence

1. Pause the autonomous campaign scheduler so no second controller can race recovery.
2. Inventory the permanent ledger and interrupted terminal record:
   - retain every operation with complete native rows and `COMPLETE` state;
   - do not replay those sweeps;
   - confirm whether the next sweep has an intent, rows, or receipt.
3. Fail closed if cleanup lacks an explicit SMU output readback, even when matrix `open_all` and `nil` readback succeeded.
4. Recover only the affected PUDA edge state. For `RUN_ID_MISMATCH`, inspect the active edge log/machine visibility, reset the affected machine state, and do not restart NATS.
5. Reissue harmless safety commands and require fresh evidence: SMU output `0`, matrix `nil`, and empty instrument error queue.
6. Read the live stage and coarse-stage positions. Never infer pose only from `completed_sweeps`.
7. Compare motion artifacts and live pose:
   - if the authorized move for attempt `N+1` already landed but no sweep was recorded, resume that attempt at the live pose and **skip its move**;
   - apply the normal increment only from attempt `N+2` onward;
   - if the move did not land, execute it once after the machine is idle and safety is verified;
   - if pose is ambiguous, remain stopped.
8. Seed the continuation with the retained operation IDs, receipts, completed-sweep count, and health counter. Write new operations under a fresh execution ID while preserving the interrupted directory.
9. The final preparation terminal should aggregate retained and new receipts, report the true final pose, and state that the retained prefix was not replayed.
10. Before candidate publication, cross-check the aggregate terminal against the permanent ledger: exact operation count, every operation COMPLETE, device UNKNOWN false, and cleanup verified.

## Concrete boundary example

A run had two complete forming sweeps. The controller had already moved from `Z=58` to `Z=63` for forming attempt 3 when transport completion failed; attempt 3 had no electrical receipt. Recovery initially assuming `Z=58` stopped on a fresh pose mismatch without motion or stress. A live pose query showed `Z=63`. The correct continuation resumed attempt 3 at `Z=63` without another move, then used `+5` only for later attempts. The combined preparation completed with five forming sweeps, thirteen conditioning sweeps, one health read, verified cleanup, and no replay of forming sweeps 1–2.

## Pitfalls

- Do not classify missing attempt-`N+1` rows as proof that its preceding motion did not happen.
- Do not clear or replace the permanent ledger to simplify recovery.
- Do not include a no-measurement recovery attempt as a completed sweep.
- Do not resume candidate testing until the preparation aggregate and live safety state agree.
