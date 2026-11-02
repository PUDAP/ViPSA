# Named-device absolute navigation

Use this workflow when the user names a substrate and device number (for example, “device 22 from S1”). This is distinct from a relative request such as “move one device left.”

## Workflow

1. Locate the active substrate/run’s authoritative `grid_positions.csv` and read the row for the requested `device_number`. For a stopped grid run, prefer the CSV copied into that run directory.
2. Read live Stage-Z and Zaber X/Y through a harmless PUDA position protocol. Do not infer current location from buffered runner output.
3. If the request follows a stopped electrical run, require already-verified output-off/open-all cleanup and no surviving runner before travel.
4. Retract stage Z for clearance once, unless a verified clearance retraction is already the current checkpoint. Do not repeat the retraction after an interrupted/resumed lateral move.
5. Compute signed native-unit deltas:
   - `dx = target_x - current_x`
   - `dy = target_y - current_y`
6. Prefer one PUDA motion protocol with absolute native-unit targets:
   - `zaber.move_x_to(position=target_x, units=None)`
   - `zaber.move_y_to(position=target_y, units=None)`
   Relative moves are acceptable only when based on the fresh readback and computed deltas.
7. Run a separate read-only position protocol after motion. Require exact final Zaber readback equal to the CSV target and verify Stage/Zaber are `idle` with `run_id: null`.
8. For a terse “move to device N” request, stop here: do not automatically align, approach, or measure. Report starting position, deltas, target, final readback, and that those follow-on phases were not run.
9. If Stage-Z telemetry is known to be software-tracked, label it as edge/readback evidence—not independent physical-motion proof.

## Critical distinction

Never infer a named device’s destination by assuming the current device number and applying a single ±5000 grid-pitch move. Camera alignment corrections, prior manual moves, a different substrate origin, or stale conversational context can make that assumption wrong. Use ±5000 only for explicit relative-neighbor requests.

## Session example

For the S1 7×7 grid, device 22 was `(24383, 509373)`. A mistaken relative move reached `(4469, 459218)`; correcting from the live position required `dx=+19914`, `dy=+50155`, followed by exact readback `(24383, 509373)`.
