# Restarting an 8×8 batch/substrate grid from the currently probed device (2026-06-24)

## Context
The user provided a full probabilistic-computing substrate workflow and asked to restart the existing batch/substrate-separated 8×8 run from the currently probed device #6, overwriting older records for devices `>6`.

Existing run folder discovered in this class of run:

```text
data/probabilistic_computing/batch_1/substrate_S2/runs/grid_8x8_batch1_S2_form_randomized_5000_...
```

## Workflow requirements to encode
For batch/substrate campaigns, keep data under:

```text
data/probabilistic_computing/batch_<N>/substrate_<S>/runs/<run_name_timestamp>/
```

For this user’s 8×8 restart workflow:

- Batch: `1`
- Substrate: `S2`
- Grid: `8×8`, standard native spacing `5000, 5000`
- Safe pre-move Z retraction: `-40` stage-Z steps
- After moving to next/current device: align before approach
- Before approach: `+20` stage-Z pre-approach
- Approach: `+0.5` increments; final trim/backtracking: `0.25`
- DCIV forming: `0 → +1 → +1.5 → 0` plus adaptive reset side/recovery logic
- Pulses: randomized `SET-read-RESET-read`, SET voltages from `0.2 V` to `Vset + 0.2 V` in `0.05 V` steps, `10 ms` pulse width, continue until `≥5000` trains or permanent SET
- If stuck SET: wait `10 s`, then send 5 reset pulses
- If permanent HRS: ensure contact with a single `+0.5 Z` step before raising compliance

## Overwrite/restart safety pattern
When the user says to overwrite older records from a restart device boundary:

1. Stop/poll any active grid/resume processes first.
2. Cleanup hardware: SMU outputs off, 707B `open_all`/`nil`, lights off, verify relevant machines idle.
3. Treat file deletion/moving of existing device folders as destructive. If the tool guard requires confirmation, ask explicitly before archiving/removing active device folders.
4. Prefer archiving over deletion:
   - Move active folders for devices beyond the restart boundary (e.g. `device_07+` when restarting from device 6 and preserving device 6) into a timestamped archive directory under the same run folder.
   - Write an archive manifest JSON with `from`, `to`, device number, and UTC timestamp.
5. Prune `summary.partial.json` / `summary.json` device entries beyond the restart boundary so stale records do not appear as current results.
6. Start the patched resume runner from the current/restart device, not the next stale `DONE.json`.

## Boundary convention from this session
The user said “device currently probed is #6” and “overwrite older records for devices >6.” Interpret this as:

- preserve or rerun `device_06` according to the current physical state/restart script, but **do not archive it solely because of `>6`**
- archive/remove active `device_07` and higher records before continuing
- use current physical probe/device position for device 6 if the runner is designed to continue after a standalone manual approach

## Durable pitfall
Do not silently skip device 6 because `DONE.json` exists, and do not let stale `device_07+` folders or summary entries control resume order after the user explicitly requests overwrite from the boundary. Patch the runner to ignore stale `DONE.json` at or beyond the restart boundary and archive old records first.