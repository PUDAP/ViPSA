# Clear Stage holds and restart exactly one edge

Use when the user asks to clear Stage holds/stale lifecycle state and restart the ViPSA Stage edge.

## Procedure

1. Query `puda machine state stage` through the active ViPSA NATS cluster and identify the actual Stage edge process by **working directory and serial-device ownership**, not by the generic command line alone. All ViPSA edges may appear as `python3 main.py`.
   - Inspect candidate process CWDs under `/proc/<pid>/cwd`.
   - Use `fuser -v /dev/openflexture` (or the configured Stage serial device) to identify the process that owns the controller.
2. Before restart, clear active motion/lifecycle state through PUDA:
   - fresh run ID
   - `machine start stage`
   - `machine run stage abort_motion '{}'`
   - `machine complete stage`
   - require `idle` and `run_id: null`
3. Terminate the owning Stage edge process group, then verify the serial device has no owner before restarting. Do not kill every generic `main.py`; those may be the light, Zaber, or SMU edges.
4. Start one Stage edge from its own directory (`/home/amdm/workspace/ViPSA/stage`, normally `uv run main.py`) as a tracked long-lived process.
5. Verify readiness from edge logs: queue subscription, immediate-command subscription, and command metadata publication.
6. Run a harmless fresh lifecycle transaction containing only `get_current_position`, complete it, and verify:
   - command succeeds;
   - Stage is `idle`, `run_id: null`;
   - exactly one process owns the Stage serial device.

## Reporting

Report only the verified outcomes: abort/hold clear, edge restarted, single serial-device owner, read-only command success, and final idle/null state. A software position readback or GRBL command acknowledgment is not independent proof of physical mechanics.