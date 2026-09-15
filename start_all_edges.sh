#!/usr/bin/env bash
set -euo pipefail

# Start all ViPSA PUDA edge services, similar to start_all_edges.bat.
# Each edge runs in the background from its own workspace directory.

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${ROOT_DIR}/logs/edges"

EDGES=(
  zaber
  stage
  light
  keysight-b2902b
  keithley-707b
  keithley-2450
)

mkdir -p "${LOG_DIR}"

pids=()

cleanup() {
  if ((${#pids[@]})); then
    echo
    echo "Stopping edge processes..."
    kill "${pids[@]}" 2>/dev/null || true
    wait "${pids[@]}" 2>/dev/null || true
  fi
}
trap cleanup INT TERM EXIT

for edge in "${EDGES[@]}"; do
  edge_dir="${ROOT_DIR}/${edge}"
  log_file="${LOG_DIR}/${edge}.log"

  if [[ ! -d "${edge_dir}" ]]; then
    echo "Missing edge directory: ${edge_dir}" >&2
    exit 1
  fi

  if [[ ! -f "${edge_dir}/main.py" ]]; then
    echo "Missing edge entrypoint: ${edge_dir}/main.py" >&2
    exit 1
  fi

  echo "Starting ${edge} (log: ${log_file})"
  (
    cd "${edge_dir}"
    exec uv run main.py
  ) >"${log_file}" 2>&1 &
  pids+=("$!")
done

echo
echo "Started ${#pids[@]} edge services. Press Ctrl+C to stop them."
echo "Logs are in: ${LOG_DIR}"

wait "${pids[@]}"
