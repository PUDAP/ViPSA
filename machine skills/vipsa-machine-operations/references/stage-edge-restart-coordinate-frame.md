# Stage edge restarts and coordinate continuity

The OpenFlexure stage position reported by `get_current_position()` is software-tracked state, not an independent physical encoder reading. Restarting the stage edge can reinitialize that tracked coordinate to `[0,0,0]` without moving the hardware.

For any post-restart jog:

1. Call `get_current_position()` before the move.
2. Execute the exact signed `move_z_by` request in one lifecycle-managed run.
3. Call `get_current_position()` afterward and verify the signed delta.
4. Describe both readings as belonging to the restarted edge coordinate frame.
5. Never add the post-restart coordinate to an earlier pre-restart value or report it as continuous absolute physical Z.

The within-run signed delta is valid evidence of the requested jog; coordinate continuity across an edge restart is not.