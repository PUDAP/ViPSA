# Named-device absolute grid navigation correction (2026-07-23)

## Context

A request to “move to device 22” was initially treated as “move one pitch left from device 23.” That was wrong because the live Zaber position (`x=9469, y=459218`) was not at the nominal S1 device-23 coordinate.

The user clarified that named devices must use the substrate grid’s stored absolute coordinates.

## Correct workflow

1. Identify the requested substrate/grid explicitly from context (for example, substrate S1).
2. Read the authoritative `grid_positions.csv` for that substrate.
3. Look up the requested `device_number` and extract its nominal absolute `x,y`.
4. Read the live Zaber position through a PUDA protocol.
5. Ensure stage-Z clearance once; preserve that checkpoint and do not repeatedly retract on retries.
6. Compute exact deltas from live position to the target:
   - `dx = target_x - live_x`
   - `dy = target_y - live_y`
7. Move by those exact deltas using PUDA, then read Zaber position again.
8. Report success only if the readback equals the requested grid coordinate.
9. Run visual pad alignment afterward only when requested; alignment corrections will intentionally shift Zaber away from the nominal grid coordinate.

## Concrete S1 example

From the S1 7×7 `grid_positions.csv`:

- Device 22: row 3, column 0, `x=24383`, `y=509373`
- Device 23: row 3, column 1, `x=29383`, `y=509373`

Corrected device-22 move:

- Live start: `x=4469`, `y=459218`
- Commanded deltas: `dx=+19914`, `dy=+50155`
- Verified final readback: `x=24383`, `y=509373`

## Pitfall

Do not infer that the current device is the last named device in conversation. Alignment passes, manual moves, substrate changes, or interrupted workflows can make that assumption false. The ±5000 pitch mapping is only for an explicit adjacent-neighbor request from a verified current grid coordinate.
