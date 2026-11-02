# Direct contact check when PUDA protocol runner duplicates START — 2026-06-13

## Trigger

Use this only as a fallback when a normal `puda protocol run` contact check fails before executing commands with a START error like:

```text
START command failed for machine keithley-707b: cannot start, <same-new-run-id> is currently running
```

or the same pattern on `keithley-2450`, while read-only `puda machine state` shows the machines are idle or recoverable.

This is not the default ViPSA operation path. Prefer normal PUDA protocols first.

## What happened

A low-bias contact check protocol failed at START. The 707B accepted/entered the new run, then reported `RUN_ID_MISMATCH` with the exact same run ID as currently running. Retrying the same `puda protocol run` repeated the problem and left a transient active hold. `puda machine reset keithley-707b` cleared the matrix; `puda machine reset keithley-2450` may time out while still leaving state idle.

A direct NATS command transaction succeeded when it:

1. Reset/cleared stale holds where possible.
2. Used core NATS publish rather than JetStream publish for commands.
3. Sent `start` to `keithley-2450` and `keithley-707b`.
4. Treated `RUN_ID_MISMATCH` where the message contains the *same* current run ID as a duplicate-start acknowledgement, not as proof the machine is unusable.
5. Sent queued commands under that run ID.
6. Sent `complete` and verified final states.

## Command sequence for a 10 mV contact check

Under one fresh `run_id`:

1. `keithley-2450.start` immediate
2. `keithley-707b.start` immediate
3. `keithley-2450.set_output(enabled=false)` queue
4. `keithley-707b.connect_keithley_smu()` queue
5. `keithley-2450.hold_voltage_measure_current(voltage=0.01, current_compliance=1e-6, settle_s=0.2, read_count=3, reset=True)` queue
6. `keithley-2450.set_output(enabled=false)` queue
7. `keithley-707b.open_all()` queue
8. `keithley-707b.get_closed_channels()` queue
9. `complete` immediate for both machines

Subscribe before publishing to:

```text
puda.<machine>.cmd.response.immediate
puda.<machine>.cmd.response.queue
```

Publish to:

```text
puda.<machine>.cmd.immediate
puda.<machine>.cmd.queue
```

Use the same payload shape as the manual jog panel helper: header with `version`, `message_type=command`, `user_id`, `username`, `machine_id`, `run_id`, timestamp; command with `name`, `params`, `step_number`, `version`, `machine_id`.

## Interpretation/reporting example

A successful fallback 10 mV read returned three pA-scale points around `6.85e-11` to `6.96e-11 A`; final current `6.87e-11 A` gives apparent resistance around `146 MΩ`. Report this as **not in contact / very weak contact** relative to the 10–100 nA contact target, not as healthy contact.

Always report cleanup:

- Keithley output off
- 707B `open_all`
- `get_closed_channels` result `nil`
- `keithley-2450` and `keithley-707b` idle with `run_id: null`

If a non-electrical machine such as `stage` or `light` is in `error`, mention it separately but do not conflate it with electrical cleanup if the electrical path is safe.

## Pitfalls

- Do not keep retrying the identical failed `puda protocol run`; it can recreate the same duplicate-start active hold.
- Do not use JetStream publish for this fallback if duplicate command delivery is suspected; core `nc.publish` was the successful path.
- Do not proceed to DCIV/pulsing after this fallback if the contact check is pA-scale; ask whether to approach further.
- Do not save ephemeral run IDs in user-facing summaries or persistent skill text.
