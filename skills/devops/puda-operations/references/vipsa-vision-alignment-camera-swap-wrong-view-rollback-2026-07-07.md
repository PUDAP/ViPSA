# ViPSA alignment camera swap / wrong-view rollback (2026-07-07)

## Trigger
User asks for terse `align`; camera streams may have been swapped or renamed, and previous camera assumptions are unreliable.

## What happened
- Alignment runner first used `camera1` RTSP paths; image showed the motor/stage assembly rather than the device/contact-pad microscope view.
- Detector locked onto a non-pad feature near the right side and commanded Zaber corrections.
- After user said cameras were swapped, runner retried with `camera2`, but the opened stream still showed the same motor/stage view.
- Detector again locked onto the same non-pad feature. The Zaber moves were reverted by summing the applied correction commands and commanding the inverse.

## Durable lesson
For ViPSA alignment, **camera name is not proof of view**. Before any Zaber correction:

1. Capture a preflight frame from the intended camera stream.
2. Verify the frame is the microscope/device contact-pad view, not the macro/motor/stage assembly.
3. Verify the selected contour is a plausible contact pad near the expected probe/device area, not a wire, motor label, screw, edge, or light reflection.
4. If view or detection is wrong, stop before motion, attach the overlay, and ask the user to fix/select the correct camera stream.

## Motion rollback pattern
If an erroneous alignment move was already commanded:

1. Sum every successful relative Zaber move issued by the alignment attempt.
2. Command the inverse total move using native units.
3. Verify `zaber` returns `idle`, `run_id: null`.
4. Turn lights off unless user requested otherwise and verify `light` idle.
5. Report the failed detection, applied moves, rollback moves, and attach the bad overlay.

## Additional guard
If the detected offset remains nearly unchanged after a large Zaber correction, treat this as a sign that the selected feature is not coupled to the device/pad view or the wrong stream is being processed. Stop and rollback rather than performing another pass.