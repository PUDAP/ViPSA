# Local NATS + ViPSA edge restart recovery for manual stage/light commands (2026-07-28)

Use this pattern when a terse manual ViPSA command such as `stage.move_z_by(15)`, `stage.move_y_by(5)`, or `turn lights red` fails because local NATS has stopped, a restarted edge is connected to the wrong NATS endpoint, or the edge replays stale START messages.

## Trigger signs

- `puda --nats-servers nats://127.0.0.1:4222 ...` fails with `nats: no servers available for connection`.
- A protocol validates but `START` times out while machine state still shows stale `idle/run_id:null`.
- After edge restart, command fails with `Send START command to start a run before sending commands`.
- Stage edge log shows a stale run such as `cannot start, <old-run-id> is currently running` after processing delayed STARTs.

## Recovery sequence

1. Check/restore local JetStream NATS:
   ```bash
   /home/amdm/.local/bin/nats-server -js -sd /home/amdm/.local/share/puda-nats -p 4222
   ```
   Run it as a tracked background process and wait for `Server is ready`.

2. Start only the affected edge(s), preserving the intended NATS routing. For local ViPSA recovery, prefer local NATS:
   ```bash
   export NATS_SERVERS=nats://127.0.0.1:4222
   cd /home/amdm/workspace/ViPSA/<machine>
   uv run main.py
   ```
   Watch for `Edge Service Ready`.

3. If the stage edge reports stale START/run activity, do not blindly repeat a motion. First clear the stale state with a harmless read-only protocol:
   ```text
   stage.get_current_position()
   ```
   This can restore `stage` to `idle/run_id:null` even when `puda machine reset stage` reports `Unknown or restricted command: reset` and transiently leaves `state:error`.

4. For stage motion plus position verification, split into two protocols when the combined `move_z_by` → `get_current_position` protocol loses run state:
   - Protocol A: one command, `stage.move_z_by(height=<signed>, feedrate=450)`.
   - Protocol B: one command, `stage.get_current_position()`.
   Require Protocol A success before claiming motion; require Protocol B success before claiming numeric readback.

5. For light color commands, after NATS/edge recovery run a one-command protocol such as:
   ```text
   light.set_red()
   ```
   Then verify `puda machine state light` is `idle/run_id:null`. `idle` is execution state, not a visual color sensor.

## Reporting standard

- If an earlier attempt timed out at START, explicitly say it did not confirm motion.
- If a retry returns success but readback fails, report command success separately from numeric readback.
- If the edge restart resets tracked coordinates, state that the coordinate is tracked/software readback only and may have reset to zero; do not infer physical position from old and new tracked coordinates across restarts.
- Keep reports concise: command run, success/failure, readback if verified, final state.
