# Shared uv workspace dependency recovery

Use when ViPSA electrical edges loop with `Could not locate a VISA implementation` after environment changes.

The ViPSA repository is a uv workspace. The root project declares `pyvisa-py`, while workspace edge projects declare PUDA/runtime dependencies. Plain `uv sync --locked` can sync only the root project and uninstall workspace-member packages such as `puda`, `nats-py`, and `pyserial`.

Recover with:

```bash
cd /home/amdm/workspace/ViPSA
uv sync --locked --all-packages
```

Verify before relying on the existing launcher retry:

```bash
/home/amdm/workspace/ViPSA/.venv/bin/python - <<'PY'
import importlib.util, pyvisa
print(pyvisa.highlevel.list_backends())  # must include "py"
for name in ("puda", "nats", "serial"):
    print(name, bool(importlib.util.find_spec(name)))
PY
```

Do not restart healthy motion/light edges merely to repair this shared dependency set.

After an edge restart, CLI KV state may remain stale (for example, showing an old active run) even when the replacement edge is internally idle. Reconcile with matched live lifecycle responses and edge logs. A direct START with the exact stale run ID followed by COMPLETE can refresh the real edge lifecycle without executing a driver command. Require matched successful responses for both operations; do not infer completion from stale `puda machine state` output alone.
