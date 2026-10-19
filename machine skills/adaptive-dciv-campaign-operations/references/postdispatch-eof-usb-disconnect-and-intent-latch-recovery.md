# Post-dispatch EOF, USB disappearance, and stale INTENT recovery

Use when a continuous native batch was visibly dispatched, the client later reports `UnexpectedEOF`/`ConnectionClosedError`, cleanup hangs or fails, or the controller is terminated before its exception handler updates the ledger.

## Required classification

1. Stop the supervisor and all candidate-controller children. Do not replay.
2. Inspect the exact wire journal and execution claim.
3. If dispatch is proven but the ledger still says `INTENT`, atomically promote the matching batch and every claimed operation to `UNKNOWN`, set `unknown_exposure=true`, `zero_exposure=false`, and `no_replay=true`, and preserve the original INTENT record. A stale INTENT after dispatch is not a harmless unstarted operation.
4. Keep the device-level UNKNOWN latch set until exact retained evidence and fresh safety proof are both accepted.

## Retained-buffer workflow

1. Identify the exact protected edge by PID and CWD.
2. If it owns the USB interface, terminate only that edge **without USB reset** so the instrument buffer survives.
3. Open the instrument directly in its known working PyVISA environment and immediately issue `ABOR` and output OFF.
4. Require the exact expected point count and dispatched voltage sequence, finite rows, strictly increasing native timestamps, all source-status output-on bits during acquired points, idle trigger state afterward, REAR terminals, output OFF, and empty error queue.
5. Save the raw retained result and hash before restarting the edge.
6. Restart one protected edge instance without USB reset. Require fresh output OFF, matrix `nil`, empty errors, correct terminals and deployed-driver hash, and unchanged pose.
7. Atomically convert only the matching UNKNOWN operations/batch to COMPLETE, preserve their UNKNOWN histories, charge energy once, recompute metrics, clear the device UNKNOWN latch, and run the missing post-batch health check.

## USB reset policy

Do not perform a routine USB reset before every batch. A reset can make a Keithley 2450 disappear from USB enumeration even when the preceding batch and health cleanup were valid.

Preferred order:

1. process-only restart of the affected protected edge;
2. verify OS/VISA enumeration and edge idle;
3. use `usbreset` only for a demonstrated stale/busy USB condition;
4. after reset, require the expected VID:PID/serial to re-enumerate before launching the edge;
5. if absent, stop retry loops, keep the campaign at the last verified batch, and require physical reconnect or power-cycle.

A pre-batch edge-start failure before candidate dispatch is zero new exposure and must not create or replay a candidate batch.