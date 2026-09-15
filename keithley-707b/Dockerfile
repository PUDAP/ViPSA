FROM python:3.14-slim-bookworm

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
COPY keithley-707b/pyproject.toml keithley-707b/pyproject.toml

RUN uv sync --frozen --no-dev --no-install-project --package keithley-707b-edge

COPY keithley-707b/ keithley-707b/

WORKDIR /app/keithley-707b

CMD ["uv", "run", "python", "main.py"]
