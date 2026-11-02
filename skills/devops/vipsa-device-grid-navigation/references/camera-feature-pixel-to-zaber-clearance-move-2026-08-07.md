# Camera-feature center-to-center Zaber move with explicit Z clearance

## Trigger

Use when the user identifies a visible pad/device in a camera image, asks for its pixel offset from the currently probed feature, converts that offset to Zaber steps, and then authorizes the resulting move. This is an **image-derived feature move**, not automatically a named-grid or adjacent-grid-pitch move.

## Pixel measurement and conversion

1. Use the actual camera frame, not a replied-to electrical plot or screenshot that contains no physical device geometry.
2. State both centers and the reference explicitly. For the 2026-08-07 Camera-1 example:
   - current/probed large pad center: `(705, 565)` px;
   - large pad immediately right: `(1255, 580)` px;
   - `dx = +550 px`, `dy = +15 px`.
3. Use the active Camera-1 calibration from `vipsa-vision-alignment`, currently `21.5` native Zaber steps/pixel:
   - `X = round(+550 × 21.5) = +11825` native steps;
   - `Y = round(+15 × 21.5) = +323` native steps.
4. Propagate pixel uncertainty into steps. A `±10 px` center estimate corresponds to approximately `±215` native steps.
5. Report the estimate before motion and do not move until the user authorizes it.

## Sign convention for this camera geometry

To bring a feature seen to the **right/down** of the current target under the fixed probe:

- image target right (`dx > 0`) → Zaber `X` positive;
- image target down (`dy > 0`) → Zaber `Y` positive.

This is equivalent to the alignment formula in `vipsa-vision-alignment`, where the desired image shift is the negative of the target-center offset.

## Safe authorized sequence

When the user gives exact clearance and return moves, preserve them exactly and execute in order:

1. Force SMU outputs off, 707B `open_all`, verify closed channels `nil`, and turn lights off.
2. Query live Stage and Zaber positions.
3. `stage.move_z_by(height=-70, feedrate=450)` and verify readback.
4. `zaber.move_x_by(distance=+11825, units=None)` and verify readback.
5. `zaber.move_y_by(distance=+323, units=None)` and verify readback.
6. `stage.move_z_by(height=+65, feedrate=450)` and verify readback.
7. Reassert electrical cleanup and verify all relevant machines idle with null run IDs.

Observed readback pattern in the example:

- Stage: `390.5 → 320.5 → 385.5`;
- Zaber: `(374049, 839613) → (385874, 839936)`.

Treat Stage position as software/edge readback, not independent proof of physical Z.

## Critical distinction from grid pitch

Do **not** replace an image-derived calibrated displacement with the generic `±5000` adjacent-grid convention. The `±5000` rule is only for an explicitly requested known adjacent device in a grid whose pitch convention is established. A visible feature-to-feature camera offset uses the current steps/pixel calibration unless an authoritative absolute grid coordinate exists.

Do not automatically align, approach, or electrically measure after the move unless the user requests those phases.