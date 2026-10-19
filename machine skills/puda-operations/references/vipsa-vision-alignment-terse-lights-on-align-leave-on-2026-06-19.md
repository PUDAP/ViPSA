# Terse “turn lights on and align” workflow

When the user says a short request like “turn the lights on and align,” treat it as an active ViPSA alignment request with the lights intentionally left on afterward.

Recommended behavior:

1. Load/use the standard camera-1 contact-pad alignment workflow: light on, capture camera 1, 900×900 center ROI, dark-pad mask, nearest-pad contour, Zaber native-unit correction with the current multiplier (typically 25 steps/px), then recapture and verify residual.
2. Do not ask whether to leave the lights on; the phrase “turn the lights on and align” implies the final lamp state should remain on.
3. In scripts cloned from an “align then turn off” workflow, patch both the normal completion path and the `finally`/cleanup path to call `light.turn_on()` rather than `light.turn_off()`.
4. Verify final `light`, `zaber`, and relevant motion-machine states are `idle` with `run_id: null` after the final `turn_on` protocol.
5. Report concise alignment evidence: final residual pixel offset, Zaber correction(s), final machine states, final light state left on, and attach the final annotated image.

This prevents the common cleanup pitfall where an alignment script turns lights off in `finally` even though the user’s latest request explicitly asked for lights on.