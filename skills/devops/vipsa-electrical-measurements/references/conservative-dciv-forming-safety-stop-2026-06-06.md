# Conservative DCIV forming safety stop — 2026-06-06

## Context

After a visual/electrical approach, the user requested a conservative DCIV sweep to form the device properly without overstressing or permanently setting it.

A conservative one-cycle split-compliance plan was used:

- Intended path: `0 -> +0.60 -> 0 -> -1.20 -> 0 V`
- Step: `0.05 V`
- Positive/form branch compliance: `100 nA`
- Negative/reset branch planned compliance: `500 nA`
- Safety guard: stop if the device looks short-like or compliance-limited at very low command voltage.

## Observed safety outcome

Only the positive-forward branch was run. It hit the `100 nA` compliance from `+0.05 V` onward while measured voltage collapsed near zero:

- At `+0.05 V` command: `I ~= 9.999859e-8 A`, `Vmeas ~= 0.0001688 V`
- At `+0.10 V` command: `I ~= 9.999786e-8 A`, `Vmeas ~= 0.0002386 V`
- Compliance-hit points: 12/13 on the PF branch

The run was stopped before PB/NF/NB because continuing into reset/form branches would add stress without clear benefit. The correct report language is: very conductive / short-like / possibly over-contacted; do not call it successful forming.

## Reusable workflow lesson

For conservative post-approach DCIV forming:

1. Preflight: verify Keithley 2450 and 707B are idle; force Keithley output off before routing.
2. Route DUT to Keithley via 707B break-before-make helper.
3. Start with a low positive branch (`<= +0.6 V`) and low SET/form compliance (`~100 nA`) before attempting a negative/reset branch.
4. After each branch, inspect for compliance at very low voltage and measured-voltage collapse.
5. If current is already compliance-limited near `+0.05` to `+0.10 V`, stop immediately, clean up, and report safety stop; do not continue the rest of the sweep merely because the planned full path had more branches.
6. Cleanup must include Keithley output off, 707B `open_all`, `get_closed_channels`, and final machine states.

## PUDA data-recovery implementation note

When an outer Python script reads `puda.db` `command_log` rows for a run, `start` and `complete` entries may appear alongside the actual command. Do not assume `responses[-1]` is the measurement command; filter by `command_name == 'source_voltage_measure_current'` or by the presence of `response.data.result`. If a script fails after the instrument command completed but before plotting/analysis, do not rerun the sweep; recover rows from `puda.db`, generate CSV/plot, and report cleanup state.
