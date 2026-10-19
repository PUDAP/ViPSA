# Exact ViPSA jog chains and PUDA Direct lifecycle safety

Use this for explicit commands such as “stage Z down 100, then Zaber X −5000,” optionally followed by a camera capture or electrical test.

## Execution pattern

1. Read live machine states and current stage/Zaber positions.
2. Put electrical hardware in a safe state before motion: Keithley output off and 707B `open_all`. Lights default off unless illumination is immediately needed, but preserve a user's explicit latest light command across mechanical-only jogs; do not silently send `turn_off` after the user intentionally turned illumination on. Electrical measurements still follow their own illumination policy.
3. Preserve the user's sign and axis exactly:
   - stage down `N` → `stage.move_z_by(height=-N, feedrate=450)`
   - stage up `N` → `stage.move_z_by(height=+N, feedrate=450)`
   - Zaber X `N` → `zaber.move_x_by(distance=N, units=None)`
4. For one isolated jog, prefer `puda machine run` **only when the edge accepts lifecycle-free commands**. Some ViPSA edges reject it with `Send START command to start a run before sending commands`; that rejection means the jog did not occur. Do not repeat blindly or guess the position. Fall back immediately to a lifecycle-managed one-command protocol or a Direct context that owns the machine, then obtain fresh before/after readbacks. For an ordered multi-machine chain, use one PUDA protocol or one Direct run context so order and cleanup are explicit.
5. Read back after every move and verify `after - before` equals the requested signed delta. Do not report motion from a successful command response alone.
6. If a camera capture follows, probe the exact RTSP source before illumination, finish all motion first, then light on → capture → light off in `finally`.
7. End with outputs off, 707B closed channels `nil`, lights off, and relevant machines idle/null.

## Direct machine-set pitfall

A helper may address more machines than the visible task. For example, the shared ViPSA `cleanup(dp)` helper addresses Keithley 2450, Keysight B2902B, and Keithley 707B. If a Direct context was opened without every machine touched by that helper, a command can start an untracked machine run that the context does not complete, leaving `state=active` with a stale `run_id`.

Use one of these safe options:

- Include every machine touched by the helper in the Direct machine set; or
- Replace the broad helper with task-specific cleanup that only addresses machines owned by that context.

After the context exits, inspect every touched machine. If one is unexpectedly active, first verify its output is off, then use the established PUDA reset/recovery path and recheck for `idle`/`run_id:null`.

## Interrupted-operation rule

If execution is interrupted before the movement tool returns, do not assume the requested jog occurred and do not automatically resend the same signed move. On the next request:

1. Inspect the machine lifecycle state. An interrupted Direct context can leave `state=idle` with a non-null run ID even though the physical move completed.
2. Attempt lifecycle cleanup only when it is valid for the recorded run. A `complete` response of `run ... not active` cannot prove whether motion occurred; it may also transition the published state to `error` with `run_id:null`.
3. Use a lifecycle-managed **read-only** Direct run to call `get_current_position()` and establish the fresh numeric baseline. Do not use a move runner merely to obtain its `before` field.
4. Compare that baseline with the last verified pre-command position. If it already differs by the requested signed amount, treat the interrupted jog as completed and do not apply a duplicate move unless the user explicitly asks for an additional jog.
5. Verify the read-only context returns the machine to `idle`/`run_id:null`, then report what was physically verified rather than what the interrupted process returned.

Never silently carry an unverified prior jog into a new chain.
