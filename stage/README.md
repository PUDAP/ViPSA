# stage

PUDA edge service for the ViPSA OpenFlexure GRBL stage.

Scaffolded from [PUDAP/machine-template](https://github.com/PUDAP/machine-template).

## Setup

```bash
cp .env.example .env
# edit .env
uv sync
uv run python main.py
```

## Persistent position and hard limits

The OpenFlexure logical position is stored in
`state/openflexure_position.json` by default. The driver loads this file before
opening the serial port, synchronizes GRBL work coordinates without moving the
stage, and atomically commits the state after every confirmed move and on
graceful disconnect. This preserves the tracked position across PUDA edge and
NATS restarts, Hermes sessions, and PC reboots.

All X, Y, and Z targets are restricted to `-300 <= position <= +300` logical
steps. A request outside that range is rejected before any serial command is
sent. Corrupt, out-of-range, pending, or uncertain state fails closed and
requires explicit user reconciliation; it is never silently reset to zero.

Configuration:

```text
STAGE_STATE_PATH=state/openflexure_position.json
STAGE_POSITION_LIMIT=300
```

The Docker compose service mounts `./state` into the container so the JSON file
is stored on the host rather than in the container filesystem.

## Docker

```bash
docker compose up -d --build
```
