# Post-approach default DCIV run with leave-lights context — 2026-06-15

## Trigger

Use this reference when the user simply says “run a DCIV sweep” after a successful ViPSA Keithley contact approach and does not specify new sweep parameters.

## Practical default used

After approach landed inside the `10–100 nA @ 10 mV` target window, a concise user request “run a DCIV Sweep” was treated as authorization for the established one-cycle Keithley split-compliance recipe:

- Route: 707B `connect_keithley_smu()`.
- Precheck: `hold_voltage_measure_current(0.01 V, current_compliance=1e-6 A)`.
- Path: `0 → +1 → 0 → -2 → 0 V`.
- Step: `0.05 V`, non-duplicated vertices, `121` planned points.
- Compliance:
  - PF `0 → +1`: `1e-6 A`
  - PB `+1 → 0`: `1e-6 A`
  - NF `0 → -2`: `1e-4 A`
  - NB `-2 → 0`: `1e-6 A`
- Use single-point `hold_voltage_measure_current(...)` calls in sweep order so hysteresis row order is preserved.
- Cleanup: `set_output(false)`, `open_all`, `get_closed_channels`, final machine states.

The preceding light state is orthogonal to electrical cleanup: if the user previously asked to leave lights on, do not turn them off as part of DCIV cleanup unless explicitly requested. Still report light machine execution state if checked.

## Outcome pattern from the session

This run completed all `121/121` points. A precheck at `10 mV` was conductive but not compliance-limited (`~2.84e-7 A` with `1e-6 A` read compliance), so the sweep proceeded. Postcheck was `~4.79e-7 A`.

Compliance-hit summary from the completed sweep:

- PF: `20` hits near `1 µA`.
- PB: `19` hits near `1 µA`.
- NF: `2` hits near `100 µA`.
- NB: `39` hits near `1 µA`.
- Max `|I|`: `~1.0e-4 A`.

Interpretation wording should be cautious: this is a valid completed sweep, but heavily compliance-limited on positive and negative-backward branches. Avoid calling it clean switching without further analysis/repeats.

## Plotting recovery detail

If system Python lacks `matplotlib`, do not rerun the electrical sweep. Create a temporary plotting venv and regenerate plots from the saved CSV/JSON:

```bash
python3 -m venv /tmp/vipsa_plot_venv
/tmp/vipsa_plot_venv/bin/python -m pip install --quiet matplotlib pandas seaborn
/tmp/vipsa_plot_venv/bin/python <plot_from_saved_csv.py>
```

Verify row count and artifact file sizes before reporting. Attach at least:

- segment-colored log `|I|` plot,
- measurement-order log `|I|` plot,
- raw CSV,
- summary JSON.

## Reporting standard

For user-facing summary, include:

- path/step/points collected,
- pre/post low-bias currents,
- branch compliance-hit counts,
- max `|I|`,
- cleanup verification: Keithley output off, 707B open, closed channels `nil`, final machine states idle,
- artifact attachments.
