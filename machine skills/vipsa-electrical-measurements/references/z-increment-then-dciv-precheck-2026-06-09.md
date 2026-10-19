# Z increment followed by DCIV with low-bias precheck — 2026-06-09

## Trigger

Use this pattern when the user asks for a small Z move immediately followed by a DCIV, e.g. “move z up by 1 step and then run a DCIV,” especially after previous low-bias checks looked open/high-resistance.

## Operational sequence

1. Treat the requested Z movement as an explicit physical side effect and execute it directly using the current ViPSA convention: `up` = `+Z`, so `stage.move_z_by(height=<positive step>, feedrate=450)`.
2. Read stage position before and after if available; report concise Z before/after.
3. Before DCIV, route DUT to Keithley and run a non-stressing low-bias precheck:
   - `keithley-2450.set_output(enabled=false)`
   - `keithley-707b.connect_keithley_smu()`
   - `hold_voltage_measure_current(voltage=0.01, current_compliance=1e-6, settle_s=0.2, read_count=3, reset=True)`
4. If the 10 mV median current is near compliance or otherwise short-like (e.g. `abs(I_med) >= 9e-7 A` with `1e-6 A` compliance), abort the DCIV, cleanup, and report the safety stop.
5. If the precheck is still pA/sub-nA and not short-like, proceed with the established conservative one-cycle split DCIV unless the user gave different parameters:
   - Path: `0 → +1 → 0 → -2 → 0 V`
   - Step: `0.05 V`, non-duplicated vertices (`121` points)
   - PF/PB compliance: `1e-6 A`
   - NF compliance: `1e-4 A`
   - NB compliance: `1e-6 A`
   - `delay_s=0.001`
6. Save JSON and CSV raw artifacts, regenerate a legible log-scale `|I|` plot from the saved CSV if plotting fails during the measurement script, and do **not** rerun the electrical sweep just for plotting.
7. Always cleanup:
   - `keithley-2450.set_output(enabled=false)`
   - `keithley-707b.open_all()`
   - verify `get_closed_channels() == nil`
   - verify stage/Keithley/707B idle states where possible.

## Example outcome and interpretation language

After Z `+1.0` from an open-like contact state, the precheck remained open-like at `~5.6e-11 A` at `10 mV`, so DCIV proceeded. The DCIV collected all `121` points. The positive forward branch hit `1 µA` compliance starting around `+0.60 V`; positive backward remained mostly compliance-limited; the negative branch did not hit compliance and stayed in the `~1e-8 A` range.

Concise wording:

- “Precheck was not short-like, so DCIV proceeded.”
- “PF hit compliance around +0.60 V; PB stayed mostly compliance-limited.”
- “Negative branch did not reset to a strong low-resistance/compliance-limited state.”
- “Cleanup verified: output off, 707B nil, machines idle.”

## Pitfalls

- Do not skip the 10 mV precheck after a Z increment. A tiny Z change can turn an open contact into an over-contact/short-like condition.
- Do not report a DCIV as complete if only the Z move or precheck ran; require point count and saved artifacts.
- Do not use system-Python plotting failure as a reason to rerun a sweep. Plot from the saved CSV/JSON using a plotting-capable environment.
