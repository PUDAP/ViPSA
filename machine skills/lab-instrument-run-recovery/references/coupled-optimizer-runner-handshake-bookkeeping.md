# Coupled optimizer bookkeeping after nonstandard completion

Use when a device completes through a nonstandard stop boundary or custom reconciliation and the next recipe publisher requires both runner and handshake state to agree.

## Two state stores must advance together

A device completion is not fully acknowledged by changing only the runner cursor. Reconcile both:

1. **Runner state**
   - pending result cleared;
   - initial-design cursor advanced exactly once;
   - pause/safety flags preserved intentionally.
2. **Optimizer handshake state**
   - active recipe matches the completed physical device and candidate;
   - append one history record containing request ID, frozen recipe, result, deterministic result hash, acknowledgement, and the exact COMPLETE candidate/health operation IDs;
   - clear `active` only after the history record is durable.

The next publisher should require `runner.pending is None`, the expected cursor, `handshake.active is None`, and the last acknowledgement for the immediately previous physical device.

## Nonstandard cycle stop

When the fixed failure criterion is reached after more than one batch (for example, nonconsecutive signals at cycle 10 followed by three consecutive signals at cycle 20):

- retain every completed batch;
- count candidate branches and health operations from the permanent ledger;
- generate plots across the full completed cycle range, not just the first batch;
- acknowledgement must record the actual final completed cycle, native-point total, health count, and confirmed consecutive failure cycles;
- do not force a one-batch bookkeeping template onto a multi-batch stop.

## Safe repair of stale handshake state

If runner bookkeeping is already durable but handshake state is stale:

1. verify the stale active recipe is exactly the completed candidate;
2. verify completion aggregate, final safety proof, UNKNOWN false, and exact COMPLETE operation set;
3. acquire runner and handshake locks together;
4. append the missing history/acknowledgement once;
5. clear active and fsync/atomically replace the handshake file;
6. re-run the next publisher's preflight rather than bypassing it.

Never clear an active handshake merely because the runner cursor advanced; prove candidate identity and completed evidence first.