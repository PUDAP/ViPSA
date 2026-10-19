---
name: vipsa-device-grid-navigation
description: Navigate ViPSA grids by absolute substrate/device coordinates or relative adjacent-device moves, with safe clearance, readback, alignment, and optional approach.
---

# ViPSA Device Grid Navigation

Use for named substrate/device destinations, relative grid-neighbor moves, and follow-on alignment or approach.

## Required companion skills

Load before executing:

1. `puda-operations`
2. `puda-env`
3. `vipsa-machine-operations`
4. `vipsa-image-capture`
5. `vipsa-vision-alignment`
6. `vipsa-electrical-measurements` when the request includes contact approach or any current/resistance check.

## Direction mapping

The user's current ViPSA grid pitch convention uses Zaber native units (`units: null`):

- Device on the **right**: `zaber.move_x_by(distance=+5000, units=None)`
- Device on the **left**: `zaber.move_x_by(distance=-5000, units=None)`
- Device **below** the current one: `zaber.move_y_by(distance=+5000, units=None)`
- Device **above** the current one: `zaber.move_y_by(distance=-5000, units=None)`

Before lateral grid travel, retract the microscope Z stage for clearance:

- `stage.move_z_by(height=-35, feedrate=450)`

In this setup, stage Z **down** is negative signed height; approach forward is +Z.

## Camera-feature moves are not grid-pitch moves

If the user identifies a visible pad/device by image geometry and asks to move to its center, use the actual center-to-center pixel displacement and the current Camera-1 calibration from `vipsa-vision-alignment` (currently `21.5` native Zaber steps/pixel). State the source image and reference centers, propagate pixel uncertainty, and preserve the calibrated X/Y signs. Do **not** substitute the generic `±5000` adjacent-grid pitch unless the user explicitly requested a known adjacent grid device or an authoritative grid coordinate applies.

For an authorized compound move, force electrical outputs off/open first, query live Stage/Zaber positions, preserve the user's exact Z-clearance → calibrated XY → Z-return sequence, and verify readbacks after every phase. Do not automatically align, approach, or measure afterward. Concrete calculation, sign mapping, and verified sequence: `references/camera-feature-pixel-to-zaber-clearance-move-2026-08-07.md`.

## Named-device navigation (for example, “move to device 22 from S1”)

A named substrate/device request is an **absolute grid-coordinate request**, not an adjacent-direction request.

**Scope rule for terse requests:** “move to device N” authorizes only safe clearance plus absolute Zaber X/Y travel. Do **not** automatically align, pre-approach, electrically approach, or measure. Those are separate follow-on phases unless the user explicitly includes them. This is especially important after a stopped/interrupted grid run, where the latest device folder may contain a completed alignment but no contact result.

1. Read the requested device row from the authoritative substrate/run `grid_positions.csv`. Prefer the active run's copied CSV when resuming or revisiting that run, because it preserves the exact coordinate frame used by the experiment.
2. Query live `stage` and `zaber` positions before motion; never infer the start from the last log message or device number.
3. Confirm prior electrical cleanup when coming from a stopped measurement: SMU outputs off, 707B open/nil, and no runner remains. Do not repeat the whole cleanup if it was just verified and no new electrical action occurred.
4. Retract stage Z for clearance exactly once, unless a verified clearance checkpoint is already current. If stage readback is software-tracked, report it as an edge/readback value rather than independent proof of physical motion.
5. Compute `dx = target_x - live_x` and `dy = target_y - live_y`.
6. Run one PUDA protocol using absolute native-unit `move_x_to(target_x, units=None)` and `move_y_to(target_y, units=None)` when available. Relative `move_x_by(dx)` / `move_y_by(dy)` is acceptable only when the signed deltas were computed from a fresh live readback.
7. Run a separate post-motion position read and require exact final Zaber readback equal to the CSV target; then verify `stage` and `zaber` are `idle`, `run_id: null`.
8. Report start position, signed deltas, CSV target, final readback, and whether alignment/approach were intentionally not performed.

**Pitfall:** Never infer a named device’s destination by assuming the current device number and applying a single `±5000` pitch. Alignment corrections, manual moves, substrate-origin changes, and stale context can invalidate that assumption. Use the `±5000` mapping only for explicit relative requests such as “one device left.”

- `references/return-from-substrate-edge-to-s9-device6-2026-07-26.md`.
- `references/manual-s9-device8-aligned-handoff-2026-07-27.md` for manual S9 device-8 handoffs: honor the user's explicit stage-Z clearance amount, force electrical outputs off/open before XY travel after pulse work, compute the archived aligned target as `zaber_readback_pre_align + alignment.move_native`, and verify post-move readbacks/states.

Detailed workflow and verified S1 example: `references/named-device-absolute-navigation.md`.

## Nearest-device identification from live Zaber position

Use this when the user asks “which device are we closest to?” or wants to assign current-position measurements to a grid device:

1. Query live Zaber X/Y with `zaber.get_current_position(units=None)` through PUDA; do not infer from the last discussed device.
2. Load the authoritative substrate/run `grid_positions.csv` and compute Euclidean distance from live `(x,y)` to every device target.
3. Report the nearest device, row/col, target `x,y`, signed offset as `live - target`, and distance in native units.
4. If the user then asks to save/continue grid data from that location, hand off to `vipsa-grid-measurement` and archive stale device folders before overwriting. See `vipsa-grid-measurement/references/retrofit-standalone-current-device-results-into-grid.md` and `vipsa-grid-measurement/references/grid-sequence-correction-and-device16-contact-gate-2026-07-27.md` for current-position boundary handoffs where an explicit Z move/approach must succeed before continuing later devices.

## Standard adjacent-device / grid-run sequence

For grid-run next-device travel with align and approach, use this default unless the user explicitly overrides distances:

1. Preflight active env and relevant machine states: `stage`, `zaber`, `light`, `keithley-2450`, `keithley-707b`.
2. Force electrical cleanup before travel: SMU outputs off and 707B open/nil.
3. Run the safe travel move:
   - `stage.move_z_by(height=-50, feedrate=450)`
   - `stage.get_position()` (current ViPSA stage edge rejects older `stage.get_current_position` with `UNKNOWN_COMMAND`)
   - Zaber native absolute or relative X/Y move to the next grid device
   - `zaber.get_current_position(units=None)`
4. Treat this travel move as a checkpoint. If it succeeds but a later phase fails, resume from alignment/approach and do **not** repeat the Z retract or grid-pitch move.
5. Run camera-1 pad alignment at the safe/retracted Z:
   - turn lights on
   - capture camera 1
   - if the first capture path fails after motion has already completed, retry with OpenCV RTSP capture before stopping
   - use the `900x900` center ROI dark-pad detector from `vipsa-vision-alignment`
   - use multiplier `21.5` native Zaber steps per pixel unless the user overrides it
   - apply up to two Zaber correction passes
   - capture and annotate a final verification image
6. Turn lights off, then run the grid pre-approach move:
   - `stage.move_z_by(height=+40, feedrate=450)`
   - verify/read back stage Z when practical
7. Run the established Keithley-guided contact approach:
   - route DUT to Keithley through 707B
   - test voltage `0.01 V`
   - target current window `10–100 nA` (`1e-8` to `1e-7 A`)
   - current compliance `1e-6 A`
   - forward +Z step typically `0.5` after the `+40` pre-approach move; use bounded max attempts sufficient to establish contact from the pre-approach position
   - retract/trim with minimum valid `0.25` Z increments when over-current
8. Cleanup electrical state in all cases:
   - `keithley-2450.set_output(false)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()` should be nil/no channels
   - verify final machine states are idle with `run_id: null` where available.

## References

- `references/named-device-absolute-navigation.md` — reusable named-device absolute-coordinate workflow.
- `references/named-device-absolute-grid-navigation-2026-07-23.md` — session-specific S1 device-22 correction, exact coordinates, deltas, and the verified readback pattern.
- `references/adjacent-device-grid-navigation-2026-06-16.md` — concrete run note covering right-device move, resumable checkpointing after a completed pre-move, OpenCV capture fallback for alignment, and reporting details.
- `references/camera-feature-pixel-to-zaber-clearance-move-2026-08-07.md` — distinguish calibrated image-feature moves from generic grid pitch; includes pixel-center measurement, `21.5` steps/px conversion, signs, uncertainty, exact Z-clearance sequencing, and readback verification.

## Reporting

Use concise operational reporting:

- State the grid move direction and exact signed move(s).
- Include final alignment residual in pixels and final annotated image attachment if available.
- Report approach final current, target window, net Z approach motion, final stage position, and cleanup status.
- Use 🎯 for alignment and 👇 for approach results.

## Safety notes

- Do not move Stage X/Y for grid navigation; grid pitch movement uses Zaber X/Y.
- Do not run DCIV/forming/pulsing automatically after approach. Ask for measurement parameters or wait for the user's next instruction.
- If any pre-move fails or cannot be read back, stop before alignment/approach rather than operating on an unverified position.
