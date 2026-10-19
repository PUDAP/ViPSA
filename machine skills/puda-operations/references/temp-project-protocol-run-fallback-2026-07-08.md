# Temporary PUDA project fallback for one-off machine protocols

Use this when a simple protocol command must run (for example `light.turn_off`) but the expected project directory is missing or the current working directory has no `puda.config`.

## Pattern

1. Confirm the target machine is reachable with a read-only command if possible:
   ```bash
   timeout 5 puda machine state light
   puda machine commands light | head
   ```
2. Create a temporary project directory instead of blocking on a stale/missing remembered project path:
   ```bash
   rm -rf /tmp/puda-light-run
   mkdir -p /tmp/puda-light-run
   cd /tmp/puda-light-run
   puda init . --name light-run --description temporary-light-control
   ```
3. Generate a full-metadata protocol JSON. Use the temp `project_id` from `project.md`; use `user.user_id` and `user.username` from `puda config list` if needed. Include a fresh `protocol_id`.
4. Validate and run from inside the temporary project directory:
   ```bash
   puda protocol validate --file /tmp/vipsa_light_off.json
   puda protocol run --file /tmp/vipsa_light_off.json --nats-servers nats://bears:4222,nats://bears:4223,nats://bears:4224
   timeout 5 puda machine state light
   ```
5. Report the command response and final machine state.

## Notes

- This is a fallback for operational continuity, not the normal preferred path when the real ViPSA project directory is available.
- Avoid dumping binary files such as `puda.db` while inspecting a temporary project; list specific text files only.
- Newer PUDA CLI builds may not expose the older `puda env ...` command group. If so, use `puda config list`, machine state/commands, and an explicit `--nats-servers` override rather than treating the missing env command as a hardware blocker.
