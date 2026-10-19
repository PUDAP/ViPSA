# Repeat a custom bounded approach after no contact

Use this when a Keithley-guided approach ends as `no_contact_after_max` and the user immediately says `approach` or `approach again` without supplying new parameters.

## Continuation semantics

- Treat the request as a **new bounded block from the verified current Stage-Z position**. Do not zero, retract, replay alignment, or repeat an earlier pre-move unless explicitly requested.
- Preserve the **entire immediately preceding approach recipe**, including custom target window, test voltage, compliance, signed direction, coarse step, settle time, and per-block maximum. Do not silently revert to the generic 10–100 nA defaults.
- Example: after a 50–500 nA, `+0.5 Z`, 140-move block misses contact, a terse `approach` means another independently bounded 140-move block at 50–500 nA and `+0.5 Z` from the current position.
- Re-read live current before any motion. If already in-window, move zero steps and stabilize/clean up.
- Run a fresh preflight: no competing grid/approach runner, required bridge/PUDA route available, and `stage`, `light`, `keithley-2450`, and `keithley-707b` idle with null run IDs.
- Keep lights off throughout the electrical phase.
- For a long block, run it as a tracked background process with completion notification and persist `summary.json` incrementally or at completion.

## Completion and reporting

Report:

- status (`in_window`, contact-edge result, or `no_contact_after_max`),
- final signed current and relation to the target window,
- travel in this block and final cumulative Stage-Z readback,
- Keithley output-off response,
- 707B `open_all` plus `get_closed_channels == nil`,
- final idle/null states for involved machines.

Successful stage movement alone is not contact. If current remains at the pA/sub-nA floor, report no contact honestly and do not automatically run DCIV.