# keysight-b2902b

PUDA edge service for the Keysight B2900/B2902B source-measure unit.

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
