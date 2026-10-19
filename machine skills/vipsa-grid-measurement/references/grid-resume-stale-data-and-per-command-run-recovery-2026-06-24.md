# Grid resume after stale run/data and RUN_ID_MISMATCH recovery — 2026-06-24

Use this when a long ViPSA grid run is interrupted by network/NATS/gateway issues and the user asks to reset machines, delete stale run data, and restart from a specific device.

## Observed failure mode

After an interrupted 8×8 randomized-pulse grid run, machines could report `idle` / `run_id: null`, but queued commands in a restarted runner still intermittently failed with:

```text
RUN_ID_MISMATCH: Run ID mismatch: expected active run, got <fresh-run-id>
```

This happened even when the immediate `start` for the same fresh run id returned `success`. Some NATS routes/ports behaved differently for the same machine; one route could succeed for `stage` while another route gave `RUN_ID_MISMATCH`, and vice versa for the 707B. Treat this as duplicate/stale edge subscribers or inconsistent edge run-state after outage, not as a device-electrical failure.

## Safe restart workflow

1. Stop the active grid/resume process first.
2. Force conservative hardware cleanup:
   - complete any visible stale `run_id` if possible;
   - SMU outputs off: `keithley-2450.set_output(false)`, `keysight-b2902b.set_output(false)`;
   - `keithley-707b.open_all()` and verify `get_closed_channels == nil`;
   - verify the six ViPSA machines are `idle` with `run_id: null`.
3. Delete stale data only from the restart point onward. Preserve confirmed completed devices before the requested restart device.
   - Example: restart from device 6 → remove `device_06+` directories and prune `summary.partial.json` device records to devices `1–5`.
   - If the user says “delete old/stale data,” permanent deletion is acceptable; otherwise prefer moving to a timestamped backup first.
4. Patch/resume the runner so the traversal order starts at the requested device and summary metadata records the cleanup event.
5. Start the resume in a tracked background process with `notify_on_complete=true`.
6. Verify early progress with real artifacts, not just process status: `device_06/summary.json`, alignment images, `DONE.json`, and machine states.

## Robust command pattern after outage

If a shared long-lived run id is unstable after an outage, do not keep one global START open across all machines. Prefer a per-command transaction:

```text
for each machine command:
  run_id = fresh uuid
  immediate START(machine, run_id)
  queued command(machine, run_id)
  immediate COMPLETE(machine, run_id)   # always attempt, even if command failed
```

Add retries around the whole transaction when the queued command returns `RUN_ID_MISMATCH` after a successful START. Use a new fresh run id on each retry and complete any stale run id named in `cannot start, <old-run-id> is currently running`.

Pseudo-code:

```python
for attempt in range(1, 6):
    rid = str(uuid.uuid4())
    sr = await rawcmd(machine, rid, 'start', immediate=True)
    if not ok_start(sr, rid):
        stale = parse_stale_run(sr)
        if stale:
            await rawcmd(machine, stale, 'complete', immediate=True)
            sr = await rawcmd(machine, rid, 'start', immediate=True)
    if not ok_start(sr, rid):
        sleep(backoff); continue

    r = await rawcmd(machine, rid, name, params, immediate=False)
    await rawcmd(machine, rid, 'complete', immediate=True)

    if status_of(r) == 'success':
        return r
    if is_run_id_mismatch(r):
        sleep(backoff); continue
    raise RuntimeError(r)
```

This pattern is a recovery fallback for unstable post-outage state. Normal protocol-first operation remains preferred when the protocol runner and edge states are healthy.

## Reporting standard

Report separately:

- stale data removal scope (which device folders/summary rows were removed);
- machines reset/cleanup verification (`idle`, `run_id: null`, outputs off, 707B `nil`);
- restart point and background process id;
- first confirmed artifact/progress for the restart device;
- any remaining blocker as a control-path/NATS/run-state issue, not as a device result unless electrical data was actually acquired.
