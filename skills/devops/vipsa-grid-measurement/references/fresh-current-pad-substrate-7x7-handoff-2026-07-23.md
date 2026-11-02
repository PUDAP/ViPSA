# Fresh current-pad substrate 7×7 handoff (2026-07-23)

Use this pattern when the user identifies a new substrate and says to start a 7×7 grid “from here” after alignment/contact has already been established on the current pad.

## Verified launch pattern

1. Treat the live Zaber X/Y readback as **device 1**, not as a coordinate inherited from an earlier substrate/run.
2. Generate a fresh row-major 7×7 position file from that origin using the established native-unit spacing (5000 in this session), then traverse it serpentine.
3. For device 1, do **not** retract for travel, move Zaber, or repeat optical alignment. Preserve the current lateral position and perform a live low-bias contact check first.
4. Enforce the current contact policy at the same bias used to establish contact. In this session the gate was **50–500 nA at 10 mV**, with 1 µA read compliance so the upper bound was observable.
5. If the first live check is over the window/compliance-limited, retract Z in minimum valid **−0.25-step** increments and re-read until the current enters the window or the bounded retry policy terminates. The S5 launch entered the window at 214.1 nA after −1.5 Z steps.
6. Save device-1 handoff metadata: substrate, live Zaber origin, stage Z before/after contact adjustment, prior standalone approach result, live check result, and the fact that initial X/Y movement/alignment was intentionally skipped.
7. For later devices, use normal cleanup → safe Z retract → absolute Zaber X/Y move → pre-approach → alignment → bounded approach.
8. Verify the runner is alive and that `grid_positions.csv`, `device_01/summary.json`, and `device_01/approach.json` contain fresh values before reporting that the run started.

## Runner-cloning checklist

When adapting an existing grid runner, explicitly replace and verify all of the following before launch:

- substrate and output hierarchy
- fresh timestamp/run directory
- `START_AT_DEVICE=1`
- live-origin behavior rather than resume-grid reuse
- approach test voltage, bounds, and read compliance
- current camera/RTSP endpoint used by alignment
- stale named-device coordinates and handoff notes
- resume/archive events and old-device preservation logic
- recording policy
- NATS server list appropriate to the active bridge

Compile the final script and search it for stale substrate names, old start-device constants, old camera hosts, and named-device resume strings. A syntactically valid clone can still be physically wrong if any of these stale fields remain.

## Reporting

A concise verified start report should include: substrate, live device-1 origin, grid spacing/traversal, contact-gate result and any Z adjustment, current stage Z, active device, run directory, and whether recording is enabled.