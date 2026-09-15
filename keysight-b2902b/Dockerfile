FROM python:3.14-slim-bookworm

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
COPY keysight-b2902b/pyproject.toml keysight-b2902b/pyproject.toml

RUN uv sync --frozen --no-dev --no-install-project --package keysight-b2902b-edge

COPY keysight-b2902b/ keysight-b2902b/

WORKDIR /app/keysight-b2902b

CMD ["uv", "run", "python", "main.py"]
