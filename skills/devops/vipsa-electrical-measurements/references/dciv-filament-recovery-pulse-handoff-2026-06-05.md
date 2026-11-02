# DCIV filament-recovery and pulse endurance handoff (2026-06-05)

## When this applies

Use this note when a ViPSA perovskite/memristor device appears to have a "lack of proper reset" or possible filament damage after a prior aggressive SET/compliance condition, and the user asks whether it is permanent and to recover SET/RESET behavior safely.

## Reusable lessons

- Do not assume a previously SET-only or poor-reset device is permanently damaged. First run a conservative DCIV recovery search and classify the current device state electrically.
- Start with a lower SET-side compliance and bounded positive voltage, then allow a stronger but still safe negative RESET branch. In the observed recovery case, a clean transition returned with:
  - sweep: `0 -> +0.8 -> 0 -> -2.0 -> 0 V`
  - step: `0.05 V`
  - PF/PB/NB compliance: `200 nA`
  - NF/reset compliance: `5 uA`
  - SET-like jump near `+0.20 V`
  - RESET-like drop near `-0.15 V`
  - `+0.1 V` read currents: initial HRS `~1.0e-10 A`, after SET `~2.0e-7 A`, after RESET `~6.3e-11 A`
- Treat this as evidence that the present state is not a permanent hard short, while avoiding overclaiming that no microscopic irreversible change occurred.
- A DCIV recipe with strong contrast does not necessarily transfer directly to pulse endurance. In the observed handoff, Keysight pulse candidates near the recovered DCIV voltages produced only weak nA-scale read separation despite completing safely.
- For pulse screening, use small batches (for example 30 cycles) and choose the best *safe* candidate only if no candidate meets robust separation. Report explicitly when the best candidate is only "best available" rather than truly optimized.
- In the observed pulse handoff, the best available 30-cycle condition was `SET=+1.0 V`, `RESET=-2.0 V`, `READ=+0.1 V`, width `5 ms`, compliance `10 uA`, but median read ratio was only `~1.5x`; it should not be called robust switching.
- For endurance after a weak screen, run bounded batches with safety guards and report cycle-completion separately from switching quality. A completed 1000-cycle run can still have poor memory contrast.
- Include cleanup verification after both Keithley DCIV and Keysight pulse runs: SMU output off, 707B `open_all`, `get_closed_channels == nil`, and final machine states idle.

## Reporting language

Good phrasing:

- "Probably not permanently shorted in the current device state; conservative DCIV recovered clean SET/RESET."
- "The pulse protocol completed safely, but read separation was weak, so this is not robust optimized endurance."
- "Stress pulses hit compliance in X% of stress pulses; interpret this cautiously and do not call compliance-hitting alone optimization."

Avoid:

- "Damage is definitely reversible" (DCIV recovery does not prove microscopic reversibility).
- "Pulse protocol optimized" when median read ratio is near unity or good-cycle fraction is low.
