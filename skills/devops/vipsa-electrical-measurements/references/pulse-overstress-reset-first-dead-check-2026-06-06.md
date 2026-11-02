# Pulse-overstress followed by reset-first DCIV dead-check — 2026-06-06

## Context

During live ViPSA memristor work, a bounded Keysight pulse optimization started from a previously safe pulse train and escalated SET/RESET voltage. The best safe candidate was weakly separated, while a stronger pulse condition caused a safety stop. The user then asked for a DCIV with an additional reset to verify whether the device was “DEAD dead.”

## Pulse optimization pattern

Use bounded pulse screening, not long endurance, when optimizing ON/OFF on one live device:

- Candidate train shape: repeated `SET → read → RESET → read`.
- Keep compliance fixed unless the user explicitly asks to change it.
- Escalate one variable at a time.
- Compute read-after-SET/read-after-RESET distributions, median SET/RESET ratio, absolute ON/OFF ratio, fractions above thresholds, max read current, and stress compliance-hit fraction.
- Stop if a low-voltage read reaches likely-short territory or stress compliance hits become unsafe.

Observed safe/weak best in this session:

- SET `+1.0 V`, RESET `-2.0 V`, read `+0.1 V`, width `5 ms`, compliance `10 µA`, 25 cycles.
- Median ON/OFF from read states: `~1.81×`.
- Max observed ON/OFF: `~5.48×`.
- Fraction cycles `≥5×`: `4%`.
- Read-after-SET median: `~1.09 nA`; read-after-RESET median: `~0.58 nA`.

Safety-stop escalation:

- `+1.5 V / -2.5 V / 5 ms` briefly increased median ratio (`~2.04×`) but the max read current reached `~10 µA`, so the screen stopped.
- A Keithley small-bias check after the stop showed `±10 mV` and higher biases near `1 µA` compliance, consistent with short-like / over-conductive behavior immediately after the pulse train.

## Reset-first DCIV dead-check pattern

When the user explicitly asks to check whether a pulse-stressed device is “DEAD dead,” run a reset-first DCIV and distinguish these outcomes:

1. Force Keithley output off and route DUT to Keithley.
2. Take a pre-read at `+10 mV` with low compliance.
3. Run extra reset first: `0 → -Vneg → 0`.
4. Run full cycle: `0 → +Vpos → 0 → -Vneg → 0`.
5. Preserve branch labels such as `RESET_PRE_NF`, `RESET_PRE_NB`, `PF`, `PB`, `NF`, `NB`.
6. Take a post-read at `+10 mV`.
7. Cleanup: Keithley output off, 707B open all, `get_closed_channels == nil`, verify machines idle.

Observed parameters:

- Extra reset first: `0 → -2 → 0 V`.
- Full cycle: `0 → +1 → 0 → -2 → 0 V`.
- Step: `50 mV`.
- Outward reset branches: `100 µA` compliance.
- Return/positive branches: `1 µA` compliance.
- Rows: `202 / 202`.

Observed result:

- Pre-read `+10 mV`: `4.39e-8 A` (`~228 kΩ`), not at `1 µA` compliance.
- Post-read `+10 mV`: `5.52e-8 A` (`~181 kΩ`), not at `1 µA` compliance.
- Extra reset outward `0→-2`: `10/41` hits at `100 µA`.
- Extra reset return `-2→0`: `38/40` hits at `1 µA`.
- PF `0→+1`: `18/21` hits at `1 µA`.
- PB `+1→0`: `15/20` hits at `1 µA`.
- Final reset outward `0→-2`: `8/40` hits at `100 µA`.
- Final reset return `-2→0`: `38/40` hits at `1 µA`.

## Reporting language

Use the distinction explicitly:

- Do **not** call this “fully dead/open” if the low-bias pre/post reads are measurable and not compliance-limited.
- Do **not** call it a permanent hard short if post-cleanup `+10 mV` is not at compliance.
- Do call it “badly damaged,” “mostly compliance-limited during sweep,” or “effectively cooked for useful switching” when most low-compliance branches hit compliance and reset does not recover a clean HRS.
- If extra reset does not recover HRS, say that directly.

This wording matters because a device can be unusable for robust switching while still not being literally open-circuit or hard-shorted at a gentle low-bias read.
