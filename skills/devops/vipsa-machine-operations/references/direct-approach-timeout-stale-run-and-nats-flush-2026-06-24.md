# Direct contact-approach timeout, stale run cleanup, and nats.py flush pitfall (2026-06-24)

Context: a current-device contact approach was started after manual Z moves and lights-on/off. The normal `puda protocol run` path repeatedly hit NATS route/connect timeouts for Keithley/707B/stage even though direct NATS command transactions could still reach the machines. A direct contact-approach script was then used as a fallback.

Reusable lessons:

1. **Turn lights off before electrical approach**, even if the previous user command turned them on for viewing/alignment.
2. If the normal protocol path cannot connect but direct NATS transactions still work, use short direct transactions only after making a real cleanup plan:
   - complete any stale run id reported by `RUN_ID_MISMATCH` on all involved machines (`keithley-2450`, `keithley-707b`, `stage` for approach);
   - force Keithley `set_output(false)`;
   - run 707B `open_all()` and verify `get_closed_channels() == "nil"`;
   - verify/read stage position if possible.
3. If a direct approach process is killed by a wrapper/terminal timeout, assume it may have left a shared active run on several machines. Do **not** immediately start a new approach. First probe with a harmless command or direct START. If START responses say `cannot start, <old-run-id> is currently running`, send direct `complete` with exactly that old run id to every machine that participated in the approach, then retry cleanup/verification.
4. With `nats.py`, `await nc.flush()` after subscribing/publishing can itself raise `FlushTimeoutError` during flaky NATS periods even when command publish/subscribe transactions still succeed. For direct fallback scripts, a pragmatic pattern is:
   - connect to one server at a time with short timeout, trying `4223`, then `4222`, then `4224`;
   - subscribe to response subjects;
   - use a short `await asyncio.sleep(0.5)` instead of relying on flush as the gate;
   - publish commands and wait for matching response by `machine_id`, `run_id`, command name/step;
   - close the connection after cleanup.
5. Do not use illegal Z trim increments in fallback scripts. The minimum valid stage Z increment remains `0.25` steps; replace any legacy `-0.1` trim with `-0.25`.
6. If approach remains pA-scale/sub-nA after a bounded continuation, report it as **open / very weak contact** and stop with cleanup verified rather than silently continuing to large unbounded Z travel.

Minimal direct stale-run completion payload pattern:

```python
# For each involved machine m and stale run_id old_id:
await nc.publish(
    f"puda.{m}.cmd.immediate",
    json.dumps(payload(m, old_id, "complete", {}, step=999), separators=(",", ":")).encode(),
)
# Wait for response.status == "success" before retrying commands.
```

Minimal safe direct one-command transaction pattern:

```python
# start -> one queued command -> complete, matching responses by run_id + machine_id.
# Use sleep after subscriptions instead of flush if flush is timing out.
await nc.subscribe(f"puda.{machine}.cmd.response.immediate", cb=cb)
await nc.subscribe(f"puda.{machine}.cmd.response.queue", cb=cb)
await asyncio.sleep(0.5)
await nc.publish(f"puda.{machine}.cmd.immediate", start_payload)
# wait for START success
await nc.publish(f"puda.{machine}.cmd.queue", command_payload)
# wait for command success
await nc.publish(f"puda.{machine}.cmd.immediate", complete_payload)
# wait for COMPLETE success
```

Reporting standard for this failure mode:

- Say clearly that the normal PUDA protocol path was blocked by NATS route timeouts and direct fallback was used.
- Include final current relative to the contact target, total Z moved during the attempt, final stage Z readback, and cleanup status.
- If cleanup/verification used direct NATS because CLI state reads were timing out, say so, but do not overstate CLI `machine state` verification.
