# Local ViPSA edge restart and stale-run recovery (2026-07-27)

Context: local ViPSA was using a local JetStream NATS at `nats://127.0.0.1:4222` with edge services under `/home/amdm/workspace/ViPSA/<machine>/uv run main.py`. Simple light/stage/electrical protocols initially failed because edge processes were stale, duplicated, or only processed delayed STARTs after restart.

Reusable recovery pattern:

1. Prefer protocol-first execution. If a protocol times out at START, do not assume the command ran.
2. Inspect the affected edge process set and check for duplicate subscribers for the same machine, especially after a manual `start_all_edges.sh` launch:
   - `ps -ef | grep '/home/amdm/workspace/ViPSA/.venv/bin/python3 main.py'`
   - map each PID with `readlink /proc/$pid/cwd`.
3. If duplicate edge subscribers exist for one machine, stop only the duplicate/stale process group, preserving other machine edges.
4. For a requested stage “clear holds and restart,” first run a normal `start -> abort_motion -> complete` lifecycle while the old edge is still responsive, then verify `idle` / `run_id:null`. Stop only that stage edge process group, verify the serial device is released, and restart from the stage directory as a tracked background process. After startup, verify exactly one process holds the stage serial device; this prevents duplicate subscribers or serial owners from making motion/readback evidence misleading.
5. Restart only the affected edge from its machine directory, e.g. `cd /home/amdm/workspace/ViPSA/stage && uv run main.py`, as a tracked background process.
6. Watch for `Edge Service Ready`. The restarted edge may immediately process a previously timed-out START and leave the machine `active` with that old run id.
7. Complete the exact stale `run_id` before retrying. A direct core-NATS complete transaction is acceptable as recovery/cleanup:
   - subscribe to `puda.<machine>.cmd.response.immediate` and `.queue`
   - publish `complete` to `puda.<machine>.cmd.immediate` with the stale `run_id`
   - wait for a `complete` response with `status: success`.
8. Verify the configured live NATS backend reports `idle` and `run_id: null`; do not silently fall back to a local NATS server when the deployment uses a shared cluster.
9. Retry the original protocol only after the stale run is cleared.

Specific observed cases:

- `light.turn_on`: duplicate light edge from `start_all_edges.sh` caused queued command failure (`Send START command to start a run before sending commands`). Stopping the duplicate set, restarting `light`, completing the stale run, then running a fresh `start -> turn_on -> complete` worked and left `light` idle/null.
- `stage.move_z_by(+10)`: original protocol timed out at START. Restarting `stage` made the edge accept the stale START, so the stale run had to be completed directly. A read-only position check showed no motion (`z=0`), then a fresh `move_z_by(height=10, feedrate=450)` succeeded and read back `z=10`.
- Stage-position origin after restart: the OpenFlexure edge may reinitialize its tracked position to `[0,0,0]`. A later `+50` command followed by `z=50` verifies the fresh edge-relative command/readback chain, but it does **not** recover the pre-restart absolute physical Z and must not be combined with an older tracked value. Report the origin reset explicitly and avoid claiming independent physical-position proof unless camera, controller coordinates, encoder data, or another independent observation corroborates it.
- `keithley-707b`: a quick resistance check timed out at 707B START, then after restart 707B reported `RUN_ID_MISMATCH` with the earlier measurement run id. Completing that exact stale id restored `idle/run_id:null`; the quick resistance check then succeeded with Keithley output-off and 707B `nil` cleanup.

Reporting standard:

- Separate blocked/cleared attempts from successful retries.
- Do not report motion or electrical measurement until the successful retry and readback/cleanup are verified.
- Include final states for affected machines (`idle`, `run_id:null`).
