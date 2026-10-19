# Electrical instrument address discovery notes

Use this reference when the user asks for PyVISA/GPIB/USB/TCPIP addresses for ViPSA electrical-test instruments.

## Machine IDs and naming aliases

- `keithley-707b` — Keithley 707B switch matrix / route controller.
- `keithley-2450` — Keithley 2450 SMU.
- `keysight-b2902b` — Keysight B2901BL/B2902-family SMU. The physical instrument may be called B2901BL while PUDA/driver names use B2902B-family labels.

## Safe first-pass workflow

1. Start with read-only PUDA metadata/state:
   ```bash
   for m in keithley-707b keithley-2450 keysight-b2902b; do
     echo "===== $m ====="
     puda machine state "$m"
     puda machine commands "$m" | sed -n '1,120p'
   done
   ```
2. If the edge responds to runs, prefer read-only commands:
   - SMUs: `identify()`
   - Switch matrix: `get_closed_channels()` is read-only, but it reports route state, not the VISA address.
3. If runs time out on `START`, do not infer live addresses from the mere existence of state/commands buckets.

## Direct NATS KV metadata inspection

PUDA publishes command signatures/docstrings to NATS JetStream KV buckets. This can confirm driver classes and available methods even when `puda machine list` omits stale/offline edges.

Observed relevant streams/buckets:

```text
KV_MACHINE_COMMANDS_keithley-2450  -> bucket MACHINE_COMMANDS_keithley-2450, key keithley-2450
KV_MACHINE_COMMANDS_keithley-707b  -> bucket MACHINE_COMMANDS_keithley-707b, key keithley-707b
KV_MACHINE_COMMANDS_keysight-b2902b -> bucket MACHINE_COMMANDS_keysight-b2902b, key keysight-b2902b
KV_MACHINE_STATE_keithley-2450
KV_MACHINE_STATE_keithley-707b
KV_MACHINE_STATE_keysight-b2902b
```

Minimal Python probe, using the `nats-py` package:

```python
import asyncio, nats

SERVERS = [
    "nats://100.109.131.12:4222",
    "nats://100.109.131.12:4223",
    "nats://100.109.131.12:4224",
]

async def main():
    nc = await nats.connect(SERVERS, connect_timeout=5)
    js = nc.jetstream()
    for bucket, key in [
        ("MACHINE_COMMANDS_keithley-2450", "keithley-2450"),
        ("MACHINE_COMMANDS_keithley-707b", "keithley-707b"),
        ("MACHINE_COMMANDS_keysight-b2902b", "keysight-b2902b"),
    ]:
        kv = await js.key_value(bucket=bucket)
        ent = await kv.get(key)
        print(f"\n===== {bucket}/{key} =====")
        print(ent.value.decode(errors="replace")[:2000])
    await nc.close()

asyncio.run(main())
```

Important limitation: the command metadata is generated from driver method signatures/docstrings (`inspect.signature` + docstrings). It usually does **not** include constructor parameters, `.env` values, or PyVISA resource strings. Treat it as capability discovery, not address discovery.

## PyVISA discovery

If running on the actual machine edge host with access to the instrument bus, use:

```python
import pyvisa
rm = pyvisa.ResourceManager("@py")  # or default backend if NI-VISA is installed
print(rm.list_resources())
```

An empty tuple only means the current host/backend cannot see VISA resources. It does not prove the instruments are absent; the addresses may live in the private edge driver repo, edge `.env`, or host-specific config outside the local PUDA project.

## Reporting standard

When addresses are not actually retrieved, say exactly what was verified:

- PUDA machine IDs confirmed.
- Driver command metadata exists / methods available.
- Whether live read-only `identify()` succeeded or timed out.
- Whether PyVISA discovery returned any resources from the current host.

Do not invent strings like `USB0::...::INSTR`, `GPIB0::...::INSTR`, or `TCPIP0::...::INSTR` unless they came from a config file, driver constructor, PyVISA discovery, or instrument response.
