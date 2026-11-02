# Keithley edge recovery after forced acquisition abort

Use only after a dispatched acquisition has been classified UNKNOWN and the user or safety policy requires an immediate stop.

1. Stop the campaign supervisor so no new batch can dispatch.
2. Preserve every dispatched branch as UNKNOWN; do not claim the requested stop boundary prevented exposure if the command was already sent.
3. Identify the exact old edge process by PID and CWD. A disconnected edge can remain alive and hold the VISA/USB interface.
4. Terminate only that stale edge and verify no campaign/batch process remains.
5. If a replacement process loops with `USBError: Resource busy`, identify the device and owner with `lsusb` plus `fuser -v /dev/bus/usb/<bus>/<device>`. Kill the retrying replacement and verify the USB node is unowned.
6. Reset only the affected instrument USB device by VID:PID (for the Keithley 2450, `usbreset 05e6:2450`). Do not restart NATS or unrelated edges.
7. Launch one clean protected edge instance using the known working instrument interpreter/environment.
8. Require fresh output OFF, matrix open, empty error queue, REAR terminals, expected driver hash, and unchanged stage/Zaber pose.
9. Preserve the interrupted batch as UNKNOWN/no-replay. For a user truncation, exclude post-boundary UNKNOWN slots explicitly rather than deleting them.

The validated recovery is the narrow stale-process/USB reset plus fresh readback sequence—not repeated blind edge launches while the node remains busy.
