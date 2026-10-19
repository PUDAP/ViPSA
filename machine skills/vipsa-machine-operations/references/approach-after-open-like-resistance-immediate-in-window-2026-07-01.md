# Approach after open-like resistance can be immediately in-window

Session pattern from 2026-07-01 ViPSA work.

## Context

The user asked to turn lights off and check resistance, then later asked simply `approach`.

Immediately before approach, a compact Keithley low-bias diagnostic measured the same current at all biases:

- `0 V`: about `1.43e-10 A`
- `+10 mV`: about `1.43e-10 A`
- `-10 mV`: about `1.43e-10 A`
- `+50 mV`: about `1.43e-10 A`
- `-50 mV`: about `1.43e-10 A`

That was correctly reported as open-like / very high resistance and not a meaningful paired differential resistance.

The user then asked `approach`. The standard direct approach routine (`10 mV`, target `10–100 nA`, `0.5` Z coarse step, max `180`, lights off, Keithley routed through 707B) measured the *initial* current as already in-window:

- initial/stabilized current: about `7.42e-8 A` (`74 nA`) at `10 mV`
- net Z movement during approach: `0.0` steps
- stage readback stayed at the existing Z (`430.25` in that session)
- cleanup verified: Keithley output off, 707B open/`nil`, stage/light idle/null

## Durable lesson

Do not treat a prior pA/sub-nA low-bias resistance check as a reason to skip a later explicit `approach` request. Re-run the approach's fresh low-bias read and branch from the live result.

If the approach's first read is already inside the target window:

1. Do not command any additional forward Z motion.
2. Take the stabilization/read confirmation used by the approach routine.
3. Report `in_window`, final current, target window, and `net_z_steps: 0.0` explicitly.
4. Still perform full cleanup: `set_output(false)`, `open_all`, `get_closed_channels`, complete involved machines, verify idle/null states.

This is not a contradiction of the earlier open-like report; small-current diagnostics can be offset/noise-dominated and contact state may change with rerouting, SMU reset/read mode, settling, or contact edge behavior. The actionable rule is to trust the fresh approach read for motion gating and to avoid unnecessary Z motion once in-window.
