# Temp-project Stage-Z move and PUDA CLI update pattern (2026-07-25)

## Trigger

Use this note when a terse ViPSA request combines:

- updating PUDA CLI / PUDA skills;
- a simple Stage-Z jog; and
- a camera-1 snapshot.

## Reusable lessons

1. **PUDA CLI update is interactive by default.** In non-interactive Hermes tool sessions, plain `puda update` can abort at `Would you like to install it?`. Use:
   ```bash
   printf 'y\n' | puda update
   puda --version || puda version
   ```
   Always verify the version changed before reporting the CLI update.

2. **`puda skills update` may legitimately report no project skills.** Report this as a completed skills-update check rather than as a failure:
   ```text
   No project skills to update.
   Install project skills with npx skills add <package>
   ```

3. **If `/home/vipsa/vipsa-puda-project` is missing, use a temporary PUDA project for simple one-off commands.**
   ```bash
   TMP=/tmp/vipsa_stage_z_$(date +%s)
   puda init "$TMP" --name "vipsa-stage-z" --description "Temporary PUDA project for ViPSA stage Z move"
   ```
   Generate full-metadata protocol JSON from `$TMP/puda.config`, run from `$TMP`, and pass the known ViPSA NATS override when needed:
   ```bash
   NATS='nats://100.109.131.12:4222,nats://100.109.131.12:4223,nats://100.109.131.12:4224'
   puda protocol run --file "$TMP/move_z_up_100.json" --nats-servers "$NATS"
   ```

4. **Stage-Z verification sequence remains unchanged.** For a Z-only jog, run `stage.move_z_by(height=<signed steps>, feedrate=450)`, then a separate `stage.get_current_position()` protocol, then a final bounded `puda machine state stage`. Report the signed move, numeric Z readback if present, and `idle/run_id:null` state.

5. **Camera-1 snapshot can use local RTSP if preflight succeeds.** Probe `rtsp://127.0.0.1:8554/camera1`; if healthy, use local Linux `ffmpeg` to capture one JPEG. Wrap light control in a cleanup path: `light.turn_on()` before snapshot, `light.turn_off()` afterward, then verify final `light` state.

## Evidence from this session

- `puda update` with `printf 'y\n'` upgraded `0.0.34 -> 0.0.36` and version verification returned `0.0.36`.
- `puda skills update` completed with “No project skills to update.”
- Stage move protocol `move_z_by(height=100, feedrate=450)` succeeded; separate readback returned `[0, 0, 250]`; final stage state was `idle`, `run_id:null`.
- Camera 1 local RTSP preflight returned H.264 `1920x1080`; snapshot wrote a non-empty JPEG; light off cleanup succeeded with final `idle`, `run_id:null`.
