# Contact approach: one-time step-size override and trim overshoot

## Context

During a ViPSA Keithley-guided contact approach, the user requested a one-time change: run the standard approach, but use `step_size=1` instead of the recent/default `0.5`.

Use the usual established approach defaults unless otherwise specified:

- `test_voltage = 0.01 V`
- `lower_current_threshold = 1e-8 A`
- `upper_current_threshold = 1e-7 A`
- `settle_delay = 0.2 s`
- `forward = +Z`
- user override for this run only: `step_size = 1`

## Observed behavior

- Initial read detected contact immediately at about `1e-6 A`, i.e. compliance/over-current.
- Retraction required many half-steps plus extra retracts before current dropped near the upper threshold.
- Stabilized current could rise again after waiting.
- A bounded final trim of `-0.1 * step_size` overshot from above the upper threshold to below the lower threshold.

## Durable workflow lesson

When a user gives a one-time step-size override, change only `step_size`; keep the other established approach defaults unless they explicitly change them.

After high-current contact, final trim should be bounded and remeasured after each trim. However, larger step sizes make `0.1 * step_size` less fine. If trim causes the final current to fall below `lower_current_threshold`, report the approach as **not stabilized in the contact window** rather than successful contact, even if a finite resistance can be computed.

## Reporting standard

For this class of run, report compactly:

- requested step size and thresholds
- whether contact was detected and whether it was over-current/compliance-limited
- retract/trim counts or coarse summary
- final current relative to the lower/upper threshold window
- computed resistance only as secondary context
- net Z change and final stage position
- cleanup verification: Keithley output off, 707B closed channels `nil`, machines idle
