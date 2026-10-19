# Consecutive high-voltage RESET/read pairs under compliance (2026-07-24)

Use this pattern when the user asks for a short sequence such as “10 sets of consecutive `-2.5 V` RESET and `+0.1 V` read pulses” on the current contacted device.

## Execution pattern

1. Run the canonical low-bias Keithley/707B precheck before applying new stress. Preserve its artifact path and classify contact from paired-bias voltage scaling rather than one current point.
2. Interpret each “set” in this request as one **pair**: `RESET -> read`. Thus 10 sets means 20 physical pulses. State this count explicitly.
3. Unless the user changes established safe settings, retain the most recent pulse width and compliance and record them as defaults/assumptions (in this session: `2 ms`, `100 uA`).
4. Prefer one PUDA protocol with lifecycle-managed machines and explicit command cleanup:
   - Keysight output off
   - 707B route to Keysight
   - one `run_voltage_pulse_train` list such as `[-2.5, +0.1] * 10`
   - Keysight output off
   - 707B `open_all`
   - 707B `get_closed_channels`
5. Save the full PUDA log and a compact CSV with pair index, commanded RESET/read voltages, measured currents, and measured voltages when available.
6. Verify electrical machines idle and 707B channels nil after COMPLETE.

## Compliance interpretation

A commanded voltage is not necessarily the voltage delivered to the DUT. When RESET current reaches compliance, report all three:

- commanded RESET voltage,
- measured RESET voltage range,
- RESET compliance-hit count.

Do not say the full requested voltage was physically applied when measured voltage collapsed under compliance. In the concrete run, all 10 RESET pulses reached the `100 uA` limit and the measured voltage was only about `-2.18` to `-2.23 V` despite a `-2.5 V` command.

Report the read-current sequence/range separately. The `+0.1 V` reads rose from `20.3 nA` to `162.1 nA` (median `41.05 nA`), so the repeated negative pulses did not monotonically recover a lower-current HRS. Avoid calling the sequence a successful RESET merely because the RESET stress polarity and amplitude were requested.

## User-facing minimum report

- pairs and total physical pulses completed,
- commanded RESET/read voltages,
- pulse width and compliance,
- measured RESET-voltage range when compliance-limited,
- RESET and read compliance-hit counts,
- read-current start/end or range,
- cleanup and final idle/open-switch verification.
