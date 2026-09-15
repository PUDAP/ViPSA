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

## Docker

```bash
docker compose up -d --build
```
