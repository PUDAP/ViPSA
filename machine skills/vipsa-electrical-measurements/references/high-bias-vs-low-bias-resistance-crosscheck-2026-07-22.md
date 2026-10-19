# Cross-checking high-bias and low-bias resistance on ViPSA DUTs

Use this when a user requests resistance at a specific high bias (for example `1 V`) and later asks for an ordinary resistance check.

## Measurement and interpretation

- Honor the requested voltage, but retain a conservative read compliance unless the user overrides it (commonly `1 µA`).
- Use multiple reads and report the individual current trend plus a robust central resistance estimate. If current changes materially across reads, report the resulting resistance range; do not present one number as a stable ohmic resistance.
- A high-bias point and a low-bias differential check answer different questions. A DUT may show MΩ-scale apparent resistance at `1 V` while a later `±10/±50 mV` differential check is GΩ/open-like because of nonlinear conduction, transient charging, or time dependence.
- Do not overwrite the low-bias classification with the earlier high-bias number. Label the bias and method every time.
- For the ordinary low-bias check, prefer paired differential resistance: `R = (V+ - V-) / (I+ - I-)`, especially when zero-bias offset is comparable to the signal.

## Parsing pitfall

Keithley response payloads can expose the same readings under overlapping key names (for example `I_meas (A)` and generic current aliases). Do not concatenate regex matches across aliases and then claim extra samples. Parse the structured response once, select one canonical current field per measurement record, and verify the parsed sample count equals `read_count`.

## Cleanup

Turn lights off before electrical routing, then always disable Keithley output, open all 707B channels, verify closed channels are `nil`, and verify idle/null-run states. Mention that lights remain off after the electrical check when that changes the user’s prior requested lamp state.
