# Stage software readback vs physical motion, and edge reconnect pattern (2026-07-28)

## Trigger

Use this when ViPSA Stage-Z commands return successful PUDA responses and `get_current_position()` changes, but the user reports the physical stage did not move, or when approach/contact attempts fail despite large reported Stage-Z travel.

## Core finding

The current OpenFlexure stage edge can report successful motion without proving physical motor movement.

Observed driver behavior in `/home/amdm/workspace/ViPSA/stage/driver.py`:

- `get_current_position()` returns internal variables `self.x_pos`, `self.y_pos`, `self.z_pos`; it does **not** query GRBL/hardware position.
- `move_z_by()` writes `G91\nG1 Z{distance} F{feedrate}\nG90\n`, sleeps, calls `_is_busy()`, then increments `self.z_pos += height` and logs `Moved Z-axis...`.
- `_is_busy()` writes `?` but reads only one line; it may read stale `ok` instead of a real `<Idle...>`/`<Run...>` status line.
- Methods mostly log exceptions and return `None`, so PUDA may mark a command successful even when the physical motion path failed.
- `abort_motion()` sends `!`, then `?`, then `G90 G1 Z0 F100` while logging `Hold cleared without resuming previous motion`; this is not a pure hold-clear and can command a Z move to zero.

Therefore:

- `stage.move_z_by` success = command path accepted, not verified physical movement.
- `stage.get_current_position` / `[x,y,z]` = software-tracked readback, not physical proof.
- Edge logs `Moved Z-axis by ...` are also not sufficient proof of physical movement.

## Operational rule

If the user says the stage is not moving or visual evidence contradicts readback:

1. Stop further approach/motion loops immediately.
2. Do not cite tracked Z readback as physical confirmation.
3. Treat any approach result that depended on those moves as unverified/failed due to no confirmed physical Z motion.
4. Audit the stage edge and serial path before more motion.
5. Require visual confirmation or a fixed driver that queries/parses real GRBL state before resuming automatic approach.

## Read-only audit checklist

```bash
# live state
puda machine state stage

# stage edge config and serial target
grep -E '^STAGE_PORT=' /home/amdm/workspace/ViPSA/stage/.env
readlink -f /dev/openflexture
udevadm info -q property -n /dev/openflexture | grep -E 'DEVNAME|DEVLINKS|ID_SERIAL|ID_MODEL|ID_VENDOR'

# stage process and serial fd owner
for pid in $(pgrep -f '/home/amdm/workspace/ViPSA/.venv/bin/python3 main.py|uv run main.py'); do
  cwd=$(readlink /proc/$pid/cwd 2>/dev/null || true)
  if [ "$cwd" = "/home/amdm/workspace/ViPSA/stage" ]; then
    echo "stage_pid=$pid cmd=$(tr '\0' ' ' < /proc/$pid/cmdline)"
    ls -l /proc/$pid/fd | grep -E '/dev/openflexture|/dev/ttyACM|/dev/ttyUSB' || true
  fi
done

# stage logs
python3 - <<'PY'
from pathlib import Path
text = Path('/home/amdm/workspace/ViPSA/logs/edges/stage.log').read_text(errors='replace')
for pat in ['ERROR','WARNING','Failed','RUN_ID_MISMATCH','Moved Z-axis','Current position set as zero','Motion was aborted','Connected to Arduino']:
    print(pat, text.count(pat))
PY
```

Expected current wiring observed here:

- Stage config: `STAGE_PORT=/dev/openflexture`
- `/dev/openflexture -> /dev/ttyACM0`
- Udev serial: `usb-Arduino__www.arduino.cc__0043_7543330363135130B012-if00`
- Light was on `/dev/ttyACM1`; Zaber was `/dev/ttyUSB0`.

## Disconnect/reconnect stage edge only

Use this when asked to reconnect the stage, or after confirming the edge may be stale. This restarts only the stage edge and does not send motion.

```bash
# Stop only processes whose cwd is the stage edge dir
for pid in $(pgrep -f '/home/amdm/workspace/ViPSA/.venv/bin/python3 main.py|uv run main.py' || true); do
  cwd=$(readlink /proc/$pid/cwd 2>/dev/null || true)
  [ "$cwd" = "/home/amdm/workspace/ViPSA/stage" ] && echo "$pid"
done | sort -nr | xargs -r kill
sleep 3

# Force-kill any remaining stage-edge pids only
for pid in $(pgrep -f '/home/amdm/workspace/ViPSA/.venv/bin/python3 main.py|uv run main.py' || true); do
  cwd=$(readlink /proc/$pid/cwd 2>/dev/null || true)
  [ "$cwd" = "/home/amdm/workspace/ViPSA/stage" ] && kill -9 "$pid" || true
done

# Verify /dev/ttyACM0 released
fuser -v /dev/ttyACM0 || true

# Restart stage edge
cd /home/amdm/workspace/ViPSA/stage
uv run main.py
```

When running through Hermes, start the restart command as a tracked background process and watch for:

- `Connected to Arduino stage on /dev/openflexture`
- `stage Edge Service Ready`

Then verify with read-only PUDA:

```bash
RUN_ID=$(python3 -c 'import uuid; print(uuid.uuid4())')
puda machine start stage --run-id "$RUN_ID"
puda machine run stage get_current_position '{}' --run-id "$RUN_ID"
puda machine complete stage --run-id "$RUN_ID"
puda machine state stage
```

## Driver fix direction before future automatic approach

Patch the driver before trusting Stage-Z automation:

1. `move_z_by()` should clear serial input before sending commands.
2. Send G-code lines separately and wait for `ok` for each line; raise on `error:` or timeout.
3. Poll `?` until a real `<Idle...>` status after motion.
4. `get_current_position()` should query GRBL status (`MPos`/`WPos`) instead of returning only internal counters, or clearly label internal counters as unverified.
5. Driver command methods should raise exceptions on failed serial/motion status so PUDA returns command failure.
6. Replace `abort_motion()`'s `G90 G1 Z0 F100` hold-clear behavior with a true GRBL hold reset/unlock/status sequence unless an explicit move-to-zero is desired.
7. After patch/restart, run a tiny visually observed jog such as `+1` then `-1` before any contact approach.
