# Stage edge coordinate frames and historical Z reconstruction

## Durable rule

Treat `stage.get_current_position()` as a **tracked edge-coordinate readback**, not automatically as an absolute physical Z coordinate. Restarting/reinitializing the stage edge can reset its reported origin to zero without moving the hardware.

## Historical-Z questions

When asked what Z height was used for an earlier device/test:

1. Identify the exact run/device from image geometry, Zaber position, timestamps, and run artifacts.
2. Read that run's `stage_position`, `stage_before`, and `stage_after` metadata.
3. Check whether a stage-edge restart/reinitialization occurred between the compared runs.
4. If the coordinate frame changed, reconstruct physical-relative Z by summing verified signed moves from the last common physical baseline. Report both:
   - the run-local tracked Z;
   - the reconstructed physical-relative Z, with its baseline and confidence.
5. Never compare `Z=50` after an edge restart directly with `Z=200.5` or `Z=240.5` from before that restart as if they shared an origin.
6. If the chain cannot be reconstructed unambiguously, say the run-local tracked value is known but absolute cross-restart physical Z is not.

## Reporting language

Use phrases such as:

- `Run-local tracked Z: 50 (edge origin had been reset).`
- `Physical-relative height versus the pre-restart baseline: +50 verified steps.`
- `Cross-restart absolute Z cannot be asserted from this readback alone.`

This distinction is especially important after all-edge resets and before answering historical questions from camera images.