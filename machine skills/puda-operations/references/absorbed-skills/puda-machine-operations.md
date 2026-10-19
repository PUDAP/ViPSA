# Absorbed skill: puda-machine-operations

Original package: `devops/puda-machine-operations` archived after consolidation into `puda-operations`.

Support files copied: ['references/ -> references/puda-machine-operations/'].

## First 80 lines of original SKILL.md for provenance

```markdown
---
name: puda-machine-operations
description: "Operate PUDA machine subsets via the puda CLI: discover machines, inspect commands, build protocols, run sequences, and verify states."
version: 1.0.0
author: local
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [PUDA, machines, lab-automation, NATS, protocols]
prerequisites:
  commands: [puda]
---

# PUDA Machine Operations

Use this skill when the user asks to control, sequence, inspect, or troubleshoot PUDA-connected machines such as `light`, `zaber`, `stage`, `keithley-*`, or another ViPSA/PUDA machine subset.

## Core workflow

1. **Work from the PUDA project root when available.** Common local project root seen in sessions: `/home/vipsa/vipsa-puda-project`. The project config may include `puda.config`, `puda.db`, `project.md`, and `protocols/`.
2. **Inspect machine capabilities before constructing commands:**
   ```bash
   puda machine commands <machine_id>
   puda machine state <machine_id>
   ```
3. **Create a protocol JSON for operations, then validate it:**
   ```bash
   puda protocol validate --file /path/to/protocol.json
   ```
4. **Run via PUDA and require real success output:**
   ```bash
   puda protocol run --file /path/to/protocol.json
   ```
   Treat success as grounded only when the run output shows the command succeeded and ends with `Protocol commands completed successfully!`.
5. **Verify final state after motion/light sequences:**
   ```bash
   puda machine state light
   puda machine state zaber
   ```

## Protocol JSON shape

A minimal protocol contains:

```json
{
  "project_id": "<project-id-if-known>",
  "protocol_id": "<uuid>",
  "user_id": "<user-id>",
  "username": "<username>",
  "description": "Human readable operation summary",
  "timestamp": "<UTC ISO timestamp>",
  "commands": [
    {
      "step_number": 1,
      "name": "turn_on",
      "machine_id": "light",
      "params": {}
    }
  ]
}
```

Notes:
- Commands with the same `step_number` run in parallel, but not for the same machine.
- Step numbers must not decrease through the command list.
- Use separate protocol runs plus `sleep` in the orchestrating script when the requested sequence requires sub-second waits and PUDA has no native wait command.

## Known ViPSA command patterns

### `light`

Useful commands discovered via `puda machine commands light`:

- `turn_on()`
- `turn_off()`
- `set_green()`
- `set_red()`
- `set_rainbow()`
```
