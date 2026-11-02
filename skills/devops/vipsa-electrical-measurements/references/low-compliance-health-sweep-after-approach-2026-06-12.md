# Low-compliance DCIV health sweep after approach — 2026-06-12

## Trigger

Use this when the user asks for a conservative / low-compliance DCIV sweep to check device health after contact approach.

## Safe health-check recipe

A bounded health-check sweep can be:

```text
planned path: 0 → +0.6 → 0 → -1.2 → 0 V
step: 0.05 V
positive/form compliance: 100 nA
negative/reset compliance: 500 nA
read compliance: 1 µA
```

Run the positive-forward branch first and inspect before continuing. If low-voltage PF points are already compliance-limited, stop before PB/NF/NB.

## Safety stop condition

Stop the sweep and cleanup if any nonzero low-voltage PF point near `+0.05` to `+0.10 V` hits the low positive compliance. This indicates the device/contact is already very conductive or over-contacted, and the negative/reset side would add stress without a clear health-check benefit.

Report language:

- `very conductive / short-like / over-contacted`
- `apparent resistance is a bound, not a precise resistance`
- e.g. a `10 mV` read at `1 µA` compliance means `R ≤ ~10 kΩ`, not exactly 10 kΩ.

## Concrete observed outcome

In this session, after Keithley-guided approach landed at `~63.6 nA` at `10 mV`, a subsequent health check found:

- Pre-read at `10 mV`: `~1.00 µA`, compliance-limited.
- PF branch `0 → +0.6 V` at `100 nA` compliance collected 13 points.
- PF compliance hits: `12 / 13`.
- Compliance began at `+0.05 V`.
- The planned PB/NF/NB branches were skipped.
- Post-read at `10 mV`: `~1.00 µA`, compliance-limited.

Interpretation: not a healthy low-compliance sweep; do not proceed to forming or pulsing unless the user explicitly requests a reset/retraction strategy.

## Data recovery / post-processing pitfall

If the electrical sweep and cleanup completed but post-processing fails (for example CSV `DictWriter` complains about extra metadata fields such as `reset` or `settle_s`, or system Python lacks `matplotlib`), do **not** rerun the sweep. Recover rows from the saved PUDA protocol JSON/output files or command logs, then regenerate CSV/plots from saved responses.

For CSV recovery, either include all metadata keys in the field list or use `extrasaction='ignore'`. If multiple protocol chunks are used, preserve execution order explicitly, e.g. pre/PF chunk before post-read/cleanup chunk; alphabetical filename order can swap pre/post labels.

## Required cleanup report

Always verify and report:

- Keithley output off.
- 707B `open_all` succeeded.
- `get_closed_channels` returns `nil`.
- Final machine states are `idle`, `run_id: null`.
