# DCIV-until-good then pulse-screen handoff (2026-06-06)

## Context

After contact approach and an initial split-compliance Keithley DCIV, the user asked to keep running DCIV sweeps until the device showed a good SET/RESET transition, then perform a pulsed measurement.

The device had just passed a non-stressing health check after the prior DCIV:

- `+0.01 V`: `~5.57e-11 A` (`~180 MΩ`)
- `+0.10 V`: `~1.17e-10 A`
- `-0.10 V`: `~-2.28e-11 A`
- Far below `1 µA` compliance; alive, not shorted, not open.

## Bounded DCIV search pattern

Use a bounded search rather than an unbounded “until good” loop. Start with the last safe recipe before escalating:

1. Confirm Keithley/707B idle and force Keithley output off.
2. Route DUT to Keithley via 707B (`connect_keithley_smu`, observed channels `1A01`, `1B03`).
3. Run candidate sweeps one at a time, saving CSV/JSON/plot after each.
4. Stop as soon as a sweep satisfies the SET/RESET criteria.
5. Cleanup after the DCIV stage: Keithley output off, 707B open_all, verify closed channels `nil`.

Candidate order used successfully:

```text
1. repeat_previous:       0 → +1.0 → 0 → -2.0 → 0 V
2. slightly_deeper_reset: 0 → +1.0 → 0 → -2.5 → 0 V
3. slightly_stronger_set: 0 → +1.2 → 0 → -2.5 → 0 V
4. moderate_set_reset:    0 → +1.5 → 0 → -3.0 → 0 V
```

Common settings:

```text
step: 0.05 V
requested delay: 0.001 s
PF compliance: 1 µA
PB compliance: 1 µA
NF compliance: 0.1 mA
NB compliance: 1 µA
```

Segment construction should keep the total point count correct by not duplicating vertices:

```text
PF: 0 → +Vpos inclusive
PB: Vpos-step → 0
NF: -step → Vneg
NB: Vneg+step → 0
```

For the original `0 → +1 → 0 → -2 → 0 V` recipe, this yields `21 + 20 + 40 + 40 = 121` points.

## “Good enough” DCIV scoring used

The first repeat sweep met criteria, so no escalation was needed:

- SET-like jump: `+0.60 → +0.65 V`, `4.79e-10 A → 1.00e-6 A`, `3.32 decades`
- RESET-like drop: `-0.05 → -0.10 V`, `-1.04e-10 A → -3.20e-11 A`, `0.51 decades`
- ON/OFF estimate at `0.1 V` (`PB/PF`): `~2240×`
- After-reset ratio (`NB/PB` at `0.1 V`): `2.78e-4`
- PF/PB hit `1 µA` compliance; NF/NB did not hit compliance.

Practical criteria used:

```text
SET jump >= 0.5 decades
RESET drop >= 0.5 decades
ON/OFF >= 5x at comparable read voltage
After-reset/read-after-SET ratio <= 1/5
No hard short / no low-voltage compliance-limited read
```

Use cautious wording: this is a “good SET/RESET-looking DCIV transition” or “good enough to hand off to pulse screening,” not proof of robust bipolar endurance.

## Pulse handoff pattern

After a good DCIV, do a bounded Keysight pulse screen, not a long endurance run. Use small batches and stop if reads become compliance-limited or stress compliance fraction becomes excessive.

Screen used:

```text
read voltage: 0.1 V
compliance: 10 µA
cycles per candidate: 30
sequence: SET, read, RESET, read
```

Candidates screened:

```text
1. SET +0.8 V, RESET -2.0 V, width 1 ms
2. SET +1.0 V, RESET -2.0 V, width 1 ms
3. SET +0.8 V, RESET -2.0 V, width 5 ms
4. SET +1.0 V, RESET -2.0 V, width 5 ms
5. SET +1.0 V, RESET -2.5 V, width 5 ms
```

Selection/reporting metrics:

- Median read-after-SET current
- Median read-after-RESET current
- Median ratio `I_read_after_SET / I_read_after_RESET`
- Fraction of cycles with ratio `>= 5`
- Max read current
- Stress compliance-hit fraction

In this run, the best safe candidate was `+1.0 V SET / -2.0 V RESET / 5 ms`:

- Read-after-SET median: `1.24e-9 A`
- Read-after-RESET median: `9.35e-10 A`
- Median ratio: `1.39×`
- Good cycles with ratio `>=5×`: `0%`
- Max read current: `1.52e-9 A`
- Stress compliance-hit fraction: `0.5`

Interpretation: the DCIV showed a good SET/RESET-looking transition, but pulse separation was weak and not robustly optimized. Report that distinction clearly; do not call the pulse condition optimized just because DCIV looked good or stress pulses hit compliance.

## Cleanup/reporting checklist

Always verify and report:

- Keithley output off after DCIV
- Keysight output off after pulse screen
- 707B `open_all` success
- 707B closed channels: `nil`
- Keithley, Keysight, 707B, stage, light states idle
- Attach best DCIV plot/CSV and pulse plot/CSV/summary JSON
