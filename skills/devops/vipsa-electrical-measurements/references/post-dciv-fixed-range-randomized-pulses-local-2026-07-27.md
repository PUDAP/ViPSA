# Post-DCIV fixed-range randomized pulses on current ViPSA device (2026-07-27)

Use this reference when a user has just run a DCIV sweep on the current contacted device and then asks for a randomized pulse measurement on **this device**.

## Trigger

- User requests randomized pulse measurement immediately after a verified DCIV on the same current device.
- DCIV showed a clear SET-like positive-branch transition but weak/no RESET.
- The system is using local ViPSA PUDA/NATS recovery or project defaults may still point at stale `bears` endpoints.

## Recommended workflow

1. Preserve the current-device identity from the reply chain and latest verified run folder; do not re-approach or move unless requested.
2. Use the Keysight/707B pulse path for `SET-read-RESET-read` trains.
3. If the DCIV has an estimated `Vset`, choose randomized SET levels around it, including values below it. Example from this session:
   - DCIV SET jump: `+0.85 V -> +0.90 V`.
   - Pulse SET range chosen: `0.60–1.10 V` in `0.05 V` steps.
4. Make pulse-count semantics explicit:
   - `1000` physical pulses = `250` four-pulse trains.
   - Train shape: `SET(Vset_candidate) -> read(+0.1 V) -> RESET(-2.0 V) -> read(+0.1 V)`.
5. Chunk execution, e.g. `100` physical pulses / `25` trains per Keysight command, and save the plan before hardware execution.
6. Monitor each chunk for read-near-compliance and stop if read pulses approach compliance; otherwise continue to the requested budget.
7. Cleanup at the end or on error: Keithley output off, Keysight output off, 707B `open_all`, verify `get_closed_channels`/idle states.
8. Plot/analyze from saved CSVs. If the measurement succeeds but plotting/imports fail, do **not** rerun hardware just to plot; rerun analysis with a plotting-capable ephemeral environment, e.g. `uv run --with nats-py --with matplotlib --with pandas python <runner.py>` or a CSV-only plotting helper.

## Interpretation pattern

If all randomized SET voltages switch with perfect separation:

- Report `P(switch)=1.0` across the tested range.
- State that the tested range is above threshold under this pulse protocol.
- Do **not** over-interpret a logistic fit whose V50 falls outside/below the tested range; say the transition likely lies below the minimum tested SET voltage.
- Report read-state medians and ROC threshold rather than just the probability table.

Concrete example outcome:

```text
1000/1000 physical pulses completed = 250 trains
SET levels: 0.60–1.10 V, 50 mV step
RESET: -2.0 V
read: +0.1 V
pulse width: 2 ms
compliance: 100 µA
read-near-compliance hits: 0
median read-after-SET: ~9.05 nA
median read-after-RESET: ~5.7 nA
ROC threshold: ~7.9 nA
P(switch): 1.0 at every tested SET level
```

## Pitfalls

- Do not let missing Python packages (`nats`, `matplotlib`, `pandas`) convert a completed measurement into a failure. If rows were saved or the hardware command completed, recover post-processing separately.
- Do not report a meaningful sigmoid V50 if the tested voltages all saturate at `P=1`; the proper conclusion is that a lower SET-voltage range should be tested next.
- If local NATS recovery is active, explicitly set `base.SERVERS=['nats://127.0.0.1:4222']` or pass the equivalent override so imported historical runners do not reuse stale remote servers.
