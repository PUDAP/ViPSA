# Atomic device-completion verification

Use this checklist after a multi-batch device reaches a terminal result and before any motion to the next device.

## Aggregate evidence

- Sort batch records by explicit batch number, never lexicographically (`batch10` otherwise sorts beside `batch1`).
- Verify every expected cycle and SET/RESET branch once, native point totals, health checkpoints, cleanup, output OFF, matrix open, instrument errors, UNKNOWN state, and zero-exposure reconciliations.
- Classify the hard-cap survivor as right-censored; do not infer recipe failure without the configured consecutive-failure evidence.

## Atomic bookkeeping closure

Treat these as one logical transition:

1. completion aggregate and hashes;
2. permanent-ledger state;
3. runner completion record and consumed-device entry;
4. pending-candidate clearance;
5. optimizer handshake acknowledgement and active-request clearance;
6. cursor increment exactly once.

After writing, read all stores back together. A successful script exit or advanced cursor alone is insufficient. If the cursor advanced while the handshake still awaits a matched result, block motion and reconcile bookkeeping from the verified artifacts without replaying electrical work.

## Delivery ordering

When optimizer ingestion requires plot-delivery evidence, generate and verify the plot first, deliver it, verify the real delivery handle, and only then set `delivered: true` and ingest the acknowledgement. Intending to attach a plot to a future response is not delivery evidence.
