# Verbose step-size approach, stop cleanup, and stage-edge reconciliation (2026-07-28)

Use this reference for terse user requests such as **"approach with step size 1; give verbose updates for every step"**, follow-up **"update"**, or **"stop approach"** during a standalone Keithley-guided ViPSA approach.

## Trigger

- User explicitly requests a bounded electrical approach with custom coarse step size, e.g. `step size 1`.
- User explicitly requests verbose per-step updates rather than the usual non-spam approach summaries.
- A running approach is killed/stopped and the final status must be reconciled from artifacts and stage edge logs.

## Workflow

1. Preserve the established standalone approach defaults unless overridden:
   - read voltage `0.01 V`
   - target current window `10–100 nA`
   - read compliance `1e-6 A`
   - lights off before/final
   - Stage-Z only, with user convention `+Z` = approach/up/forward
   - hardware minimum Z step `0.25`
2. Apply only the requested override, e.g. `--step 1` for coarse approach.
3. For verbose per-step reporting, prefer a runner that prints structured, flushed updates after every read/move, for example:
   ```json
   {"STEP_UPDATE":"read","phase":"coarse","attempt":37,"net_z_steps":37.0,"current_a":3.66e-11,"abs_current_a":3.66e-11}
   {"STEP_UPDATE":"move_z","phase":"coarse","height":1.0,"net_z_steps":38.0}
   ```
   If using `terminal(background=true)`, do **not** rely solely on `watch_patterns` for every-step messages: Hermes rate-limits watch-pattern notifications and disables them after repeated 15 s-window hits. Tell the user that manual `update` polling is available, then use `process poll` / process logs to report current attempt, net Z, current, and whether it is still below/in/above the target window.
4. If a serialization bug appears when writing `plan.json` from an argparse namespace containing `pathlib.Path`, patch the runner to convert Path values before `json.dumps`, e.g. `{k: str(v) if isinstance(v, pathlib.Path) else v for k, v in vars(args).items()}`. Also use the same JSON-safe args dictionary in any persisted summary.
5. On `stop approach`:
   - kill the tracked process immediately;
   - inspect the process log and run directory artifacts (`approach_log.csv`, `approach_summary.json`, per-command `*_run.txt`) before summarizing;
   - if summary/log CSV were not written because the process was killed mid-command, use process output and per-command artifacts to find the last completed read/move;
   - force Keithley output off + abort, 707B `open_all` + `get_closed_channels`, lights off, stage abort/readback;
   - verify final states for the six ViPSA machines when possible.
6. A killed approach can leave the stage state as `idle` with a non-null stale `run_id`, or can leave a run that was STARTed but had no queued `move_z_by` yet. If `stage` blocks fresh commands with `RUN_ID_MISMATCH`, complete the exact stale run id when active, then run `stage.abort_motion()` and `stage.get_current_position()` under a fresh run.
7. Use `/home/amdm/workspace/ViPSA/logs/edges/stage.log` to reconcile what physically/driver-wise happened when artifacts are ambiguous:
   - `Queue command received ... command_name=move_z_by, params={'height': ...}` plus `driver - INFO - Moved Z-axis by ... steps` means the driver executed the move.
   - A `Started run ...` with no subsequent queued `move_z_by` before stop means the next stage run was only STARTed, not moved.
   - `abort_motion` may log status history such as `MPos ... 0.500`, `1.000`, `1.500`; report this as edge/readback evidence, not independent visual confirmation.

## Reporting pattern

For each verbose `update`:

```text
👇 Still running.
- Attempt: <N>
- Net Z this run: +<steps>
- Current at 10 mV: <A> = <pA/nA>
- Target: 10–100 nA
- Status: still below / in-window / over-current; continuing or trimming
```

On stop, explicitly distinguish:

- last completed read attempt and current;
- last confirmed cumulative net Z from this run;
- whether a final summary/log exists;
- cleanup verification;
- final stage readback.

Do not say "no Z move happened" from lack of `approach_summary.json` alone. Check per-command artifacts and the stage edge log first.
