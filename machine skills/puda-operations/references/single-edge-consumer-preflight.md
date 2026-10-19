# Single-edge-consumer preflight for long PUDA runs

Use before a long multi-machine grid or electrical campaign when commands time out, a START succeeds but the queued command is rejected, or state timestamps do not advance.

## Failure mechanism

PUDA queue and immediate subjects use durable consumers. If two edge processes for the same `machine_id` are running, different lifecycle messages can be consumed by different processes. One process may accept START while another consumes the queued driver command and responds `RUN_ID_MISMATCH`; alternatively, the controller waits while the visible machine state stays stale. This can look like a runner bug even though each edge process is individually healthy.

## Preflight

1. Require the prior electrical runner to be finished and all controlled machines idle.
2. Enumerate edge processes by both command and `/proc/<pid>/cwd`; several identical `uv run main.py` commands cannot be distinguished by command line alone.
3. Require exactly one process per required machine directory (`stage`, `zaber`, `light`, `keithley-2450`, `keithley-707b`, etc.).
4. Stop duplicates only while the affected machine is idle. Restart one canonical edge for any machine whose durable consumer may have been stolen by a duplicate.
5. Wait for `Edge Service Ready`, queue subscription, immediate subscription, and command publication in logs.
6. Clear stale run ownership before launch. `puda machine reset <machine>` may report a response timeout even when the reset took effect; read machine state afterward and do not repeat if it is already `idle` with `run_id: null`.
7. Run a harmless lifecycle/readback command and confirm the state timestamp advances before starting the long runner.

## Long-run startup verification

Do not equate a live Python PID with a started experiment. Require at least one of:

- newly created per-device artifacts,
- advancing machine-state timestamps,
- expected START/queue/COMPLETE log entries,
- or a verified target/readback.

If a fresh runner created only its initial manifest and no hardware command was consumed, stop it, archive that manifest as a startup failure, repair edge ownership, and restart from a clean output directory. Do not claim lateral motion or electrical stress occurred without corresponding edge responses/artifacts.

## Safety

Never terminate duplicate edges while their machine is busy. First identify the valid active run and let it finish or stop it through its cleanup path. After any recovery, verify electrical outputs off and switch-matrix routes open before motion or a new experiment.
