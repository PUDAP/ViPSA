# Long native-batch EOF recovery and sidecar plotting

Use when a long continuous DC-IV batch loses its NATS response after dispatch, or when the operator requests plots while measurement continues.

## Post-dispatch EOF recovery

1. Treat `UnexpectedEOF`, `ConnectionClosedError`, or timeout after proven dispatch as UNKNOWN immediately. Do not replay.
2. A killed or hung controller may leave the batch and operations as `INTENT` because its exception/finally path never committed. Proven dispatch overrides that stale bookkeeping state: under the owner lock, atomically normalize the batch and every operation to `UNKNOWN`, set the device UNKNOWN latch, preserve the original INTENT record as fault history, and mark `no_replay=true`.
3. Stop the controller/supervisor before recovery. Identify and stop only the protected instrument edge if it owns VISA. Do not USB-reset while trying to preserve a retained native buffer.
4. Extract the retained buffer and require exact run ID/request identity, exact segment arrays, exact point count, finite rows, monotonic native timestamps, source-output-on status for acquired points, trigger idle, output OFF, REAR terminals, and an empty error queue.
5. Restart the protected edge without USB reset, then require fresh independent OFF/open/error/driver-hash/pose proof.
6. Atomically convert only the matched UNKNOWN operations and batch to COMPLETE, charge energy exactly once, retain the original UNKNOWN history, clear the UNKNOWN latch only when the full ledger is resolved, and run the missing post-batch health check.
7. Resume at the next batch only after health and cleanup verify.

## Edge restart policy

For normal between-batch hygiene, prefer a process-only protected-edge restart. Do not make `usbreset` routine: it can cause the instrument to disappear from USB enumeration. Use a targeted USB reset only for a demonstrated stale USB/VISA session and only after checking enumeration and ownership. If the device disappears, do not dispatch; wait for re-enumeration or physical reconnect/power cycle, then re-establish all safety gates.

## Sidecar plotting during a live run

1. Never pause or lock out the live supervisor merely to plot.
2. Read the ledger once and freeze a snapshot at the highest contiguous COMPLETE batch/cycle boundary. Exclude active INTENT/UNKNOWN batches.
3. Plot saved commanded voltage against `abs(saved measured current)` on a logarithmic current axis.
4. Preserve branch styles: PF solid, PB dashed, NF dotted, NB dash-dot; use a cycle color scale for dense overlays.
5. Export PNG plus CSV. The CSV must contain exactly one row per native measurement. A turning point may be shared visually by forward/backward traces, but must not be duplicated in the CSV.
6. Record the frozen boundary, ledger hash, cycle/operation/row counts, artifact hashes, and that the live campaign was not paused.
7. Verify the rendered plot and confirm the supervisor remains active afterward.
