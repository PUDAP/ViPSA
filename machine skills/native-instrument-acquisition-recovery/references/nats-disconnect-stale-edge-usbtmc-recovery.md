# NATS disconnect, stale edge ownership, and USBTMC recovery

Use after a native acquisition was dispatched, the response channel timed out or disconnected, and cleanup commands cannot start because the old edge run remains active.

## Classification
- Missing reply after dispatch is UNKNOWN exposure unless complete native rows can be recovered.
- Fresh cleanup after restart proves current safety only; it does not turn the interrupted batch into zero exposure.
- Never replay the unresolved physical slots.

## Recovery sequence
1. Preserve the operation IDs, exact wire journal, timeout/EOF, and any `RUN_ID_MISMATCH` replies.
2. Identify the old edge process by PID and CWD. An edge may be offline in PUDA while its process still holds VISA/USB.
3. Terminate only that stale edge; do not restart NATS or unrelated devices.
4. Launch the isolated driver with the known working instrument interpreter/environment. Avoid a different environment that omits the established VISA backend.
5. If the new process reports USB resource busy:
   - `lsusb` to rediscover the current bus/device;
   - `fuser -v /dev/bus/usb/<bus>/<device>` to identify the owner;
   - stop the retrying process and require the node to become unowned;
   - reset only the affected VID:PID, e.g. `usbreset 05e6:2450`;
   - start exactly one clean edge process.
6. Require a new independent transaction proving output OFF, matrix open, acceptable error queue, expected driver fingerprint, terminals, and mechanical pose.
7. Quarantine the interrupted physical slots as UNKNOWN/no-replay. Continue only at fresh physical slots if continuation is still authorized.

## User stop after dispatch
If the user requests a truncation boundary after a later batch was dispatched, mark that entire in-flight range UNKNOWN, perform the same recovery, and exclude post-boundary slots from the truncated analysis. Do not claim that those operations never happened.
