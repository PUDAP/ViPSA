# Extended fixed-range randomized pulses and read-current window histogram (2026-07-27)

## Trigger
Use when the user asks for an extended randomized pulse test over an explicit SET-voltage range, or asks to plot read currents for a bounded pulse-index window plus a histogram of those current values.

## Measurement pattern
- Preserve the explicit SET-voltage range exactly and inclusively. In this session: `0.40 V` through `0.80 V` in `0.05 V` steps.
- Use balanced randomized `SET -> read -> RESET -> read` trains when no different sequence is requested.
- In this session the protocol used:
  - SET voltages: `[0.40, 0.45, ..., 0.80] V`
  - read voltage: `+0.1 V`
  - RESET voltage: `-2.0 V`
  - pulse width: `2 ms`
  - compliance: `100 µA`
  - 10,000 physical pulses = 2,500 complete trains
  - 100 physical pulses / 25 trains per checkpoint
- For an explicitly requested extended run, do not stop solely because RESET separation remains weak, unless the user asked for a reset-success-gated run. Keep hard safety stops such as low-voltage read current approaching compliance.
- Record direction sanity separately from P(switch): if read-after-SET and read-after-RESET medians differ only weakly, report probabilistic/partial switching rather than robust SET/RESET separation.

## Analysis/reporting pattern
- Save raw pulse rows, the generated pulse plan, per-voltage probability table, checkpoints, and summary JSON.
- Compute per-voltage attempts, switches, `P_switch`, reset-high count/fraction, and checkpoint medians.
- In the concise user report include:
  - SET range/step and physical pulse/train count
  - median read-after-SET and read-after-RESET
  - median SET/RESET ratio
  - max read current and whether a safety stop triggered
  - a per-voltage probability table
  - cleanup verification (`set_output(false)`, `open_all`, `get_closed_channels == nil`, light state)

## Read-current window + histogram plot
When the user asks for read current vs pulse number for a pulse-index window and a histogram:
1. Filter the pulse CSV to `role in {read_after_set, read_after_reset}` and `pulse_index` within the requested inclusive range.
2. Save the filtered CSV as a named artifact, e.g. `read_currents_pulse_0_3000.csv`.
3. Generate a two-panel plot:
   - left: scatter of `abs_current_a` vs `pulse_index`, log-y, colored by read role;
   - right: histogram of `abs_current_a` using log-spaced bins, overlaid by read role.
4. Report counts and medians for the filtered window.
5. In headless/Linux desktop sessions set `MPLBACKEND=Agg` for matplotlib plot scripts to avoid GUI/Tk display authorization failures.

## Example artifact names
- `extended_randomized_pulse_results.csv`
- `extended_randomized_pulse_plan.csv`
- `extended_switching_probability.csv`
- `extended_device_plot.png`
- `read_currents_pulse_0_3000.csv`
- `read_currents_pulse_0_3000_and_histogram.png`
