# Grid resume current-device handoff and Z-policy (2026-06-25)

Use this when resuming a ViPSA substrate grid DCIV→randomized-pulse campaign from the currently positioned device after a manual approach was already completed.

## Pattern

- If the user says to continue from **this/current device** after manual Z positioning/approach, do **not** automatically run the normal grid pre-travel sequence on that first handoff device.
- Preserve the current Zaber/stage position and reuse the verified manual approach artifact if available.
- Record the handoff explicitly in the device summary:
  - no initial stage or Zaber move
  - no initial alignment or re-approach
  - copied/manual approach status, final current, net Z, final stage position, and source summary path
- Start the requested DCIV/pulse sequence from that handoff state, with the usual electrical cleanup after measurement.

## Normal next-device Z policy

For subsequent devices in the same grid continuation, the established mechanical sequence is:

1. `stage.move_z_by(-60)` safe retract before X/Y travel.
2. Move Zaber X/Y to the next device target.
3. `stage.move_z_by(+30)` pre-approach return.
4. Run alignment/contact approach.
5. After DCIV/pulse cleanup, do **not** add an immediate Z retract solely because measurement ended; the next Z movement is the next device's `-60` safe retract.

When the user asks "what are the pre-approach and post-measurement Z movements currently," answer with both the normal next-device policy and any special first-device handoff exception.

## Approach parameters to report

Report both coarse and trim/fine steps, because the user may mean either by "step size":

- Running grid approach default in this continuation:
  - forward approach: `+0.5` Z steps
  - trim/backtrack: `-0.25` Z steps
  - fine forward: `+0.25` Z steps
  - example read gate: `0.1 V`, `100 nA` compliance, target `0.5–10 nA`
- If reusing a manual approach, report its actual saved parameters instead of the grid default. In the 2026-06-25 S2 handoff, device 24 reused a manual approach with:
  - coarse step `+1.0`
  - fine/trim step `0.25`
  - final net Z `-5.0`
  - final stage Z `85`

## Pitfall

Do not collapse the handoff-device behavior and subsequent-device behavior into one answer. The first resumed device may intentionally skip `-60/+30` and approach, while later devices use the normal grid movement policy.