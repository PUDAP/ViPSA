# Revisiting a previously aligned device: coordinate precedence

Use this pattern when a stopped/paused grid run must return to a device that was previously aligned or manually revisited.

## Coordinate source order

1. Confirm the substrate/run and requested device number.
2. Read `grid_positions.csv` to establish the nominal device identity and coordinates.
3. Inspect the device's completed/retry summary for an explicitly recorded **aligned absolute Zaber X/Y** and evidence that those coordinates were successfully commanded/read back.
4. For a direct revisit to the same tested pad, prefer the verified aligned absolute X/Y over the nominal CSV X/Y. The alignment offset is intentional and snapping to nominal can undo it.
5. If the aligned coordinates are missing, ambiguous, stale after a substrate remount, or not backed by readback, fall back to the CSV target and plan a fresh alignment.

## Safety and execution

- Verify no grid runner remains active.
- Force SMU outputs off and verify the 707B is open before travel.
- Query stage Z and Zaber X/Y live.
- If stage Z is already at a freshly verified safe retracted clearance, do not add another automatic retract. Otherwise retract Z once before X/Y motion.
- Use absolute native-unit `move_x_to` and `move_y_to` PUDA protocols.
- Read Zaber X/Y afterward and require exact agreement with the selected target.
- Report whether the destination was the nominal CSV coordinate or a prior verified aligned coordinate.

## Example class of evidence

A grid row may contain nominal coordinates while a later retry summary records a small alignment correction. A terse request to “move to device N” during the same mounted run should return to the prior verified aligned coordinate when the goal is the same tested pad, while still using the CSV to verify device identity.
