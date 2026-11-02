# Offset-dominated low-bias resistance immediately before approach

Session pattern from 2026-07-01 ViPSA work.

## Measurement pattern

A quick low-bias Keithley/707B resistance check after lights-off produced nearly identical current at every small bias:

- `0 V`: `~1.43e-10 A`
- `+10 mV`: `~1.43e-10 A`
- `-10 mV`: `~1.43e-10 A`
- `+50 mV`: `~1.43e-10 A`
- `-50 mV`: `~1.43e-10 A`

Because the current did not scale with voltage and matched the zero-bias offset, offset-corrected and paired differential resistance were not meaningful. The appropriate user-facing interpretation was open-like / very high resistance, not a precise `R = V/I` value.

## Follow-up nuance

A subsequent explicit `approach` request should still be run. In this session, the approach routine's first live `10 mV` read was already in the target contact window (`~74 nA`) and therefore no Z motion was commanded. This can happen because contact-edge state/read conditions can change between a compact diagnostic and the approach routine.

## Reporting rule

For low-bias checks with identical pA/sub-nA currents across `0 V`, `±10 mV`, and `±50 mV`:

- Report the current table.
- State that paired/offset-corrected resistance is not meaningful because the bias response is indistinguishable from offset.
- Classify as open-like / very high resistance for that diagnostic.
- If the user then asks to approach, do not cite the diagnostic as a blocker; run the fresh approach read and gate motion from that result.
