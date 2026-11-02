# Manual Z move followed by current measurement (2026-07-01)

## Trigger

Use this when the user explicitly combines a microscope-stage Z move with a terse current measurement request, for example:

```text
move z stage up by another 50 steps and measure current
```

This differs from `check resistance`: the user asked for **current**, not a full low-bias resistance diagnostic.

## Workflow

1. Execute the authorized Stage-Z move first using the current ViPSA convention:
   - `up` = positive Z (`stage.move_z_by(height=+N, feedrate=450)`)
   - `down` = negative Z
2. Verify Stage-Z readback with `stage.get_current_position()` and final stage idle/null state.
3. Turn lights off if they were on before electrical measurement.
4. Route DUT to Keithley through the 707B and force Keithley output off before routing.
5. For a terse `measure current` request with no voltage specified, default to a direct current read at **+0.1 V** with conservative compliance (typically `1e-6 A`) and `settle_s ~= 0.2`, `read_count=3`.
6. If the user says `check resistance`, `low-bias resistance`, or asks whether it is open/shorted, use the multi-bias diagnostic (`0 V`, `±10 mV`, `±50 mV`, optional `±100 mV`) instead.
7. Cleanup in all cases:
   - `keithley-2450.set_output(false)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()` should be `nil`
   - Verify Keithley/707B idle/null.

## Reporting

Keep it compact:

- signed Z move and readback Z
- current at `+0.1 V` (or the user-specified voltage)
- whether the current is pA/sub-nA/open-like, nA contact-like, or compliance-limited
- cleanup verification

## Pitfall captured

Do not silently substitute a full resistance sweep for a terse `measure current` request. If no voltage is specified, use `+0.1 V` as the default current-measurement bias; reserve the full multi-bias table for `check resistance` or diagnostic/classification requests.
