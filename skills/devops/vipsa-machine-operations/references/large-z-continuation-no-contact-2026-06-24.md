# Large Z continuation after repeated low-current/no-contact approach

Context: paused grid/device-22 manual approach retries after earlier bounded attempts had ended below the soft contact threshold. The user asked for one more approach attempt with `max steps 100` after a previous `+1.0 Z` continuation ended at `stage z ~= 99.25` with current around `1.1e-10 A`.

Reusable pattern:

1. Treat the request as a continuation from the verified current stage Z, not as a full device restart or Zaber move.
2. Check for active/stale runner processes before starting so two approach loops do not fight over stage/SMU state.
3. Turn lights off before electrical approach unless explicitly requested otherwise.
4. Cleanup first: Keithley output off, Keysight output off, 707B `open_all`, `get_closed_channels`.
5. Connect DUT to Keithley, then loop:
   - read current at the established retry settings (`0.1 V`, `1e-7 A` read compliance in this session; keep current session constants unless user changes them),
   - if `lower <= abs(I) <= upper`, stop as in-window,
   - if `abs(I) > upper`, stop and run bounded minimum-step retract trim,
   - otherwise move stage `+Z` by the user-requested step size and log readback.
6. Persist the log after every read/move so partial state survives interruption.
7. Always cleanup afterward and verify `get_closed_channels == nil` plus `stage`, `keithley-2450`, and `keithley-707b` idle/null-run when possible.
8. Report no-contact honestly if the current remains below threshold after the requested max steps; do not run DCIV/pulsing automatically.

Concrete outcome that motivated this note:

- Additional attempt: `100` steps at `+1.0 Z` from `z ~= 99.25` to `z ~= 199.25`.
- Current stayed near `1.1e-10 A`, below the `5e-10–1e-8 A` contact window.
- Final status: `no_contact_after_extra_100_step1`.
- Cleanup verified: 707B closed channels `nil`; stage/Keithley/707B idle with `run_id: null`.

Reporting style: summarize only final status, start/final Z, net additional Z, final current vs threshold, cleanup/idle status, and log path. Do not paste every per-step read unless the user explicitly asks for the detailed log.
