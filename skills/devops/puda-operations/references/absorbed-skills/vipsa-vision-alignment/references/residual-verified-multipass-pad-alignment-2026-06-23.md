# Residual-verified multi-pass pad alignment

Use this when a standard ViPSA pad-centering move leaves a significant residual offset after the verification image.

## Lesson

The nominal pad-alignment multiplier (currently often 25 native Zaber steps per pixel) is only a first-pass estimate. Always recapture and redetect after the move. If residual is still large, do a bounded second correction rather than declaring alignment done or blindly repeating the same nominal correction.

## Recommended pattern

1. Capture camera 1 with lights on.
2. Detect nearest dark pad in the 900×900 center ROI.
3. Apply the standard native Zaber correction.
4. Recapture and redetect.
5. If residual distance is still above tolerance (for example >10 px), estimate the observed response from the first move:
   ```text
   response_x_px_per_native = (offset_after_x - offset_before_x) / move_x_native
   response_y_px_per_native = (offset_after_y - offset_before_y) / move_y_native
   ```
6. Compute a second correction from the measured response, with conservative clamps and correct sign.
7. Recapture again and report final residual offset and images.
8. If the second correction is still outside tolerance, do not stop early: continue a small bounded empirical loop using the most recent move response, especially on Y where backlash/nonlinear response can require several corrections. Clamp each additional correction (for example 800–1800 native steps depending on residual), recapture after every move, and stop once residual is within tolerance or the residual stops improving.

## Session example

A first pass started at about (+10.4 px, +20.0 px), moved Zaber X +261 and Y -500 native, then verified a residual of about (-3.3 px, +46.2 px). A second empirical correction of X -62 and Y +881 native reduced the residual to about (+0.17 px, +5.10 px). This demonstrated the importance of verification and bounded second-pass correction.

## Reporting

Use 🎯 and report:
- initial offset and move
- post-move residual
- any second correction
- final residual
- final annotated image
- final `light`/`zaber` idle verification
