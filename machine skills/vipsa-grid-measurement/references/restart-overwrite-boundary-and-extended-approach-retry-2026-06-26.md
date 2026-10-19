# Restart/overwrite boundary + extended approach retry (2026-06-26)

## Context

During an active S3 8x8 grid run, the user requested two live changes:

1. Move back to a prior device and rerun all devices from there while overwriting existing data.
2. If contact approach has no contact after the primary 120 steps, continue/retry for another 100 steps before declaring no-contact.

This belongs to the class of live grid-restart changes where stale per-device folders and partial summaries can otherwise cause the runner to skip devices or preserve old data unintentionally.

## Verified workflow

### 1. Stop the active runner and clean up hardware

- Kill the tracked active grid process first.
- Force/verify electrical safety before editing/restarting:
  - `keithley-2450.set_output(false)`
  - `keysight-b2902b.set_output(false)`
  - `keithley-2450.abort_measurement()`
  - `keysight-b2902b.abort_measurement()`
  - `keithley-707b.open_all()`
  - `keithley-707b.get_closed_channels()` should return `nil`
  - `light.turn_off()`
- Verify no old grid-run Python process is still active.

### 2. Overwrite from a requested boundary device

For a request like “move to device 7 and re-run all devices from there; overwrite existing data”:

- Preserve devices before the boundary only (`device_number < 7`).
- Delete stale active folders at and after the boundary:
  - `device_07`, `device_08`, …
- Prune `summary.partial.json` so `SUMMARY['devices']` keeps only devices before the boundary.
- Remove stale final `summary.json` if present; the restarted runner will regenerate it.
- Patch the continuation runner:
  - `START_AT_DEVICE=<boundary>`
  - `_completed_before_restart={devices before boundary}`
  - traversal restart must use the serpentine traversal index of `START_AT_DEVICE`, not numeric `>=` filtering.
  - record a `resume_events` entry noting overwrite/restart boundary and preserved devices.

### 3. Restart cleanly and verify first new artifacts

- Start the patched runner as a tracked background process with `notify_on_complete=True`.
- Verify:
  - process is running
  - `device_<boundary>/summary.json` exists with `status: started`
  - old folders at/after the boundary were actually removed before restart
  - `summary.partial.json` still contains only pre-boundary completed devices until the new device finishes

## Extended approach retry patch

When the user says: “when approaching, if there is no contact after 120 steps, retry approach for another 100 steps”:

- Stop the active runner at a safe boundary or immediately if it is early/partial and user wants the behavior to apply now.
- Clean up electrical outputs/routes before editing.
- Patch the `approach()` routine to treat 120 as the primary budget and add a second forward-search budget:

```python
primary_max_attempts = 120
extra_retry_attempts = 100
total_max_attempts = primary_max_attempts + extra_retry_attempts

for a in range(total_max_attempts + 1):
    # read current
    if lower <= abs_i <= upper:
        status = 'in_window' if a <= primary_max_attempts else 'in_window_after_extra_retry'
        break
    if abs_i > upper:
        status = 'over_current' if a <= primary_max_attempts else 'over_current_after_extra_retry'
        break
    if a == primary_max_attempts:
        log.append({'kind': 'retry_boundary', 'reason': 'no_contact_after_primary_120_steps'})
    if a == total_max_attempts:
        status = 'no_contact_after_primary_120_plus_extra_100'
        break
    # move Z forward by the existing approach step
```

- Store approach metadata:
  - `primary_max_attempts: 120`
  - `extra_retry_attempts: 100`
  - `max_attempts: 220`
  - `retry_after_no_contact_120: true`
  - `retry_started: <bool>`
- Update all downstream logic that previously checked only `status == 'no_contact_after_max'` to also handle the new terminal status `no_contact_after_primary_120_plus_extra_100`.
- Update `open_weak` classification to include both no-contact statuses.
- If a partial device folder was created under the old approach logic, delete that boundary device folder and restart it cleanly so the new approach metadata and behavior are used from the beginning.

## Reporting standard

Keep the user-facing report concise:

- old runner stopped / new runner ID
- cleanup evidence: output off, 707B `nil`, light off
- deleted/overwritten device range
- preserved summary devices
- patched approach budgets (`120 + 100 = 220`)
- verified fresh `device_N/summary.json` with `status: started`

Do not spam per-step approach reads/moves; the device summary/approach JSON carries that detail.