# Current-device approach with coarse 1.0 and later 0.5 trim (2026-06-24)

## User request
The user asked to approach the current device using:

- coarse forward approach: `+1.0` stage-Z steps
- later trim/backtracking: `0.5` stage-Z steps

The standard approach target was `10–100 nA` at `10 mV`.

## Observed behavior
The device showed a very sharp contact edge:

- Initial reads were pA-scale (`~5e-11 A`).
- Coarse `+1.0 Z` steps stayed pA-scale until a sudden jump to Keithley compliance (`~1e-6 A`).
- Repeated `-0.5 Z` trim steps remained compliance-limited for many steps.
- One additional `-0.5 Z` step then dropped straight back to pA/open-like current.
- Final state was safely below contact, but not stabilized in the `10–100 nA` window.

## Durable lesson
When the user explicitly requests coarse `1.0` steps and `0.5` trim, use those values, but if the current transition is sharp and `0.5` cannot land in the target window, report **contact edge too sharp for 0.5-step trim** rather than claiming successful contact. Do not invent a stabilized contact from either compliance-limited or pA/open-like readings.

If the user allows finer trim, switch final backtracking/forward trim to the hardware-supported minimum (`0.25` stage-Z steps). Never command smaller than `0.25`.

## Reporting pattern
Concise report should include:

- coarse/trim step sizes actually used
- initial current
- net Z where contact/over-contact appeared
- final current relative to target window
- final stage position/readback
- cleanup verification: SMU output off, 707B `open_all`, closed channels `nil`

Use 👇 for approach results.