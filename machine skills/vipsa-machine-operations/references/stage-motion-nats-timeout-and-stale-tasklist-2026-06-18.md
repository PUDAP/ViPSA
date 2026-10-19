# Stage motion NATS timeout + stale task-list verification (2026-06-18)

## Trigger

Use this note when a user asks for a simple stage Z move after a long ViPSA/grid session, or asks why a run took so long / what failed while the visible task list still says a grid run is in progress.

## Lessons

### 1. Stale task lists after context compaction

A preserved task list can be stale. Before telling the user a grid run is still active:

1. Check tracked/background processes.
2. Inspect the latest run folder summary (`summary.json`) and final-state files.
3. Report the verified state: completed devices, skipped devices, cleanup state, and whether any process is still running.

For grid runs, useful concise fields are:

- `started_utc` / `finished_utc`
- number of devices in `devices`
- per-device `approach.status`, `dciv.status`, `pulse.status`, and final status
- final cleanup files / final state tails

Do not let an old in-progress task list override verified artifacts.

### 2. Stage Z move timeout pattern

For requests like “move the stage down by 35 steps,” protocol-first is still the default:

1. Generate a metadata-complete PUDA protocol with:
   - `stage.move_z_by(height=-35, feedrate=450)` for Down
   - `stage.get_current_position()` for verification
2. Run from `/home/vipsa/vipsa-puda-project` so PUDA can find `puda.config`.
3. Validate the protocol before running it.
4. If `puda protocol run` fails during NATS connection/setup, do **not** claim motion occurred.
5. Retry once with a single known ViPSA NATS server override if appropriate.
6. Probe TCP ports only as diagnosis. `</dev/tcp/host/port` showing `open` does not prove PUDA/NATS session setup succeeded and does not prove hardware motion.
7. For physical motion, report success only when command response and position/state verification complete.

### 3. Direct NATS fallback boundary

Direct/raw NATS fallback may be technically available, but for physical motion it should not be used silently. If protocol control cannot execute the motion, report:

- validated protocol status
- exact NATS timeout/connection blocker
- “no confirmed stage motion”
- offer direct NATS fallback only with explicit user authorization

This preserves the user's protocol-first preference and avoids unverified hardware movement claims.
