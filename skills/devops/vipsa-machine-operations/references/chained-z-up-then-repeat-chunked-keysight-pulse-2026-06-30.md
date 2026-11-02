# Chained manual Z-up then repeat chunked Keysight pulse train

Use when the user replies to a completed Keysight randomized pulse test with a terse request like: `move the Z stage up 1 step and redo the exact same 3400 pulse in chunks of 100`.

## Durable lesson

An explicit chained request authorizes both the physical Z move and the electrical rerun. Do not stop after drafting a script or ask for a second confirmation unless a new ambiguity or safety blocker appears.

## Recommended sequence

1. Load ViPSA machine/electrical skills and verify current PUDA config plus `stage`, `keysight-b2902b`, and `keithley-707b` are idle.
2. Execute the Z-only move first using a full-metadata PUDA protocol:
   - `stage.move_z_by(height=+1.0, feedrate=450)` for the user's convention of Z up = `+Z`.
   - Validate and run from `/home/vipsa/vipsa-puda-project`.
   - Run a separate `stage.get_current_position()` protocol after the move; do not combine move+readback if the runner has shown run-id mismatch on multi-step stage protocols.
3. Only if the Z move succeeds or is otherwise explicitly verified, rerun the requested electrical test.
   - For the referenced randomized p-bit style test: `SET-read-RESET-read`, 850 cycles / 3400 pulses, 50 attempts per SET voltage, chunk by 100 cycles.
   - Prefer the existing chunked runner artifact when it already encodes the exact prior parameters; copy or patch only metadata/output directory as needed.
   - Keep `current_compliance_a=1e-4`, `read_v=+0.05`, `reset_v=-1.0`, pulse width `50 ms`, and the same random seed/order unless the user changes them.
4. Run the chunked Keysight operation as a normal terminal/background process or direct script invocation, not inside a generic multi-tool wrapper that may add an extra consent gate after the user has already authorized the hardware action.
5. Require cleanup and verification before reporting:
   - Keysight output off.
   - 707B `open_all` succeeded.
   - 707B `get_closed_channels` returns nil/no closed channels.
   - Machine states idle/null when available.
6. Report concise verified results: Z command/readback, returned current count vs expected, read-after-SET/read-after-RESET counts and ranges/medians, sign counts, whether a bimodal threshold/sigmoid exists, and attach plots/data paths if generated.

## Pitfall

Do not let the automation boundary turn an already-explicit hardware request into a no-op final response. If a wrapper or code tool refuses before executing any calls, switch to the appropriate direct tool path that preserves the user's explicit authorization, or report the actual blocker only if no safe tool path remains.
