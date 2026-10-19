# Keysight single-SET / 100-read retention check (2026-06-29)

Use this reference when the user asks for a quick pulsed retention measurement on the current ViPSA device using the Keysight SMU.

## Proven live recipe

Requested test:

- SMU: `keysight-b2902b`
- Route: DUT connected through `keithley-707b.connect_keysight_smu()`
- Stress: one SET pulse at `+0.8 V`
- Reads: `100` subsequent pulses/reads at `+0.1 V`
- Compliance: `1e-6 A` for both SET and reads
- Pulse/read width: `50 ms`
- Voltage list shape: `[0.8] + [0.1] * 100`
- Driver command: `keysight-b2902b.run_voltage_pulse_train(voltages=..., current_compliance=1e-6, pulse_width_s=0.050, reset=True)`

Execution sequence:

1. Turn lights off before electrical work if they may be on.
2. Start `keysight-b2902b` and `keithley-707b` under the same run id.
3. `keysight-b2902b.set_output(enabled=false)`.
4. `keithley-707b.connect_keysight_smu()`.
5. Run the 101-point pulse train in one `run_voltage_pulse_train` call.
6. Parse exactly one current per voltage point; expect 101 currents.
7. Save CSV with row 0 as `set_pulse` and rows 1–100 as `read`.
8. Plot read index vs `|I|` at `0.1 V` on log scale.
9. Cleanup: `keysight-b2902b.set_output(false)`, `keithley-707b.open_all()`, `get_closed_channels()`; expected safe response is `result: "nil"`.
10. Complete both machines.

## Direct-NATS reliability notes

During the NATS advertised-route outage pattern, protocol-first may be blocked. If direct fallback is authorized/needed:

- Prefer `nats://100.109.131.12:4224` first for Keysight direct control in this pattern.
- Use one NATS connection for the whole run and avoid depending on `flush()` for correctness; subscribe first, publish, then wait for matching responses by `machine_id`, `run_id`, command name, and step.
- Set a long `ping_interval` (for example 120 s) to avoid `nats.py` `_process_pong InvalidStateError` during multi-step waits.
- Persist response messages incrementally (`responses.jsonl`) so partial evidence survives if the wrapper times out.

## Stale-run recovery

If `keysight-b2902b.start` fails with `RUN_ID_MISMATCH` and reports an old run id currently running:

1. Publish `complete` for that exact old run id to `keysight-b2902b`.
2. Also publish `complete` for the same old run id to `keithley-707b` if the previous attempt coordinated both machines.
3. Retry the retention run with a fresh run id.

Do not send the pulse train until both machine START responses are successful for the fresh run id.

## Interpretation wording

For this test, report retention from the low-bias read sequence, not from the SET-pulse current alone. If the reads remain pA/sub-nA and hundreds of MΩ after the SET pulse, say no strong retained filament was observed under the requested pulse condition. Include:

- SET-pulse current
- first and last read current/resistance
- median/min/max absolute read current
- returned-current count vs expected count
- cleanup verification
- CSV and plot paths
