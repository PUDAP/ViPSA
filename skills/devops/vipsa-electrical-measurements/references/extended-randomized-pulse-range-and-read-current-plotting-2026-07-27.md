# Extended fixed-range randomized pulses and bounded read-current plotting

Use this for current-device or grid-style randomized pulse runs where SET voltages are explicitly specified (not derived from Vset), and for follow-up plots over a bounded pulse-index range.

## Measurement pattern

- Preserve the exact user-requested SET voltage list, e.g. `0.40..0.80 V` inclusive in `0.05 V` increments.
- Make pulse-count semantics explicit:
  - A `SET -> read -> RESET -> read` train contains 4 physical pulses.
  - `10,000` physical pulses = `2,500` trains.
- Use balanced randomized blocks across voltage levels; do not let randomization starve any SET voltage.
- Save a plan CSV before execution and a results CSV with at least:
  - `pulse_index`
  - `train_index`
  - `role` (`set`, `read_after_set`, `reset`, `read_after_reset`)
  - `set_voltage_v`
  - `voltage_v`
  - `current_a`
  - `abs_current_a`
  - compliance fields/flags
- Checkpoint weak SET/RESET separation and compliance/read-current safety; label weak or unimodal thresholds as such rather than overclaiming robust switching.

## Follow-up plotting pattern

For requests like “plot read currents vs pulse number for pulse index 0 to 3000, then plot the histogram”:

1. Load the saved randomized pulse results CSV; do not rerun hardware.
2. Filter rows where:
   - `role in {'read_after_set', 'read_after_reset'}`
   - `pulse_index` is within the requested inclusive range.
3. Plot `pulse_index` vs `abs_current_a` as scatter-only points, separated by read role.
4. Use log scale for current, clipping only the plotted values to a small positive floor; preserve raw currents in the CSV subset.
5. Plot a histogram of the same read-current magnitudes with logarithmic current bins when values span orders of magnitude.
6. Run plotting headlessly with `MPLBACKEND=Agg` or `matplotlib.use('Agg')`; verify output file exists and is non-empty before reporting.
7. Report the count of read points included and split counts for after-SET/after-RESET reads.

## Concrete 2026-07-27 outcome shape

An S9 current-device extended run used SET voltages `0.40..0.80 V`, `0.05 V` step, `10,000` physical pulses / `2,500` trains. Follow-up plotting for pulse index `0..3000` included `1,500` read points (`750` after SET and `750` after RESET), and produced a combined scatter + log-binned histogram artifact from saved CSV only.
