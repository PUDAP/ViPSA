# ViPSA grid DONE.json error-artifact triage (2026-07-01)

Use this when retrospectively answering "what happened to the previous run?" or deciding where to resume after a long grid runner failed.

## Lesson

A `device_N/DONE.json` file is not sufficient proof that a device was actually measured. Some grid runners write `DONE.json` in a `finally` block even when the per-device `summary.json` has `status: "error"` and no approach/DCIV/pulse artifacts. After a NATS or connection failure, this can cascade quickly across the remaining traversal devices and create many `DONE.json` sentinels with `ConnectionClosedError()` or similar errors.

## Triage steps

1. Inspect the run-level `summary.json` / `summary.partial.json` and each `device_*/summary.json`.
2. Count devices by `summary.status`, not by `DONE.json` existence alone.
3. Treat a device as validly measured only if:
   - `summary.status == "completed"`, and
   - the requested measurement artifacts are present for that device (for example `dciv`, `randomized_pulse`, plot/CSV/JSON), unless the requested protocol legitimately stopped earlier with a recorded measurement reason.
4. Treat `DONE.json` with `status: "error"`, `ConnectionClosedError()`, START timeout, or missing electrical artifacts as stale/error artifacts, not completed measurements.
5. For resume/restart, archive or patch around those stale `DONE.json` folders before launching; otherwise the runner may silently skip requested measurements.
6. Report cleanup/state verification separately from artifact triage. If PUDA/NATS state checks time out, say cleanup verification is blocked/unverified rather than claiming the hardware is safe.

## Concise reporting pattern

- Run folder path
- Valid completed devices
- First failed device and exact error
- Any cascade of stale `DONE.json` error artifacts
- Whether a runner process is active
- Whether hardware cleanup/state was verified or blocked
