# Resume a grid from a named device after an explicit Z retract

Use this pattern when the user says, for example, “move Z down by 35 steps and continue the grid from device 4.” The key ambiguity is whether the stage is still on the last incomplete device or has already been manually moved/aligned to the named boundary device. Resolve that from live readback and the saved grid—not from the newest partial folder.

## Procedure

1. **Inspect, then act.**
   - Confirm no measurement runner is active.
   - Read the current stage Z, Zaber X/Y, electrical route/output state, the grid-position table, the named device summary, and the last partial device summary.
   - Compare live Zaber X/Y with the named device’s absolute grid target. Allow for a small alignment correction: a live position near the nominal target can be the aligned named device even when it is not exactly equal to the CSV coordinate.
   - Treat the user’s named restart device as authoritative. An earlier `status: started` folder is historical partial data, not evidence that the hardware is still there.

2. **Perform the requested Z motion as a standalone PUDA protocol.**
   - Include electrical cleanup first: Keithley and Keysight outputs off, then 707B `open_all`.
   - Include stage position readback before and after `move_z_by`.
   - Include final Zaber position and 707B route readback.
   - Let `puda protocol run` supply explicit lifecycle START/COMPLETE commands.
   - Verify the numerical Z delta (for “down 35,” `Z_after = Z_before - 35`) rather than reporting only command success.
   - Record protocol creation/run in `project.md` using real timestamps.

3. **Choose first-device continuation behavior from the live handoff.**
   - If live X/Y already matches the aligned named device, do **not** move Zaber back to the nominal CSV coordinate and do not realign blindly. Preserve live X/Y.
   - After the explicit retract, approach electrically from the verified retracted Z position. Do not add an unrequested pre-approach move that would partially undo the requested retract.
   - Record the verified `Z_before`, `Z_after`, live X/Y, requested boundary device, and “no initial X/Y move” in the first resumed device summary.
   - If live X/Y does not correspond to the named device, keep electrical cleanup active, use a safe travel Z, move to the device’s **absolute** grid coordinate, then align/pre-approach normally.

4. **Patch the continuation boundary correctly.**
   - Set `START_AT_DEVICE` to the named device and slice the actual serpentine traversal at that device.
   - Preserve valid summaries before the boundary. Also preserve an earlier standalone partial `device_N/summary.json` even if it was never appended to `summary.partial.json`; mark it as interrupted/partial instead of rerunning it unless requested.
   - Do not let “first missing `DONE.json`” override the named boundary.
   - Ensure stale first-device handoff text, substrate/device IDs, coordinates, Z values, and old contact-current claims are removed from cloned runners.
   - Compile the patched runner before launch.

5. **Launch and verify real progress.**
   - Run as a tracked background process with unbuffered output and completion notification.
   - Verify a fresh `device_<boundary>/summary.json`, a `device_start` event for the correct device, and live machine activity/readbacks.
   - For a long grid, install one stateful reporter for the entire run before launch. It should parse `summary.json` after each new terminal device event and report every device exactly once; a one-device watcher is only an initial verification aid, not a substitute.

## Pitfalls

- **Assuming the last partial device is the current physical device.** Manual motion/alignment may have happened after the runner stopped. Live X/Y plus the grid map decides.
- **Snapping an already aligned device back to nominal CSV coordinates.** Preserve the live aligned offset for the first resumed device.
- **Undoing the user’s retract.** Do not automatically apply the generic `+30` pre-approach when the instruction was explicitly “down 35” and live X/Y is already on the named device; let bounded electrical approach advance from the verified retracted position.
- **Dropping partial history.** A stopped runner may have written `device_03/summary.json` but not appended it to `summary.partial.json`; preserve it as partial when resuming from device 4.
- **Reporting movement from command success alone.** Require before/after position readbacks and the expected delta.
