# One-by-one protocol optimization after overforming / short-life failures (2026-06-30)

## Context

During an S1 8x8 ViPSA probabilistic-pulse grid run, early devices showed underwhelming lifetime and ON/OFF behavior. Several devices SET during DCIV but failed pulse lifetime early with `read_current_near_pulse_compliance` or `permanent_set_after_two_reset_recoveries`. The user asked to try protocol changes one by one to get higher ON/OFF ratio and longer life.

The important lesson is to treat this as an **adaptive safe-boundary optimization problem**, not a single large restart with many simultaneous changes.

## Observed failure pattern

Symptoms suggesting protocol-induced overforming / over-contact rather than uniformly bad devices:

- Approach often ended as `over_current` or `over_current_after_fine`, with final contact currents near `1e-7 A` even when the intended window was lower.
- Many DCIV sweeps showed very early SET-like jumps near `+0.02 V` or `+0.06 V`.
- Positive DCIV branches frequently hit SET compliance.
- Pulse tests then stopped early because read currents approached pulse compliance, or devices became permanently SET after reset recovery attempts.
- Some devices still completed full pulse budgets, so the substrate was not uniformly dead; the protocol/contact was a plausible contributor.

## Workflow pattern

When the user asks to improve lifetime/ON-OFF by trying protocol changes one at a time:

1. **Inspect the last completed devices before changing anything.**
   - Extract approach status/final current/net Z.
   - Extract DCIV path, Vset/Vreset detection, compliance-hit counts, max current.
   - Extract pulse count, stop reason, read-after-SET/read-after-RESET ratio, and probability summaries.

2. **Identify protocol-induced stress signals.**
   - Over-contact at approach.
   - Very early SET.
   - Compliance-limited DCIV branches before pulsing.
   - Pulse read currents near compliance.

3. **Apply only one class of change at a time at a device DONE boundary.**
   - Do not mix approach, DCIV, pulse reset, pulse width, and voltage-range changes in one restart unless the user explicitly requests a wholesale protocol rewrite.
   - Wait for current device `DONE.json`, then stop/cleanup/restart before the next physical device.

4. **Preserve the safe-boundary restart hygiene.**
   - Stop the active runner after the current device is done.
   - Force SMU outputs off.
   - `707B.open_all()` and verify `get_closed_channels == nil`.
   - Archive any incomplete next-device folder.
   - Prune `summary.partial.json` only for incomplete/non-DONE devices.
   - Restart as a tracked background process and verify a fresh next-device `summary.json`.

5. **Use an adaptive supervisor/poller if the user wants continuing optimization.**
   - Watch for new `device_XX/DONE.json` files.
   - Analyze the just-completed device.
   - If it fails lifetime/ON-OFF, patch exactly one further protocol category and restart at the next safe boundary.
   - If it looks good, keep the current protocol and do not continue tweaking.

## Example one-change sequence

A reasonable progression after overforming/short-life failures:

1. **Softer approach only**
   - Narrow target, e.g. `1e-9`–`5e-9 A`.
   - Reduce forward Z approach step, e.g. `0.25` instead of `0.5`.
   - Keep DCIV and pulse settings unchanged for this trial.

2. **Stronger pulse reset only**
   - If DCIV reset was already extended but pulse reset remains weaker, change only pulse RESET, e.g. `-1.0 V` → `-1.2 V`.
   - Keep SET voltage range, pulse width, and compliance unchanged.

3. **Gentler SET pulse stress only**
   - If pulse-reset strengthening still fails, reduce SET stress, e.g. max SET `1.0 V` → `0.8 V`.
   - Shorten pulse width, e.g. `10 ms` → `2 ms`.
   - Reduce chunk size, e.g. `500` pulses → `100` pulses, so failures are caught earlier.

## Implementation pitfalls

- **Serpentine order matters.** After row 0 device 8, the next physical device in an 8x8 serpentine traversal is device 16, not device 9. Restart logic must filter by `DONE.json` or traversal order, not naive numeric `device_number >= boundary` when continuing physically.
- **Do not confuse DCIV reset and pulse reset.** Extending DCIV reset to `-1.2 V` does not alter randomized pulse RESET if the pulse function still has `reset_v=-1.0`.
- **Do not overclaim a fix from one device.** Report the just-tested device metrics and whether the next single change is justified.
- **Do not archive completed folders.** Archive only incomplete/partial folders and preserve completed device summaries.
- **Log each adaptive change in `project.md`.** Include the trigger device, the one changed parameter category, and what remained unchanged.

## Reporting pattern

Keep the user-facing update concise:

- State the last device result and failure/success criterion.
- State the single active change now.
- State the next conditional change if this one fails.
- Include active runner/supervisor handles if relevant.
