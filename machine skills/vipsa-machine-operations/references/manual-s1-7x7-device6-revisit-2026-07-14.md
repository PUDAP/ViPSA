# Manual S1 7x7 device revisit: device 6 aligned target

Use this pattern when the user asks to move back to a device from a prior S1 7x7 grid run, without restarting the runner.

## Session pattern

A terse request like `move to device 6 from s1 7x7 run` should be treated as an immediate hardware move request when the run artifacts identify the target.

1. Load the prior run artifacts and device summary.
   - Run folder used here: `data/probabilistic_computing/batch_1/substrate_S1/runs/grid_7x7_batch1_S1_currentdevice_dciv0p6_randomized_10000pulses_20260701T070136Z/`
   - `device_06/summary.json` contained grid target:
     - `x=49383.0`
     - `y=494373.0`
   - The associated restart log recorded the previous alignment correction for device 6:
     - `alignment_move: {"x": 521, "y": -48}`
2. Compute the aligned absolute Zaber target, not a relative move:
   - `x = 49383 + 521 = 49904`
   - `y = 494373 - 48 = 494325`
3. Keep the microscope stage at a safe negative Z before Zaber X/Y travel.
   - In this session the user had just moved stage down to `z=-35`, verified by `stage.get_current_position()`.
   - Do not move stage X/Y.
4. Before Zaber travel, verify/force electrical safety with separate short PUDA protocols if needed:
   - `keithley-2450.set_output(enabled=false)`
   - `keysight-b2902b.set_output(enabled=false)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()` should return `nil`
5. Move Zaber using absolute native units:
   - `zaber.move_x_to(position=49904, units=null)`
   - `zaber.move_y_to(position=494325, units=null)`
6. Verify with separate readback protocols:
   - `zaber.get_current_position(units=null)` returned `x=49904`, `y=494325`
   - `stage.get_current_position()` still returned `z=-35`
   - final states for stage, zaber, Keithley, Keysight, and 707B were `idle`, `run_id: null`

## Reporting

Keep the report concise:

- Identify the source run and whether the target is raw grid target or aligned target.
- Report grid target, alignment correction, final commanded/readback Zaber X/Y, stage Z, electrical cleanup, and final idle states.
- Do not claim electrical contact or alignment was freshly verified unless a fresh camera/electrical step was actually run.
