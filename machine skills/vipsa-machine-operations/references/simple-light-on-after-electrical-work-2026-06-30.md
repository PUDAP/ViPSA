# Simple light-on after electrical work (2026-06-30)

## Trigger
User gives a terse lights-only request such as `turn on lights` after an electrical measurement/cleanup sequence.

## Verified pattern
Use protocol-first control, not a camera/snapshot workflow and not direct/raw NATS unless protocol routing fails.

1. Generate a full-metadata one-command PUDA protocol in the ViPSA project with:
   - `machine_id: light`
   - `name: turn_on`
   - `params: {}`
2. Validate it:
   ```bash
   puda protocol validate --file <protocol.json>
   ```
3. Run it from `/home/vipsa/vipsa-puda-project`:
   ```bash
   puda protocol run --file <protocol.json>
   ```
4. Verify the light edge has completed:
   ```bash
   timeout 5 puda machine state light
   ```

## Expected success evidence
- Command response status `success`.
- `response.data.result: true` from `light.turn_on()`.
- Final `puda machine state light` reports `state: idle` and `run_id: null`.

## Reporting
Keep the Telegram reply terse:

```text
Lights are on.

Verified:
- light.turn_on() succeeded with result: true
- Light state: idle, run_id: null
```

Do not attach camera media or inspect visual brightness unless the user explicitly asks for a snapshot/image or asks whether the light is visibly on.