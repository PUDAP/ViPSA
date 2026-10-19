# PEA signed-current interpretation and direct approach cleanup (2026-06-29)

## Context

During a ViPSA PEA-based memristor session, the user corrected the interpretation of low-current Keysight/Keithley reads:

- With the current TE probing polarity, **negative current at positive applied voltage indicates open circuit or very high HRS**.
- Do **not** interpret negative positive-bias reads as retained conduction/LRS, even if the absolute current gives a finite-looking resistance.
- For contact approach thresholds, continue using `abs(I)` for lower/upper threshold decisions unless the user explicitly requests signed-current logic, but always report the signed current and avoid overstating contact quality.

## Approach run pattern captured

A verified approach used:

```text
test_voltage = +0.01 V
lower_current_threshold = 1e-8 A
upper_current_threshold = 1e-7 A
current_compliance = 1e-6 A
forward direction = +Z
coarse step = +0.5 Z
trim step = 0.25 Z
lights = off before approach
```

The direct-NATS orchestrator turned the lights off, forced Keithley output off, routed the DUT to Keithley through the 707B, then looped Keithley `hold_voltage_measure_current` and `stage.move_z_by(+0.5)`. Contact entered the requested window after net `+2.0 Z` with a positive current around `1.09e-8 A`, and stage readback returned `z=110.75`.

## Cleanup / verification lesson

PUDA CLI `machine state` checks can time out during the WSL/Tailscale/NATS advertised-route issue even while direct NATS command transactions work. In that case:

1. Do not claim final `puda machine state` values that were not retrieved.
2. Verify safety using fresh direct command transactions:
   - `keithley-2450.set_output(enabled=false)` returns success.
   - `keithley-707b.open_all()` returns success.
   - `keithley-707b.get_closed_channels()` returns `nil`.
   - `stage.get_current_position()` returns a fresh readback when relevant.
3. If an earlier cleanup `complete` response timed out, send/verify a later direct `complete`; if it returns `RUN_ID_MISMATCH` / `not active`, that old run is no longer active, then run a fresh output-off transaction.
4. Report the CLI-state timeout as a control-plane verification blocker, not as an electrical or mechanical result.
