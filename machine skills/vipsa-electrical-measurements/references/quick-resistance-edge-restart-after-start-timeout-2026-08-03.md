# Quick resistance check edge restart after START timeout (2026-08-03)

## Trigger

Use when the terse ViPSA request is `check resistance`, the canonical `tools/quick_resistance_check.py` fails before measurement with PUDA START timeouts for `keithley-2450` and/or `keithley-707b`, and machine state timestamps look stale from a prior session.

## Observed failure shape

The canonical script connected to bears NATS and created the protocol, but failed before any measurement rows:

```text
START command failed for machine keithley-2450: timeout waiting for response after 30 seconds
```

Emergency cleanup protocols also timed out on START for `keithley-2450` / `keithley-707b`. `machine state` still returned `idle/run_id:null`, but with stale timestamps from days earlier; do not treat stale state timestamps as fresh edge readiness.

## Recovery pattern

1. Inspect/read machine states and process table enough to distinguish stale KV state from active edge processes.
2. Restart only the needed ViPSA electrical edges:
   ```bash
   cd /home/amdm/workspace/ViPSA/keithley-2450 && uv run main.py
   cd /home/amdm/workspace/ViPSA/keithley-707b && uv run main.py
   cd /home/amdm/workspace/ViPSA/light && uv run main.py
   ```
   Run them as long-lived background processes.
3. If the restarted 2450/707B immediately consumes old START messages or reports `RUN_ID_MISMATCH`, reset/recover the affected machine IDs with bears NATS:
   ```bash
   NATS='nats://bears:4222,nats://bears:4223,nats://bears:4224'
   puda --nats-servers "$NATS" machine reset keithley-2450 || true
   puda --nats-servers "$NATS" machine reset keithley-707b || true
   puda --nats-servers "$NATS" machine state keithley-2450
   puda --nats-servers "$NATS" machine state keithley-707b
   ```
4. For the light edge, `reset` may be unknown/restricted. If lights should be off before the electrical check, use a proper lifecycle:
   ```bash
   RID=$(python3 - <<'PY'
   import uuid; print(uuid.uuid4())
   PY
   )
   puda --nats-servers "$NATS" machine start light --run-id "$RID"
   puda --nats-servers "$NATS" machine run light turn_off '{}' --run-id "$RID"
   puda --nats-servers "$NATS" machine complete light --run-id "$RID"
   ```
5. Retry the canonical check, still using bears explicitly:
   ```bash
   python3 tools/quick_resistance_check.py --nats-servers 'nats://bears:4222,nats://bears:4223,nats://bears:4224'
   ```
6. Report only the retry measurement as the resistance result; mention the first attempt was blocked by stale/dormant edge START timeout only if useful.

## Reporting pattern from the successful retry

- Dark check after explicit light-off lifecycle.
- `0 V` offset was tens of nA.
- `±10 mV` and `±50 mV` hit the `1 µA` read compliance.
- Classify as `conductive_compliance_limited_or_short_like`.
- Report resistance as bounds, not precise ohmic values: `10 mV` compliance-limited read implies `R <= ~10 kΩ`; paired differential estimates are compliance-limited and not clean ohmic resistance.
- Verify cleanup: Keithley idle/null, 707B open/nil, light idle/off.
