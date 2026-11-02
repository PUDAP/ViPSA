# Retained-prefix recovery after interrupted instrument operations

Use this when a campaign transport fault occurs after some electrical operations or guarded motion may have completed.

## Core rule

Electrical operations, health checks, and motion have separate evidence. A missing electrical receipt does not prove that the preceding motion did not occur.

## Recovery sequence

1. Pause autonomous scheduling to prevent concurrent ownership.
2. Preserve every ledger operation that is `COMPLETE` with complete native evidence; never replay retained stress.
3. For a PUDA `RUN_ID_MISMATCH`, reset only the affected machine state with `puda machine reset <machine_id>` after it is visible. Do not restart NATS.
4. Obtain fresh safety proof: SMU output OFF, matrix open/`nil`, error queue empty.
5. Query live XY/Z directly. Do not infer Z from completed-sweep counts: a guarded move may have completed before the following electrical operation failed.
6. If motion completed but the next electrical operation had no exposure, resume that same operation at the live pose without another move. If the operation is COMPLETE, resume at the following operation.
7. Seed stress and health counters from retained COMPLETE operations so health checks remain on absolute sweep/cycle boundaries.
8. Aggregate retained and new operation IDs/receipts in the recovery terminal record. Verify final counts, cleanup, and `UNKNOWN == false` before candidate publication or optimizer advancement.
9. Resume scheduling only after reconciliation and safety verification, and never overlap it with an active manual controller.

## Candidate/health distinction

If candidate acquisition completed natively but a following health operation failed with zero exposure, retain the candidate cycles and replace only the missing health operation. Do not replay retained candidate stress.
