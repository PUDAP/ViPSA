# Electrical machine readiness, IDN checks, and direct NATS fallback (2026-07-07)

## Trigger
Use when the user asks whether ViPSA electrical machines are available, asks to run `*IDN?`/ID checks, or PUDA CLI discovery is flaky but raw NATS command subjects still work.

## Readiness checks learned

1. `puda machine list --json` can lag or return only actively advertised heartbeat machines. Do not treat omitted known ViPSA electrical machines as definitely unavailable.
2. Probe exact known electrical IDs directly:
   ```bash
   for m in keithley-2450 keithley-707b keysight-b2902b; do
     timeout 8 puda --nats-servers nats://100.109.131.12:4223 machine state "$m"
     timeout 8 puda --nats-servers nats://100.109.131.12:4223 machine commands "$m" | head -40
   done
   ```
3. Interpret results carefully:
   - `machine list` advertising a machine + `machine commands` returning signatures proves the edge is reachable at the discovery/metadata level.
   - `machine state` can return stale timestamps; report stale timestamps explicitly instead of implying fresh instrument state.

## IDN/identify results from this session

Validated via direct PUDA/NATS start → queued command → complete on `100.109.131.12:4223`:

- `keithley-2450.identify()` returned:
  ```text
  KEITHLEY INSTRUMENTS,MODEL 2450,04507059,1.7.5b
  ```
- `keysight-b2902b.identify()` returned:
  ```text
  Keysight Technologies,B2901BL,MY61390645,5.0.2029.1911
  ```
- `keithley-707b` does **not** expose `identify()` in the current PUDA command surface. Sending `identify` returned:
  ```text
  UNKNOWN_COMMAND: Unknown or restricted command: identify
  ```

## 707B cleanup pitfall

A failed unknown command on `keithley-707b` can leave the machine state as `error` with the attempted `run_id`. After such a probe, immediately recover and verify:

```bash
timeout 10 puda --nats-servers nats://100.109.131.12:4223 machine reset keithley-707b
timeout 8 puda --nats-servers nats://100.109.131.12:4223 machine state keithley-707b
```

Expected recovery evidence observed:

```text
keithley-707b: reset command sent successfully
{"state":"idle","run_id":null}
```

## Direct raw NATS fallback without `nats.py`

If the active Python environment does not have `nats`/`nats.py`, a minimal socket-level NATS client can still perform simple PUDA command transactions:

1. Open TCP to `100.109.131.12:4223` first, then try `4222`/`4224`.
2. Read initial `INFO`.
3. Send:
   ```text
   CONNECT {"verbose":false}\r\nPING\r\n
   ```
4. Wait for `PONG`.
5. Subscribe to:
   ```text
   puda.<machine>.cmd.response.immediate
   puda.<machine>.cmd.response.queue
   ```
6. Publish `start` to `puda.<machine>.cmd.immediate`.
7. Only if START succeeds, publish the driver method to `puda.<machine>.cmd.queue`.
8. Publish `complete` to `puda.<machine>.cmd.immediate` and verify/cleanup.

This fallback was used successfully for `light.turn_on()`, `keithley-2450.identify()`, and `keysight-b2902b.identify()` when normal project/protocol routing was unavailable from the current working directory.

## Resetting/restarting all ViPSA edges safely

When the user requests an all-edge reset while a measurement is active:

1. **Stop the measurement runner first.** A Keithley native list may still be executing even if orchestration is interrupted; do not restart instrument edges while the runner is still issuing commands.
2. Restart each edge process exactly once, then verify the replacement reached its NATS-ready signal. Avoid duplicate edge instances.
3. Use driver `reset` only on edges that expose it. Electrical edges may support reset, while `light`, `stage`, and `zaber` can reject it as `UNKNOWN_COMMAND` and enter an error state. For those edges, use process restart plus a harmless live verification:
   - light: `connect` (preserve any user-latched light state)
   - stage: `get_current_position`
   - zaber: `get_current_position`
4. Distinguish a logical PUDA reset from a physical driver reconnect. If `keithley-707b` returns a current NATS state but `open_all` fails with `USBError: [Errno 19] No such device (it may have been disconnected)`, `puda machine reset keithley-707b` may clear `state/run_id` without reopening the VISA/USB handle. Restart only the 707B edge process, wait for fresh NATS subscriptions, then run a short lifecycle-managed verification containing `open_all` followed by `get_closed_channels`; require `result: nil` before electrical routing or stress.
5. If a restarted USBTMC edge reports `USBError: [Errno 16] Resource busy`, stop its retrying process before diagnosing. A retry loop can retain multiple USB descriptors and contend with itself.
6. Inspect the exact USB device owner with `lsof`/`fuser` on `/dev/bus/usb/...`. Once unowned, reset only that instrument with `usbreset <VID:PID>`, then launch one edge instance. Verify that the USB bus/device path is still current after reset because enumeration can change.
7. Preserve logical position and state before restart. Some mechanical drivers keep position only in process memory: after restarting `stage`, a fresh `get_current_position` may report `[0,0,0]` even though the hardware did not physically move. Treat that as **lost software origin/readback**, not physical zero, and do not use it to claim motion or absolute Z. Recover position from the last verified readback/artifact or re-establish a trusted reference before any position-dependent move. Likewise, restart-only verification for `light` must not silently change a user-latched illumination state.
8. Verify hardware readiness—not only NATS state:
   - Keithley 2450: correct identity, empty error queue, output off, idle/run_id null.
   - Keithley 707B: `open_all`, `get_closed_channels == nil`, idle/run_id null.
   - Keysight: identify/readback, output off, idle/run_id null.
   - Stage/Zaber: harmless readback, but compare against the pre-restart value and flag discontinuity.
   - Light: harmless connection/telemetry check that preserves the requested light state.
9. Retry into a **fresh run directory**. Record whether the interrupted attempt acquired a verified complete cycle, returned partial records, or returned no records. A native-list timeout with no returned trace does **not** prove zero stress: the instrument may have traversed part or all of the list before `*OPC?` timed out. Label it `outcome_unknown_after_possible_stress`, never merge it with a fresh retry, and obtain explicit authorization before repeating potentially destructive history when authorization is not already clear.

A CLI reset can time out even though the edge applied it if response serialization fails. Inspect edge logs and fresh state/readiness before sending another reset; timeout alone does not prove reset failure.

## Duplicate-owner recovery findings (2026-09-15)

- `start_all_edges.sh` can coexist with orphaned `uv run main.py` copies. Inspect exact cwd/cmdline/parents first. The launcher has a cleanup trap that kills all its children: do not terminate it when preserving stage/Zaber. It does not respawn children; terminating only affected Python children also lets their `uv` wrappers exit, while the launcher remains waiting for healthy mechanical children.
- Duplicate failed electrical initializations accumulated 1008 USB descriptors per process (1016 total FDs), then raised Errno 24 in VISA discovery. The healthy originals each had one USB FD. Both drivers unconditionally call `rm.list_resources()` even with explicit addresses, and main retries on exceptions. Removing duplicate owners and starting once restored 13 total FDs / one USB FD. Treat an eventual TCPIP socket allocation error as potentially downstream of leaked USB handles, not proof of a socket leak.
- Fresh tracked Hermes terminal daemons: avoid shell `exec` for these launches. In this runtime it caused process polling to falsely mark live Python daemons exited after cmdline replacement. Use `NATS_SERVERS=<approved cluster> /exact/venv/bin/python3 main.py > <fresh-log> 2>&1; rc=$?; exit "$rc"` with `background=true`, retaining a shell wrapper. Verify both process handle status and exact Python child PID. Do not create a second owner to repair tracking without stopping/releasing the first.
- Current SMU live surfaces expose `set_output(enabled=False)` and `read_errors()`, but no output-state getter. Report output-off command acknowledgements honestly, not an independent output readback. An existing Keysight `-113,Undefined header` was drained; subsequent off + read_errors returned an empty queue. No measurement/read-bias is needed for this control-plane check.

## Reporting standard

For electrical availability reports, separate:

- **Advertised now in `machine list`**
- **Known ViPSA machine IDs with readable state/commands**
- **Fresh vs stale timestamp**
- **Actual command response** for IDN/identify
- **Cleanup state** after any failed command probe
