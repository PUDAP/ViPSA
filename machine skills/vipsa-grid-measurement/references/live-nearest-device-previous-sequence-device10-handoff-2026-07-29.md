# Live nearest-device reconciliation and previous-sequence handoff (2026-07-29)

## Trigger
Use when the user asks which grid device is closest to the current position, or asks to move to a previous/next device in grid sequence before aligning/approaching.

## Pattern
1. Read live Zaber X/Y via `zaber.get_current_position(units=None)`; do not infer the current device from chat history or stale folders.
2. Compare live X/Y against the relevant substrate `grid_positions.csv` by Euclidean distance in native units.
3. Report the nearest device with target X/Y, live offset, and next-nearest distance.
4. If the user names a sequence relation (e.g. “previous device in the grid sequence (Device 10)”), treat the named device as authoritative and use its absolute target from the grid CSV, even if numeric order/serpentine direction could be ambiguous.
5. Before Zaber X/Y travel from a recently contacted device:
   - force SMU outputs off,
   - `keithley-707b.open_all()` and verify `get_closed_channels == nil`,
   - turn lights off,
   - retract microscope stage Z by the configured safe travel amount (current default `stage.move_z_by(-50)`).
6. Move Zaber using absolute native targets: `move_x_to(position=<x>, units=None)`, `move_y_to(position=<y>, units=None)`.
7. Run canonical `tools/align.py --execute ... --final-light off` and require a small residual before approach. In the session, device 10 alignment residual was `2.82 px`.
8. After alignment, do the current grid-default pre-approach move `stage.move_z_by(+40)` and then run the bounded Keithley-guided approach.
9. If approach ends at read compliance / over-current after trim, report it as over-contact/compliance-limited, not stable in-window; verify cleanup and idle/null states.

## Concrete example
- Live Zaber `(271765, 490910)` against S9 7x7 grid gave closest device 9: target `(271765, 491131)`, offset `(0, -221)`, distance `221` native units.
- User then asked for previous device in sequence and explicitly named Device 10. Device 10 target from the S9 grid was `(276765, 491131)`.
- Handoff sequence used cleanup → `stage -50` → Zaber absolute move to device 10 → align → `stage +40` → approach.
- Final approach was not stable: it ended compliance-limited around `1 µA` at `10 mV`, with 707B open/nil and machines idle after cleanup.
