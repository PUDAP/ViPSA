# Fresh substrate 8x8 grid from current contacted device + DCIV low-current retry

Use this pattern when the user says a new substrate/grid should start from the **current device** after a verified standalone approach, and asks to keep the previous grid protocol with explicit DCIV changes.

## Reusable workflow

1. Load the prior grid runner/summary as the baseline, but create a **new substrate/run folder** instead of resuming or appending to the old substrate folder.
2. Adjust grid dimensions explicitly for the new request (for example `7x7` means rows/cols metadata, grid-generation loops, device numbering, traversal loops, and output folder/script names all change together). Do not leave stale `8x8` ranges or device-number formulas in a copied runner.
3. Set the current Zaber position as device 1 / origin for the new grid and generate a fresh `grid_row_major.json` + `grid_positions.csv` in the new folder.
4. If a standalone approach was just completed, or the user explicitly says the current device is already contacted, treat device 1 as a **current-device handoff**:
   - do not retract, move Z/stage, re-align, or mechanically approach before device-1 DCIV/pulse;
   - if a recent approach artifact exists and is known to be the handoff, reuse its `summary.json` for device 1;
   - otherwise run only a live low-bias electrical handoff read and record it in `device_01/approach.json`/`summary.json` with `no_mechanical_approach: true`;
   - still run electrical cleanup before DCIV.
5. For subsequent devices, keep the normal inter-device safe retract, Zaber X/Y move, pre-approach Z, alignment, approach, DCIV, pulse, cleanup sequence.
6. Before launching, verify no conflicting grid/approach process is active and all six ViPSA machines are idle/null-run when possible. If a machine reports a stale active `run_id` but direct COMPLETE says “not active,” record it as stale state and proceed only if command-level cleanup/output-off/open-all succeeds.
7. Start the long grid runner as a tracked background process with completion notification, then set up a lightweight monitor/reporter for that specific new run folder to report completed devices instead of spamming approach-loop details.

## Current-device handoff pitfalls

- “Already contacted” is an instruction not to repeat mechanical approach, not a guarantee that the live low-bias handoff read will be good. Record the read honestly (including open-like pA/sub-nA results) and follow the active grid policy for whether to continue measurements.
- For a fresh grid, remove/rescope old resume behavior: no previous `summary.partial.json` preservation, no old `DONE.json` skip behavior, and no old `START_AT_DEVICE` boundary unless the user explicitly asks to resume.
- A separate folder is part of the measurement artifact contract. Verify the new `OUT` path is distinct from the previous run before launch and mention it in the user-facing start report.

## DCIV changes from this session

When the user requests reset-side sweeps that never run positive voltages and strict SET-side direction:

- SET side:
  - `PF`: `0 -> +1.0 V`
  - `PB`: `+1.0 -> 0 V`
- Reset side:
  - normalize adaptive reset voltage so it remains strictly negative;
  - `NF` starts at `-0.05 V` and goes to the negative reset voltage;
  - `NB` returns from the negative reset voltage toward `0 V` without positive points;
  - recovery/pre-reset sweeps must also be non-positive.

For very-low-current DCIV (`max |I| < 5e-9 A`):

1. classify/log `possible permanent HRS / poor contact`;
2. move stage Z `+0.5` once;
3. retry the same DCIV path with the same compliance, labeling rows distinctly (e.g. `DCIV_CONTACT_RETRY_*`);
4. if still below `5e-9 A`, retry again with high compliance and labels beginning `DCIV_RETRY_*`:
   - positive side (`PF`, `PB`): `1e-5 A`
   - negative side (`NF`, `NB`): `1e-4 A`.

## Pitfalls

- Do not let old resume logic silently skip or archive device ranges for a new substrate/run. Remove previous-summary loading and `DONE.json` skip behavior unless the user explicitly asks for a resume.
- Update all substrate/run metadata (`SUMMARY`, output path, params, run folder names) together; stale `S2`/`S3`, `8x8`, or old START_AT labels in a fresh run are misleading.
- When cloning an old grid runner to a different grid size, verify both generation and traversal code: row/col loop bounds, `device_number = row*cols + col + 1`, summary params, filename/folder labels, and any monitor script paths.
- If device 1 is a current-contact handoff, the first log line should explicitly confirm no initial movement/alignment/approach before stress (for example `CURRENT_DEVICE_START ... no initial movement/alignment/approach`). Inspect early logs and `device_01/summary.json` before claiming launch success.
- Verify the generated runner with `python3 -m py_compile` and inspect the DCIV path code before execution.
- If using a direct-NATS/per-command runner due to PUDA protocol issues, still report that it is an execution fallback and preserve the protocol-first cleanup/safety sequence.
