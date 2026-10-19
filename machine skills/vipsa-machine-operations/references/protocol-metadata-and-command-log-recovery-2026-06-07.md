# PUDA protocol metadata + command-log recovery (2026-06-07)

## Trigger

During a live ViPSA resistance check and conditional Z move, a generated minimal protocol JSON with only `commands` failed:

```text
Error: failed to run protocol: user_id is required in the protocol file
```

## Durable lesson

For active ViPSA protocols, include the same metadata fields used by project-generated protocol files, not just the command list:

```json
{
  "project_id": "<active project id>",
  "protocol_id": "<new uuid>",
  "user_id": "<puda user id>",
  "username": "<puda username>",
  "description": "<short description>",
  "timestamp": "<UTC ISO timestamp>",
  "commands": [
    {"step_number": 1, "name": "...", "machine_id": "...", "params": {}}
  ]
}
```

The active ViPSA project/user values observed in existing protocol files were:

```text
project_id = ed111132-ab51-456d-8776-436a2d604378
user_id    = 1204c118-ecb8-4a91-abca-26c18c0bff84
username   = vipsa
```

Prefer deriving these from existing project protocol files or PUDA config when available rather than hard-coding blindly.

## Response parsing pitfall

When running `puda protocol run` from Python with `subprocess.run(capture_output=True)`, do not assume the machine response JSON is only in `stdout`. The CLI may emit useful run logs/responses to `stderr`, and the canonical responses are also written to `command_log`.

Robust pattern:

1. Capture and inspect `stdout + stderr` together for response JSON.
2. If response extraction fails, query `command_log` for the run/protocol or for the latest matching machine command.
3. For measurement payloads, parse:
   - `payload.response.data.result`
   - Keithley current fields: `I_meas (A)` first, then `Current (A)`
   - Stage position: `response.data.result` as `[x, y, z]`
4. Still run cleanup/verification protocols even if the first parser fails.

Example SQL recovery:

```bash
puda db exec "SELECT command_log_id, run_id, step_number, machine_id, command_name, payload FROM command_log WHERE machine_id='keithley-2450' AND command_name='hold_voltage_measure_current' ORDER BY command_log_id DESC LIMIT 1"
```

## Session outcome pattern

A 10 mV resistance check returned `I_meas (A)=6.003701e-11`, so the device was below the established contact threshold (`1e-8 A`). The correct conditional behavior was to **not** move Z down. Final verification still checked stage position, SMU/switch cleanup, and idle states.
