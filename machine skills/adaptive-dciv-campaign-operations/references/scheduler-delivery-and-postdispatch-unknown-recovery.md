# Scheduler, delivery, and post-dispatch UNKNOWN recovery

## Scheduler status is not controller status

A cron in-flight timeout or stale scheduler claim does not prove that a detached device supervisor failed. Before restarting anything:

1. Inspect live controller/supervisor processes and owner locks.
2. Read the newest terminal/progress artifacts.
3. Compare optimizer pending/active state with permanent-ledger counts.
4. If a supervisor is still running, do not start a duplicate controller.

A safe pattern is to let a live supervisor reach a terminal boundary while later cron ticks report or reconcile it.

## Delivery-gated optimizer acknowledgement

When the optimizer handshake requires actual plot/status delivery, use this order:

1. Complete candidate, health, cleanup, plots, and permanent ledger reconciliation.
2. Deliver the verified result to the requested channel.
3. Read back runner/handshake state.
4. Record and ingest the matched delivery acknowledgement.
5. Only then request or dispatch the next device.

A generated plot file or successful cron return is not itself proof of delivery.

## Continuous-acquisition timeout after dispatch

If the wire journal shows a continuous command was dispatched and then timed out before a trace response:

- preserve every claimed branch ID as UNKNOWN;
- do not count the intended cycles;
- do not replay the batch merely because receipt files are absent;
- force output OFF, open the matrix, read the instrument error queue, and independently verify safety;
- inspect wire, driver state, trace/buffer recovery, ledger, and energy evidence;
- clear UNKNOWN only if evidence proves zero exposure or reconstructs the exact completed native trace;
- otherwise retain a fail-closed hold and require explicit user resolution before quarantine-and-advance.

This differs from a pre-dispatch failure, which may be reconciled as zero exposure when the absence of hardware dispatch is proven.

## Campaign-specific gates outrank newly invented generic gates

Do not introduce a new movement gate midway through a stable campaign merely because a generic skill contains a stricter fallback. For routine transitions, preserve the campaign’s established contract. If a controller adds an unjustified gate after a retract has already completed, preserve the retract/readback and remove only the new gate; never repeat the motion. Escalate to extra optical clearance only for concrete new collision/scratch evidence, stale or contradictory position state, ambiguous motion completion, changed geometry, or explicit user direction.
