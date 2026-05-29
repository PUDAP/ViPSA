FROM python:3.14-slim-bookworm

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
COPY keithley-2450/pyproject.toml keithley-2450/pyproject.toml

RUN uv sync --frozen --no-dev --no-install-project --package keithley-2450-edge

COPY keithley-2450/ keithley-2450/

WORKDIR /app/keithley-2450

CMD ["uv", "run", "python", "main.py"]
