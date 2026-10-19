# Repeating a bounded step-size-1 contact approach after no contact

Use this when a standard Keithley-guided approach ends at its bounded maximum with pA/sub-nA current and the user says “try approach again” with the same step size.

## Durable continuation rule

- Treat the request as a **new bounded block from the current physical Z position**; do not zero, retract, or replay earlier moves unless requested.
- Re-run preflight and preserve the established electrical defaults unless explicitly overridden: `10 mV`, `1 µA` compliance, `10–100 nA` target window, `+Z` approach, `0.2 s` settle.
- For step size `1`, use the same bounded block (typically 100 moves) and stop again if contact remains below threshold.
- Report both **travel this run** and **cumulative stage readback** so repeated blocks are unambiguous.
- Do not infer contact from successful PUDA motion/readback alone. Contact requires the electrical threshold.
- Always finish with Keithley output off, 707B `open_all`, `get_closed_channels == nil`, lights off, and all involved machines idle with `run_id: null`.

## Example outcome pattern

A first 100-step block can end at `[0,0,100]` with pA current. If the user repeats the approach, another 100-step block should continue from there and may end at `[0,0,200]`. If the current still stays at the pA noise floor, report `no_contact_after_max`; do not call the second run contact merely because cumulative travel increased.
