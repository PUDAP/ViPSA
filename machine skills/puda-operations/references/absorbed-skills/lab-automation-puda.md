# Absorbed skill: lab-automation-puda

Original package: `devops/lab-automation-puda` archived after consolidation into `puda-operations`.

Support files copied: ['references/ -> references/lab-automation-puda/'].

## First 80 lines of original SKILL.md for provenance

```markdown
---
name: lab-automation-puda
description: "Operate PUDA-connected lab machines safely via the puda CLI: discover machines, inspect commands/state, run protocol JSON, and verify hardware responses."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [puda, lab-automation, hardware, instruments, zaber, nats]
    created_by: agent
---

# Lab Automation with PUDA

Use this skill when the user asks to operate, move, inspect, or troubleshoot a lab machine exposed through the `puda` CLI, such as Zaber stages, Keithley instruments, lights, Biologic, Opentrons, or other PUDA machines.

## Safety stance

Hardware commands can move physical devices. Before sending motion or actuation commands:

1. Identify the target machine and command from `puda machine list` and `puda machine commands <machine_id>`.
2. Check machine state with `puda machine state <machine_id>`.
3. If the user omitted an axis, direction, magnitude, unit, or target device and the default is not obvious, ask for clarification.
4. Prefer small, explicit protocol files with a verification/readback command after the action.
5. Report the actual run ID, command response, and readback telemetry; do not infer success without PUDA output.

## Core workflow

1. Work from the PUDA project directory when one exists, commonly a directory containing `puda.config`, `puda.db`, and `protocols/`.
2. Discover machines:
   ```bash
   puda machine list
   ```
3. Inspect available commands:
   ```bash
   puda machine commands <machine_id>
   ```
4. Check state:
   ```bash
   puda machine state <machine_id>
   ```
5. Create a protocol JSON in `protocols/<uuid>.json` containing:
   - `project_id`
   - `protocol_id`
   - `user_id`
   - `username`
   - `description`
   - `timestamp`
   - `commands[]`
6. Validate before running:
   ```bash
   puda protocol validate --file protocols/<uuid>.json
   ```
7. Run the protocol:
   ```bash
   puda protocol run --file protocols/<uuid>.json
   ```
8. Verify from the returned command responses and any readback command data.

## Zaber stage notes

For Zaber stages exposed through PUDA, inspect commands first. Typical commands include:

- `move_x_by(distance, units=None)`
- `move_y_by(distance, units=None)`
- `move_x_to(position, units=None)`
- `move_y_to(position, units=None)`
- `get_current_position(units=None)`
- `configure_units(distance_units=None, velocity_units=None, acceleration_units=None)`

When the user asks for **microsteps** or **native units**, pass JSON `null` for `units` rather than a string unit like `"mm"`. Example command params:

```json
{"distance": 500, "units": null}
```

When the user asks for millimeters, pass `"mm"` explicitly:

```json
{"distance": 500, "units": "mm"}
```
