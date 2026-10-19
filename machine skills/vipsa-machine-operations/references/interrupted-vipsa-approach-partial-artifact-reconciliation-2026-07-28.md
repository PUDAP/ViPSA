# Interrupted vipsa_approach partial-artifact reconciliation (2026-07-28)

Use when a standalone `tools/vipsa_approach.py --execute` run is killed or interrupted before it writes `approach_summary.json` / `approach_log.csv`.

## Lesson

Do **not** infer “no Z motion occurred” from missing summary/log files. The approach script writes per-command protocol artifacts as it goes, and can have already executed Stage-Z moves before interruption. A missing `approach_summary.json` only means the wrapper did not reach its normal `finally`/summary path.

## Required reconciliation steps

1. Kill the tracked process if still running.
2. Inspect the active approach output directory, especially:
   - `approach_start_stage_position_run.txt`
   - `approach_coarse_z_move_*_run.txt`
   - `approach_read_coarse_*_run.txt`
   - any `*_validate.txt` with no matching `*_run.txt` to identify the step being prepared when stopped.
3. Sum only successful `stage.move_z_by` responses from `approach_coarse_z_move_*_run.txt` / trim/fine move files; do not count validate-only files as executed motion.
4. Run explicit cleanup:
   - `keithley-2450.set_output(false)` and `abort_measurement()`
   - `keithley-707b.open_all()` and `get_closed_channels()`
   - `light.turn_off()` if the run policy requested lights off
   - clear any stale `stage` active run ID with `puda machine complete stage --run-id <old>` if `puda machine state stage` reports `active`
   - `stage.abort_motion()` and fresh `stage.get_current_position()`
5. Verify final states for the six ViPSA machines.
6. Report separately:
   - whether the first failed attempt had no motion
   - partial Stage-Z motion that did occur in a retry
   - final readback and whether it matches summed successful moves
   - cleanup/stale-run clearing status

## Concrete example

An interrupted retry produced:

- `approach_start_stage_position_run.txt`: stage `[0, 0, 0]`
- `approach_coarse_z_move_001_run.txt`: successful `move_z_by(height=+0.5)`
- `approach_coarse_z_move_002_run.txt`: successful `move_z_by(height=+0.5)`
- `approach_coarse_z_move_003_run.txt`: successful `move_z_by(height=+0.5)`
- `approach_coarse_z_move_004_validate.txt` existed but no `_run.txt`, meaning step 004 was only prepared/validated when the user said `stop`
- fresh readback after cleanup: `[0, 0, 1.5]`

Correct report: “first attempt did not move; retry moved Z up by +1.5 steps before stop.”

Incorrect report: “no completed summary/log exists, so no approach result / no motion.”

## Script robustness note

If `vipsa_approach.py` stores `argparse` values with `type=pathlib.Path` in JSON, convert `Path` values to strings before writing `plan.json`:

```python
"params": {k: str(v) if isinstance(v, pathlib.Path) else v for k, v in vars(args).items()}
```

This avoids failing before physical execution when `--outdir` is supplied as a path.
