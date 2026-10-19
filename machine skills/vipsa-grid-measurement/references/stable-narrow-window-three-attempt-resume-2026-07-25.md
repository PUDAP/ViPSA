# Stable narrow-window contact gate with a third coarse retry (2026-07-25)

Use this pattern when a live ViPSA grid is paused/restarted and the user changes both the contact window and retry policy.

## Policy encoded

- Contact read: `10 mV`.
- Target window: `1–10 nA`.
- “Stable contact” means three consecutive low-bias reads inside the window at the same Z position.
- Attempt 1: bounded approach, `+0.5` Z step.
- Attempt 2: bounded approach, `+0.5` Z step.
- If both fail stability/window, attempt 3: bounded approach, `+1.0` Z step.
- DCIV/pulses are blocked after attempt 3 if contact is still unstable or outside the window.

## Critical mechanical invariant — later correction

The original session implementation treated each attempt as a separate baseline and retracted its full positive `net_z_steps` before retrying. The user later corrected this policy: **subsequent approach attempts must continue from the verified current Z without a gross `-50` or attempt-sized inter-attempt retract.**

Current rule:

1. Save `net_z_steps` separately for every bounded block and preserve cumulative Stage-Z readback.
2. After a low-current/no-contact block, start the next authorized block from the current verified Z; do not insert a generic gross retract.
3. Keep minimum-step negative trims for over-current/overshoot safety.
4. Before any X/Y travel, perform and verify a dedicated safe travel retract large enough for the accumulated approach depth.
5. If the reply chain discusses a different device than live Zaber X/Y identifies, stop before Z motion and resolve the target mismatch.

This separates retry continuity from lateral-travel clearance: no unnecessary retract between approach blocks, but no X/Y travel at accumulated approach depth.

## Restarting an interrupted next device

- Stop runner and reporter, cleanup outputs/routes, and preserve the interrupted folder by archiving it with a timestamp.
- Resolve the device’s nominal absolute X/Y from `grid_positions.csv`, then apply its saved alignment correction to recover the aligned absolute X/Y.
- Use a verified safe Z clearance before X/Y travel.
- Do not blindly restore the prior device’s deep retry Z at the destination. Restore only a verified safe pre-contact or previously validated destination-device Z, then perform a fresh low-bias check/approach under the new window.
- Preserve the old interrupted folder separately; create fresh `device_N` artifacts for the restarted policy.

## Stable-contact implementation

At the terminal approach position:

1. If the first read is inside the window, take two more reads without moving Z.
2. Set `stable_contact_confirmed=true` only when all three absolute currents lie in the window.
3. Downstream gates must use `stable_contact_confirmed`, not merely `final_abs_current_a` or an `in_window` status string.
4. Save `stability_reads_abs_a`, step size, max attempts, net Z, and stage readback in each attempt artifact.

## Per-device reporting

A long runner should emit one machine-readable `device_finished` event per device. A stateful reporter should parse `summary.json` and immediately send a concise status after each device:

- stable contact current/window and attempt used;
- whether DCIV ran, SET/RESET status;
- pulse count/failure;
- skipped reason when gated;
- plot attachment when present.

Do not infer completion from `DONE.json` alone; interrupted or error paths may also write it.

## Validation before launch

- Compile the continuation runner.
- Assert constants, start boundary, third-attempt step, stability-read count, **absence of gross inter-attempt retracts**, cumulative/net-Z accounting, a verified safe retract before X/Y travel, and the pulse fallback branch.
- Archive the interrupted restart-device folder.
- Start as a tracked background process and verify a fresh `device_start` event for the intended boundary.
