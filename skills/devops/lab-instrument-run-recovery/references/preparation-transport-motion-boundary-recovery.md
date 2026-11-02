# Preparation recovery across transport and motion boundaries

Use when a forming/conditioning run loses NATS or cleanup verification after a retained prefix of native sweeps.

## Recovery sequence

1. Pause schedulers and competing owners.
2. Preserve every operation with exact native evidence and permanent `COMPLETE` state; never replay that prefix.
3. Fail closed until explicit SMU output `0`, matrix `nil`/open, and empty error-queue readbacks succeed.
4. If harmless Keithley commands reject with `RUN_ID_MISMATCH`, reset only that PUDA machine state and repeat the full safety proof. Do not restart NATS or unrelated edges merely because one command timed out.
5. Query live Stage-Z and Zaber X/Y before constructing continuation.

## Motion-before-sweep boundary

A controller may complete the guarded `Z+step` for forming attempt N and then fail before attempt N's electrical sweep. Therefore completed sweep count does not determine live Z.

- Compare live pose with saved motion intent/completion artifacts.
- If live Z already includes attempt N's move, execute attempt N at the current pose without another move.
- Restore normal move-then-sweep behavior only for later attempts.
- If an initial recovery assumption fails at the fresh pose gate, preserve that zero-measurement preflight stop and verified cleanup, then rebuild from direct readback in a fresh recovery directory.
- Stop if the pose remains ambiguous.

## Aggregate continuation

Seed the recovery terminal with retained operation IDs and receipts, initialize cumulative-energy and every-N-sweeps health counters from the retained prefix, and append only new operations. Before candidate dispatch, verify unique COMPLETE IDs, exact forming/conditioning/health totals, final live pose, UNKNOWN false, and cleanup. Recipe publication must reference the aggregate recovery terminal, not the interrupted terminal.
