# Direct NATS fallback during advertised-route outage (2026-06-29)

Use this note when ViPSA machine operations are blocked because the PUDA CLI can initially connect to a Tailscale NATS endpoint, but then follows server-advertised internal/LAN `connect_urls` that the Hermes/WSL host cannot reach.

## Observed pattern

- `puda protocol run --nats-servers nats://100.109.131.12:4222` can still fail by trying an advertised `192.168.50.6:4223` URL.
- Raw/direct command transactions to edge response subjects can still work from the same host.
- `nats.py` `flush()` may time out even when direct publish/subscribe command responses still arrive.

## Safe fallback recipe

Use protocol-first by default. Switch to direct/raw NATS only when protocol routing is blocked and the task is bounded/simple or safety cleanup is needed.

1. Connect to one reachable Tailscale server with reconnect/discovery disabled, e.g. `allow_reconnect=False`.
2. Subscribe to both response subjects for each involved machine:
   - `puda.<machine>.cmd.response.immediate`
   - `puda.<machine>.cmd.response.queue`
3. Avoid relying solely on `flush()` during this outage. It is acceptable to publish, sleep briefly, and wait for a matching response by `machine_id`, `run_id`, and command name.
4. For each machine command, use a fresh short transaction:
   - publish `start` on `.cmd.immediate`
   - require `start` success, or complete the stale run id named in `cannot start, <run_id> is currently running`
   - publish exactly one queued driver command
   - require the queued command response to be `success`
   - publish `complete` and wait for/record the response when possible
5. For electrical work, always force cleanup afterward:
   - `keithley-2450.set_output(false)`
   - `keithley-707b.open_all()`
   - `keithley-707b.get_closed_channels()` should return `nil`
6. Report direct command response evidence, not intent. If CLI state probes time out after successful direct cleanup, say cleanup was verified by direct responses and state readback was unavailable.

## Concrete commands used successfully

- `light.turn_on()` and `light.turn_off()` with final direct `complete` response.
- Keithley/707B low-bias resistance check:
  - light off
  - Keithley output off
  - 707B `connect_keithley_smu()`
  - Keithley `hold_voltage_measure_current()` at `0 V`, `±10 mV`, `±50 mV`
  - cleanup output off / open all / closed channels nil
- Direct contact approach continuation with user-specified parameters:
  - `+1.0 Z` coarse step
  - `100` max attempts
  - valid window `5e-10 A < |I| < 5e-8 A`
  - final over-current trim using `-0.25 Z` steps

## Reporting pattern

Keep user-facing Telegram updates concise:

- For a running approach: parameters, initial/current read, process id, summary path.
- For a completed resistance check: key currents, paired differential resistance, contact classification, direct cleanup evidence.
- Avoid per-step approach spam unless explicitly requested.
