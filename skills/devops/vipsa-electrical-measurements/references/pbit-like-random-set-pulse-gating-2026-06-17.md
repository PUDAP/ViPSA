# p-bit-like random SET-voltage pulse workflow: precheck, gating, and artifacts

Use this reference when the user asks for p-bit-like switching probability tests on a ViPSA memristive device.

## Durable workflow lesson

1. **Use previous context, then verify live state.** A previous health check can say the device was short-like/over-contacted, but the current contacted state can change. Repeat a low-bias Keithley probe before any reset or pulse stress.
2. **Low-bias live classification gates the branch:**
   - If low-bias reads are short-like / compliance-limited, run a reset-only side of DCIV first, then re-check read state.
   - If low-bias reads are already HRS-like and safely non-shorted, skip reset-only DCIV and proceed only if the contact is strong enough for meaningful pulsed reads.
   - If low-bias reads are pA/sub-nA and voltage response is weak/open-like, **do not run the p-bit pulse train**; report open/very weak contact rather than generating meaningless switching probabilities.
3. **Generate the randomized pulse CSV before running hardware.** For the requested p-bit recipe, the CSV rows should explicitly encode every pulse in the sequence: `set`, `read_after_set`, `reset`, `read_after_reset`, with `trial_order`, `trial_index`, `repeat_index_for_voltage`, `set_voltage_v`, `voltage_v`, `pulse_width_s`, and compliance.
4. **Requested recipe captured:** SET voltages `0.20–0.90 V` in `0.05 V` increments, `25` repeats per SET voltage, randomized trial order, read at `+0.1 V`. Reset pulse, pulse width, and compliance may be inherited from the most recent validated pulse context if the user did not restate them; in the 2026-06-17 run this meant RESET `-1.5 V`, pulse width `10 ms`, compliance `10 µA`.
5. **Run only after live protocol readiness.** Validate the generated protocol, then run via PUDA/Keysight. If PUDA/NATS/Keysight START blocks before the pulse command executes, stop and report that no read distribution or switching probability can be plotted; do not synthesize results.
6. **Plotting after successful pulse run:**
   - Preserve raw signed current in the result CSV.
   - Use `abs(I)` only for read-current histogram/log-scale thresholding.
   - Plot histogram of `read_after_set` and `read_after_reset` currents.
   - Estimate threshold from the actual read-current distribution, e.g. Otsu threshold in log10(|I|), or report that no reliable bimodal threshold exists.
   - Plot `P(switch) = fraction(read_after_set > threshold)` versus SET voltage with binomial error bars.
   - Also report/reset-state leakage: fraction of `read_after_reset` values above the same threshold.

## Safety/reporting notes

- Do not run p-bit pulses on an open-like/very weak-current device just because it is technically non-shorted; the result would be dominated by contact/noise floor.
- A previous short-like state plus a current pA state should be reported as a changed live state, not as a contradiction.
- If pulsing is skipped, still provide the generated CSV/protocol artifacts if they were created, and clearly state which steps were not run and why.
