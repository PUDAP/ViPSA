# Stage state wait between Z moves during electrical approach

## Context

During a regular electrical-only ViPSA contact approach after a deliberate `stage.move_z_by(height=-10)` pre-move, the outer approach loop issued repeated `stage.move_z_by(height=+0.5)` commands with Keithley low-voltage reads between moves. After dozens of successful read/move cycles, a later stage move failed at PUDA START with:

```text
START command failed for machine stage: cannot start, <run_id> is currently running
```

The stage was briefly reported `busy`, then later returned `idle`; a follow-up read-only `stage.get_current_position()` succeeded. Electrical cleanup also succeeded (`keithley-2450.set_output(false)`, `keithley-707b.open_all()`, closed channels `nil`).

## Durable lesson

For stage-heavy approach loops, do not assume that a successful `puda protocol run` response plus a local `sleep(settle_s)` is enough before the next `stage.move_z_by`. Insert an explicit stage-idle wait after every Z move and before any subsequent stage command.

Recommended pattern:

```python
def wait_stage_idle(timeout_s=30, poll_s=0.25):
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        st = machine_state('stage')
        if isinstance(st, dict) and st.get('state') == 'idle':
            return st
        time.sleep(poll_s)
    raise RuntimeError(f'stage did not return idle within {timeout_s}s: {st}')
```

Use it after:

- initial Z pre-moves
- every coarse `move_z_by`
- every over-current retract / extra retract
- every fine-approach or final-trim move
- before final `get_current_position()`

If a stage START conflict still occurs:

1. Stop issuing additional motion commands.
2. Run electrical cleanup first: Keithley output off, 707B open all, verify closed channels `nil`.
3. Poll `puda machine state stage` until it returns `idle`.
4. Read `stage.get_current_position()`.
5. Optionally do one final low-voltage contact read with cleanup to determine whether contact was actually reached.

Report it as a motion-scheduler/state conflict, not as a successful completed approach unless the final current is inside the requested contact window.
