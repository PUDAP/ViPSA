# Z increment + DCIV blocked by RUN_ID_MISMATCH

Use this when the user authorizes a combined mechanical/electrical action such as “move Z one step and run DCIV,” but the control layer rejects the motion.

## Key lesson

A combined request authorizes DCIV **after** the requested Z move, but the DCIV must remain conditional on the move actually succeeding. If the Z move is rejected by PUDA/edge run-state errors, no electrical sweep should be run.

## Failure pattern

In a follow-up to bounded DCIV forming with weak coupling, the user requested `+1.0` Z and another DCIV. The safe intended sequence was:

1. Move `stage.move_z_by(height=+1.0, feedrate=450)`.
2. Read back stage position.
3. Route DUT to Keithley.
4. Run a `10 mV` low-bias precheck with `1 µA` compliance.
5. Abort if near compliance/short-like; otherwise run the bounded forming/DCIV recipe.

Actual observed state:

- PUDA CLI path failed on NATS timeouts before motion.
- Direct raw-NATS reached the stage edge, but START/queue state returned `RUN_ID_MISMATCH`.
- No stage move was confirmed.
- No 10 mV precheck or DCIV stress should be considered executed.

## Reusable rule

For `Z move → DCIV` chains:

- Require a successful motion response and, when possible, a position readback before any electrical stress.
- Then require a non-stressing low-bias read precheck (`10 mV`, low compliance) before DCIV.
- If motion fails, the correct outcome is “blocked; no confirmed Z move; no DCIV executed,” not a fallback electrical run at the old contact.
- If cleanup/state verification is blocked by NATS, report cleanup as unverified instead of claiming a safe final state.

## User-facing wording

Prefer terse hardware-safe wording:

```text
Blocked — I did not successfully move Z or rerun DCIV.
No confirmed Z move. No confirmed electrical stress.
Reason: PUDA/NATS RUN_ID_MISMATCH before stage.move_z_by executed.
```
