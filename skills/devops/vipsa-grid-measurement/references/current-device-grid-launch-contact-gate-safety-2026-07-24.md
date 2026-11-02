# Current-device 7×7 launch: verified handoff and contact-gate safety

Use this pattern when the user identifies a substrate and asks to start a grid from the device that was just aligned and approached.

## Handoff

- Treat live Zaber X/Y as device 1; generate a fresh row-major grid at the established pitch and traverse serpentine.
- Record substrate identity, exact origin, live stage Z, prior alignment residual, and prior standalone approach current.
- Do not move Zaber, retract/re-lower Z, or repeat alignment before the first live contact check.
- Run the first contact check at the same bias/window used for approach (currently 10 mV and 50–500 nA, with 1 µA read compliance).

## Contact handling

- If the fresh check is in-window, reuse the handoff directly; do not call a full approach routine merely because the generic device loop normally does.
- If over-window or compliance-limited, retract Z in bounded minimum-valid −0.25-step increments and re-read until in-window or the attempt budget ends.
- If below-window, perform one bounded forward approach. Preserve all readings and net Z motion.
- If attempt 1 remains outside the window, perform the required optical recheck and one complete second bounded approach.
- **Before any optical alignment recheck after over-current or possible contact, retract Z to verified optical/travel clearance. Never move Zaber laterally while the probe may still be contacting the substrate.** After alignment, pre-approach conservatively and run the second electrical approach.
- Gate DCIV/pulses on the final numeric |I|, not the approach status text. If attempt 2 remains outside 50–500 nA, save `skipped_contact_not_in_window` and continue without electrical stress.

## Launch verification

Before reporting a verified start, confirm:

1. Runner remains alive.
2. `grid_positions.csv` contains the fresh device-1 origin and 49 rows.
3. `device_01/summary.json` is fresh and identifies the correct substrate.
4. Startup logs expose device start, first contact result, and retry phase; long approach loops should emit periodic progress so silence is not mistaken for a hang.
5. A stateful per-device reporter is recurring (`every 1m`, repeat forever), parses `summary.json` rather than treating `DONE.json` as proof of measurement, and stays silent when nothing new completed.

## Runner-clone audit

Search the final clone for stale substrate names, timestamps, prior contact currents, output paths, start-device metadata, and recording policy. Compile before launch. Create the log directory before starting a `tee` pipeline.
