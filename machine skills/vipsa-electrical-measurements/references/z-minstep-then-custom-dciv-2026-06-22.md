# Z minimum-step contact improvement then custom split-compliance DCIV (2026-06-22)

Use this note when the user explicitly asks to improve contact with the minimum valid Stage Z increment and then run a custom DCIV path.

## Trigger

User request shape:

- "Move the z stage up 0.25 steps to ensure contact"
- Then run a DCIV sweep such as `0 -> +1 -> 0 -> -1.5 -> 0`
- Explicit branch compliances, e.g. positive/SET compliance `1e-6 A`, reset/negative compliance `1e-5 A`

## Workflow

1. Treat `+0.25` as a valid minimum forward-Z contact-improvement step in the user's current ViPSA convention.
2. Use PUDA protocol-first orchestration when possible:
   - `stage.get_current_position`
   - `stage.move_z_by(height=+0.25, feedrate=450)`
   - `stage.get_current_position`
   - `keithley-2450.set_output(false)`
   - `keithley-707b.connect_keithley_smu()`
   - low-bias pre-read probes (`0 V`, `+10 mV`, `-10 mV`) at a low/read compliance
   - DCIV sweep points in the exact requested order
   - low-bias post-read probes
   - `keithley-2450.set_output(false)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()`
3. For the requested path `0 -> +1 -> 0 -> -1.5 -> 0`, a 0.05 V pitch gives 101 non-duplicated sweep points:
   - PF: `0, +0.05, ..., +1.0`
   - PB: `+0.95, ..., 0`
   - NF: `-0.05, ..., -1.5`
   - NB: `-1.45, ..., 0`
4. Map compliances by segment unless the user says otherwise:
   - PF/PB: positive/SET compliance
   - NF/NB: reset/negative compliance
5. Save CSV, JSON summary, and a log-scale `|I|` plot preserving row order. If the live run succeeds but the system Python lacks plotting libraries, do not rerun hardware; create/use a temporary plotting venv and regenerate the plot from the saved CSV/JSON.
6. Verify final state and cleanup before reporting:
   - Keithley output off
   - 707B open/nil closed channels
   - `stage`, `keithley-2450`, `keithley-707b`, and `light` idle with `run_id: null`

## Reporting pattern

Keep the user-facing report concise:

- Z movement and before/after Z readback
- DCIV path and compliances
- number of sweep points
- pre/post `+10 mV` read currents and ratio if available
- max sweep current
- branch compliance-hit counts
- largest SET-like jump or RESET-like drop if obvious
- cleanup/final idle state
- attach plot and CSV with `MEDIA:`

## Pitfall

Do not let a post-processing/plotting failure imply the electrical run failed. The hardware run and cleanup are primary; plot regeneration is safe from saved data and should be done without repeating the DCIV.