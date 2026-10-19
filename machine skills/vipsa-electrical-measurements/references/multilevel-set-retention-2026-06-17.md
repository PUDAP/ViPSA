# Multi-level SET retention on current ViPSA device (2026-06-17)

Use this reference for user requests like “check if the filament dissolves with time”, “SET pulse then read at 0.1 V”, or “multi-level SET test with successive 100 s reads at several SET compliances.”

## Measurement pattern

- Use Keithley + 707B when the requested operation is a voltage SET pulse followed by low-bias read-current retention.
- Route DUT to Keithley once, then keep the session/routing stable for the whole sequence.
- For each SET level:
  1. Optional/preferred: take a pre-read at the requested read voltage immediately before the SET level.
  2. Apply one SET pulse with `run_voltage_pulse_train(voltages=[Vset], current_compliance=Icomp, pulse_width_s=...)`.
  3. Record the returned SET-pulse current and whether it actually reached compliance.
  4. Repeatedly read with `hold_voltage_measure_current(voltage=Vread, current_compliance=read_compliance, reset=False)` at the requested timepoints.
  5. Store `target_time_s`, actual `elapsed_after_set_s`, voltage, current, abs current, SET compliance, and row kind.
- For a cumulative multi-level test, use increasing SET compliances without RESET between levels unless the user explicitly requests reset/reinitialization. The pre-read before each level then documents the state carried forward from previous levels.
- Save partial CSV/JSON before cleanup so data survives even if later plotting or cleanup parsing fails.

## Example defaults used successfully

- SET voltage: `+1.0 V`
- SET pulse width: `10 ms` when the user did not specify pulse width and prior session context used 10 ms SET pulses.
- SET compliances: user-specified sequence such as `1e-7, 1e-6, 1e-5, 1e-4 A`.
- Read voltage: `0.1 V`.
- Read timepoints for “100 s read”: `0, 1, 2, 5, 10, 20, 40, 60, 80, 100 s`.
- Read compliance: choose and report a safe non-stressing read compliance; `1e-5 A` preserves headroom for multi-level conductance but still bounds a low-voltage short. If a read hits compliance, report the current/resistance as compliance-limited rather than precise.

## Interpretation rules

- Do not infer a retained filament merely because a SET pulse reached compliance. The decisive evidence is the low-bias read current after the pulse and its time dependence.
- For each compliance level report:
  - SET-pulse current and whether it hit SET compliance.
  - First read current at `Vread`.
  - Last read current at the requested final time.
  - `last / first` absolute-current ratio.
  - Approximate first/last resistance if not compliance-limited.
  - Any read-compliance hits.
- If high requested SET compliances return only sub-nA SET-pulse current and all 0.1 V reads remain clustered near the baseline pA/sub-nA value, report “no clear retained multi-level SET states” rather than treating requested compliance as achieved device programming.
- For filament dissolution/volatile retention, plot `|I_read|` vs elapsed time on a log y-axis. A dissolving filament should show a clear decay in low-bias read current after a real SET/LRS state; a flat pA/sub-nA trace means the device likely never strongly formed under that pulse condition.

## Plot/report pattern

Create one plot with:

1. Time traces: elapsed time after each SET pulse vs `|I|` at read voltage, log y-axis, one line per SET compliance.
2. Bar/summary panel: first read vs final read for each SET compliance, log y-axis.

Always report artifact paths for CSV, summary JSON, PNG, and PDF where available.

## Contact-pressure rerun pattern

If a multi-level SET-retention run stays pA/sub-nA and the user asks to press the contact tighter before changing electrical conditions, execute the mechanical contact change first and then rerun the exact same electrical recipe so the before/after comparison isolates contact pressure.

- Use the user's ViPSA convention: stage Z `+` / up / forward presses the contact tighter. Respect the requested increment; do not move X/Y.
- For a request like “move z stage up by 0.5 and run the same protocol again,” command `stage.move_z_by(height=+0.5, feedrate=450)` and verify readback before electrical stress.
- Record before/after stage position in the run summary. In one verified rerun, Z readback changed `[0, 0, 3.0] -> [0, 0, 3.5]` for `+0.5`.
- Rerun the same SET voltage, pulse width, compliance list, read voltage, read compliance, and timepoints. Do not silently change pulse width/voltage/compliance just because the previous result was weak.
- Compare baseline/current levels before vs after pressing. A small pA/sub-nA increase after contact pressure is not sufficient evidence of robust contact or retained LRS if high-compliance SET pulses still draw only sub-nA and low-bias reads remain clustered around baseline.
- If plot generation is blocked but CSV/summary data exists, still report the verified numeric comparison and artifact paths; do not rerun the electrical stress merely to obtain a plot.

## Cleanup

Always run and verify:

- Keithley `set_output(false)`.
- 707B `open_all()`.
- 707B `get_closed_channels()` returns `nil` / no closed channels.
- `complete` sent for Keithley and 707B direct-NATS sessions.
