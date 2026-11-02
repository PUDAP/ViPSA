# No-skip grid restart and stale DONE cleanup (2026-06-30)

## Context

During a paused/restarted ViPSA grid run, the user explicitly said not to skip measurements and requested remeasurement from a specific device. The runner had safety/contact gates converted to record-only metadata, but old `device_##/DONE.json` folders from prior partial attempts caused subsequent devices to be skipped until those stale folders were archived.

## Durable workflow lesson

When the user requests a **no-skip remeasurement** from device N, do both of these before launching the continuation runner:

1. Patch/verify the measurement gates are record-only rather than blockers, if that is the requested override:
   - keep contact/health/safety diagnostics in metadata;
   - still attempt DCIV and randomized pulses under the configured safer compliance/reset caps unless the user changes them;
   - mark the override explicitly in per-device summaries (for example `no_skip_override: true`).
2. Remove stale skip sentinels for the rerun range:
   - archive or rename existing `device_##` folders that contain stale `DONE.json` or partial artifacts for the restart range;
   - prune or update run summary entries from the restart device onward if the runner consults the summary;
   - especially archive the target device and the immediately following devices that were created by previous aborted attempts.

Do not rely on `START_AT_DEVICE=N` alone. A continuation runner may still skip a requested device if `DONE.json` already exists.

## Verification before reporting success

After launch, verify from actual artifacts, not just process state:

- active runner PID/session is alive;
- target device folder is newly started or completed with fresh timestamps;
- per-device summary shows the no-skip override and real measurement fields;
- DCIV has a real max-current field or saved CSV/JSON;
- pulse summary shows collected trains/pulses if pulses completed;
- old archived folders are clearly named and not still in the active device path.

If an earlier runner completes with exit code `143`, treat it as expected SIGTERM only if it was intentionally killed for patch/restart/pause. Confirm hardware cleanup separately rather than assuming the exit code is safe by itself.

## Reporting standard

Keep the update concise:

- say which device was restarted/re-done;
- report fresh DCIV max `|I|` and pulse train count when available;
- name the current in-progress device if the runner is still active;
- explicitly state if a stale `DONE.json` skip was found and corrected;
- include cleanup/idle verification if the runner was stopped.
