# Zaber Manual Jog and Position Recording

Use this reference when the user wants to manually jog the ViPSA Zaber X/Y stages or record the current X/Y position.

## Manual jog UX

When the user asks for manual jog buttons, present a concise interactive choice set with a safe default native-unit step size. A good Telegram button set is:

- `⬅️ X -100`
- `➡️ X +100`
- `⬆️ Y +100`
- `⬇️ Y -100`

Also accept typed commands such as:

```text
X +500
X -50
Y +100
Y -25
pos
step 25
```

For jog moves, use native/controller units unless the user explicitly requests millimetres:

```json
{"name": "move_x_by", "machine_id": "zaber", "params": {"distance": -100, "units": null}}
{"name": "move_y_by", "machine_id": "zaber", "params": {"distance": 100, "units": null}}
```

After each jog, report:

- button/command selected
- exact PUDA method and signed distance
- move status
- final Zaber machine state
- position readback if available

## Position readback parsing pitfall

`zaber.get_current_position()` returns its X/Y payload directly under `response.data`, not under `response.data.result`.

Examples observed:

```json
"data": {"x": 601289, "y": 1017639}
```

for native/default units, and:

```json
"data": {"x": 59.659142968750004, "y": 100.96886953125001}
```

for `params: {"units": "mm"}`.

Do not parse only `data.result` for Zaber position; that will incorrectly appear as `null` even when the readback succeeded.

## Recording current position

When the user says to record the current Zaber position:

1. Verify `zaber` state is idle.
2. Run `get_current_position` with no `units` or `units: null` to capture native/default units.
3. Run `get_current_position` with `units: "mm"` to capture millimetres.
4. Record both in the active PUDA project's `project.md` under `## Logs` if the user asked to record/save the position.
5. Report both native and mm positions plus final `zaber` state.

Do not store one-off position values in Hermes memory; they are experiment/session state and belong in `project.md` or the user's chosen experiment log.
