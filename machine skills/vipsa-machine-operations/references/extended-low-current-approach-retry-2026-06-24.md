# Extended low-current approach retry after grid pause (2026-06-24)

## Context
During an 8x8 ViPSA grid run, the user paused the active runner and requested repeated device-22 contact-approach retries while changing the lower contact threshold and the Z step size.

## Durable workflow lessons

- When changing the approach lower threshold mid-run, patch the continuation runner constant and also use the new threshold in any standalone/manual retry script. Verify the patched constant before reporting it as active.
- Keep the grid runner paused/killed while manual retry approaches are being performed. Treat SIGTERM completion notifications from the killed runner as stale buffered output, not as active-run failure.
- For manual retry approaches from an already-positioned device, do not redo full grid measurement. Reuse the current device position and run only:
  1. cleanup: Keithley output off, Keysight output off, 707B open_all/get_closed_channels;
  2. confirm/record stage and Zaber positions;
  3. route DUT to Keithley;
  4. bounded approach loop with the requested threshold/step/attempt count;
  5. cleanup and final idle-state verification.
- If the user asks for "another 50 step attempts", interpret this as an additional bounded continuation from the current stage Z, not a restart from the original device handoff height, unless they explicitly say to reset/retract/reposition.
- If the user changes step size for a single attempt, apply it only to that continuation script and report it explicitly. In this session, `+1.0 Z` step attempts were used after earlier `+0.5 Z` attempts.
- If the approach remains near ~1e-10 A after many forward Z steps and below the new lower threshold, report `no_contact_after_extra_N` honestly; do not declare success just because an older lower threshold would have accepted the current.
- If a background/manual approach process is killed after apparent stage-control stall, immediately recover safely: abort stage motion if needed, read stage position, turn SMU outputs off, open/verify the 707B, then decide whether to continue from the verified current Z. Do not trust the process log's `net_z` alone; use live stage position readback.

## Reporting standard
Keep the update concise and include:

- lower/upper threshold and voltage;
- step size and number of added attempts;
- start/final stage position;
- final current and whether it is below/in/above the requested window;
- 707B closed-channel result (`nil` expected);
- final idle/null-run verification for Keithley, 707B, Keysight, stage, Zaber, and light.
