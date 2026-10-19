---
name: puda-operations
description: "Operate PUDA CLI environments and edge machines: login/config checks, environment discovery, machine listing, machine state/control, and concise Telegram reporting."
---

# PUDA Operations

## Consolidated PUDA Lab/Machine Operations

This skill is the umbrella for day-to-day PUDA environment, lab automation, and machine-operation workflows. Narrow PUDA siblings have been folded here as labeled sections so agents load one operational playbook before touching hardware or experiment state.

### Machine Operations

Before operating a PUDA-connected machine, select the correct environment, list machines, inspect current state, and verify the machine identity. Prefer project/environment-aware `puda` commands over direct device access. For ViPSA/Zaber-related actions, preserve native-unit conversions, light/camera state, and machine-specific reference notes in `references/`.

### Lab Automation

Treat lab automation as safety-critical: discover devices, check interlocks/limits, dry-run movement plans when available, and log every hardware-affecting command. Do not mix experiment protocol changes with manual machine nudges unless the protocol state is updated or clearly annotated.

### Vision/Measurement Tie-ins

When a PUDA operation depends on camera alignment, electrical measurement, or grid traversal, treat PUDA as the orchestration/state owner and the ViPSA subsections as device-specific technique. Do not improvise hardware movement or image-processing details: follow the relevant labeled subsection and its preserved reference package.

### ViPSA Vision Alignment

Use this subsection when the user asks to implement, modify, or run ViPSA camera-based alignment: camera-1 contact-pad/probe-tip alignment, OpenCV ROI crops, thresholding, contour ranking, Zaber correction moves, probe-tip annotation, qualitative photometric-stereo from `circle` light videos, or vision-guided contact approach.

Operational rules absorbed from the former `vipsa-vision-alignment` skill:

1. Load/perform the PUDA environment and machine-state checks in this skill before physical acquisition or motion.
2. Capture camera 1 with the lighted snapshot workflow: light on, capture one frame, cleanup/finally path for the requested final light state, and verify idle/on state as appropriate. If the user says cameras are swapped, or if recent captures look wrong, do not trust the `camera1`/`camera2` label alone: inspect a preflight frame and confirm it is the microscope/device contact-pad view before any Zaber correction.
3. For contact-pad alignment, establish the **actual physical probe-tip target in full-image pixels** from a fresh frame or a resolution-specific calibration. A centered `900x900` ROI may be used as a search window, but never assume its center is the probe tip unless independently calibrated. Revalidate remembered probe coordinates after camera, crop, resolution, or optical changes.
4. Detect square pads using polarity appropriate to the current frame: dark-response (`blurred_background - gray`) for dark pads on a lighter field, or bright-response (`gray - blurred_background`) for bright pads on a dark field. Use morphology plus square/area/extent filtering and visually inspect the annotated preflight.
5. Rank plausible pads by distance to the calibrated probe-tip target, not frame center. Let `offset = pad_centroid - probe_tip_target`; under the verified ViPSA sign convention use `zaber_axis_steps = round(offset_axis * M_axis)`. Start with the current nominal multiplier (commonly `21.5` or `25` native steps/px), then recapture and adapt axis-specific scale only from a plausible same-pad response.
6. After motion, recapture and rerun detection. If residual offset is only a few pixels, stop unless the user requests tighter tolerance. Otherwise, estimate **axis-specific observed calibration** from the successful first move and measured offset change: `Mx = abs(step_x / (offset_x_after - offset_x_before))` and likewise for Y, then use `next_step_axis = round(offset_axis_after * M_axis)`. Reject this estimate if the detected pad identity changed, the denominator is near zero, or the response sign/magnitude is implausible. Keep corrections bounded; a tiny final micro-correction is acceptable when it materially brings the verified residual inside tolerance. If a large correction leaves the offset nearly unchanged, or the overlay shows a motor/stage assembly, wire, screw, label, or other non-pad feature, stop immediately, do not continue, sum successful relative Zaber moves and command the inverse rollback, then report the failed detection with the overlay.
7. For probe-tip separation/annotation, generate an annotated artifact (orange/yellow probe taper, red tip marker) and report full-image pixel coordinates.
8. For qualitative photometric stereo from `circle` videos, detect the active bright window, fit a sinusoidal lighting model over sampled frames, produce depth/overlay/3D outputs, save numeric `.npy` arrays, and label the result as qualitative relative relief only.
9. For vision-guided contact approach, use `/home/vipsa/vipsa-puda-project/tools/vision_guided_approach.py`; no-motion modes are default and actual Z motion requires explicit `execute --execute`.
10. Reporting is terse and verification-oriented; use 🎯 for alignment reports and attach generated images with `MEDIA:/absolute/path`.
11. When the user selects a target in an older or annotated image, follow `references/image-selected-pad-relocation-adaptive-verification.md`: separate markup from the pad, account for image scaling, retract before lateral motion, verify same-target identity from surrounding geometry, and keep geometric alignment distinct from electrical contact.
12. When comparing before/after camera frames to decide whether a probe moved, register the after-frame to substrate-only features before measuring the tip. Report raw and substrate-relative displacement, visually verify tip markers, and generate a crop panel, registered overlay/difference, and blink GIF. See `references/paired-camera-probe-motion-difference.md`.

The former skill package is archived unchanged, and its session references have been re-homed as top-level umbrella references with the `vipsa-vision-alignment-` prefix, including `references/vipsa-vision-alignment-align-dark-pad-centering.md`, `references/vipsa-vision-alignment-residual-verified-multipass-pad-alignment-2026-06-23.md`, `references/vipsa-vision-alignment-vision-guided-contact-approach-2026-06-09.md`, `references/vipsa-vision-alignment-terse-align-overlay-photo-2026-06-25.md` for terse “align and send overlay photo” requests using the reusable alignment runner and final overlay attachment, `references/vipsa-vision-alignment-chained-stage-z-down-then-align-2026-06-29.md` for chained Z-only stage jog → standard camera-1 pad alignment requests, `references/vipsa-vision-alignment-camera-swap-wrong-view-rollback-2026-07-07.md` for camera-label swaps, wrong-view preflight rejection, and rollback after erroneous Zaber alignment moves, `references/vipsa-vision-alignment-resolution-aware-adaptive-calibration-2026-07-20.md` for deriving axis-specific native-steps-per-pixel from verified before/after offsets, and `references/vipsa-vision-alignment-probe-tip-target-adaptive-pad-polarity-2026-08-08.md` for aligning bright/dark pads to the actual visible probe tip rather than frame center.


Use this skill when the user asks about PUDA CLI, PUDA environments, PUDA machines, machine heartbeats, machine state, ViPSA camera alignment, PUDA-connected lab automation, or commands such as `puda env`, `puda machine`, `puda login`, or `puda config`.

## Quick workflow

1. Verify the CLI is available and identify the installed version:
   ```bash
   command -v puda && puda --version
   ```
2. Discover PUDA config/context:
   ```bash
   puda config list
   puda config get project_root
   puda config get nats_servers
   ```
   Note: PUDA CLI v0.0.33 removed `puda env`; do not use `puda env list/current` unless an older CLI's help confirms it exists.
3. Check whether the global config/login exists before machine operations:
   ```bash
   puda config list
   ```
4. If config is present, list machines with JSON for reliable parsing:
   ```bash
   puda machine list --json
   ```
   Fall back to human-readable output if JSON is unavailable or empty:
   ```bash
   puda machine list
   ```
5. For a specific environment, switch first, then list:
   ```bash
   puda env switch <env>
   puda machine list --json
   ```

## Protocol-file pitfall

For `puda protocol run --file ...`, do not generate a command-only JSON file. Include protocol metadata (`project_id`, fresh `protocol_id`, `user_id`, `username`, `description`, timestamp) plus `commands`; otherwise current PUDA CLI versions can fail before execution with `user_id is required in the protocol file`. Existing project protocol JSON files are a practical source for the active project/user values.

For an ordered multi-command machine transaction such as `get_current_position -> move_z_by -> get_current_position`, use one full-metadata protocol rather than issuing several `puda machine run` calls with the same run id. `machine run` may create a database run row per invocation, so reuse can fail on a duplicate-run foreign-key/uniqueness path after the first command. The protocol runner supplies START/COMPLETE once, preserves command order, and returns both before/after readbacks. Its `commands` array must contain driver commands only—never explicit START/COMPLETE entries.

**OpenFlexure Stage stale-run exception:** never use `puda machine reset stage` merely to clear `RUN_ID_MISMATCH` or a missing COMPLETE. On the Stage edge, reset invokes the driver reset/set-zero behavior: it does not physically move the stage, but it redefines the current physical location as logical zero and overwrites the persisted coordinate. This invalidates position tracking and creates a motion-safety blocker. Clear the exact stale run with `puda machine complete stage --run-id <exact-id>` only when the run identity is known and completion is safe; otherwise stop for explicit physical-coordinate reconciliation. Do not repair `stage/state/openflexure_position.json` from narrative or inferred coordinates.

`puda protocol validate --file /tmp/protocol.json` can pass from any directory, but `puda protocol run --file ...` also needs a PUDA project working directory containing the project `puda.config`. If run from a non-project directory, it can fail with `project puda.config file not found in current directory. Please run 'puda init' to create it first`. Keep generated protocol JSON files anywhere, but run the command with `workdir` set to the active project directory when available.

If the remembered ViPSA project path is missing but the machine is reachable and the task is a simple one-off machine command, do not stop at the stale path. Create a temporary PUDA project with `puda init . --name <name> --description <description>`, generate the full-metadata protocol using that temp project id plus `puda config list` user metadata, and run the protocol from the temp directory with the active NATS override. See `references/temp-project-protocol-run-fallback-2026-07-08.md`. Avoid dumping binary files such as `puda.db` when inspecting the temporary project.

When scripting `puda protocol run`, capture both stdout and stderr. If a machine response is not visible in the captured stream, recover it from the SQLite `command_log` table using `puda db exec` and the `run_id` or latest matching `machine_id`/`command_name`. This is especially useful for measurement payloads that need `payload.response.data.result`.

## Login/config pitfall

`puda machine list` and `puda env current` require the global config file. If the CLI reports:

```text
PUDA config file not found at ~/.config/puda/config.json. Please run 'puda login' to create it
```

Do **not** frame this as PUDA being broken. Report that the CLI is installed but not authenticated/configured for the current OS user, and give the fix:

```bash
puda login --username <your-username>
```

After login, rerun:

```bash
puda env current
puda machine list --json
```

## Reporting style

For Telegram, keep PUDA machine reports compact:

- If machines are returned: list environment, machine name/id, state, heartbeat/last seen, and any notable status fields.
- PUDA v0.0.36 `machine list --json` can finish in about 1.6 seconds, while ViPSA heartbeats arrive roughly every 6 seconds; a successful list can therefore omit live edges. Before declaring any expected edge offline, observe `puda.*.tlm.heartbeat` through a read-only NATS subscription for at least 15 seconds (or use an equivalent sufficiently long discovery window). Record the observation time, received machine IDs, and reported heartbeat timestamps. Distinguish fresh heartbeat connectivity from instrument command readiness; stored KV state is not a live probe. Do not upgrade PUDA or restart hardware merely to address this discovery-window limitation.
- If a live machine list is blocked by NATS timeout, do not imply availability. Report the exact endpoint/timeouts, then separately list the known expected machine IDs for the relevant rig as **known/unverified**, not live. For ViPSA, the expected set is `keithley-2450`, `keithley-707b`, `keysight-b2902b`, `light`, `stage`, and `zaber`.
- If blocked by login/config: show the exact failing command and the minimal login command needed.
- Avoid long setup explanations unless the user asks; PUDA operations are usually operational/diagnostic requests.

## Edge NATS configuration pitfall

Changing the PUDA controller/CLI NATS config does **not** change already-running PUDA edge services. Edges read `NATS_SERVERS` from their own `.env` / process environment at startup. When the user asks to move ViPSA edges to another NATS cluster, edit each edge `.env`, stop the old edge processes, restart all edges, then verify logs and machine visibility.

For the ViPSA workspace `/home/amdm/workspace/ViPSA`, the common edge set is `zaber`, `stage`, `light`, `keysight-b2902b`, `keithley-707b`, and `keithley-2450`; logs are under `logs/edges/`. See `references/vipsa-bears-nats-edge-restart-2026-07-28.md` for the exact stop/edit/restart/verify pattern used for `nats://bears:4222,nats://bears:4223,nats://bears:4224`.

## Hermes/PUDA observability logs

When checking whether a PUDA/Hermes agent is writing logs, query the Hermes logger database before drawing conclusions from local plugin config. The shared InfluxDB endpoint at `http://bearsnas:8181` uses the InfluxDB v3 SQL API shape, not the v2 Flux API: `/api/v3/query_sql?db=hermes-logs&q=<SQL>` with `Authorization: Token <provided-token>`. Count rows in `hermes_llm_turn`, `hermes_session`, `hermes_tool_call`, and `hermes_api_request` for the target `agent_id`; if other agent IDs have rows but the target has zero, report that as an agent-specific ingestion/configuration issue. See `references/hermes-logger-influxdb-v3-querying.md` for exact SQL/curl probes.

## References

- `references/manual-control-panel-nats-reconnect.md` — repair persistent jog-panel NATS connection closure and cross-event-loop access without replaying motion or resetting run/position state.
- `references/repeat-bounded-step1-approach-after-no-contact-2026-07-22.md` — continue a repeated bounded step-size-1 contact approach from the current Z position, report per-run versus cumulative travel, and preserve electrical/cleanup gates.
- `references/machine-listing-config.md` — notes from a WSL session where `puda env list` worked but `puda machine list --json` required `puda login`/`~/.config/puda/config.json`.
- `references/hermes-logger-influxdb-v3-querying.md` — query Hermes logger rows for PUDA/Hermes agent IDs through the bearsnas InfluxDB v3 SQL API without using stale Flux/v2 endpoints.
- `references/edge-restart-nats-advertised-route-pitfall-2026-06-25.md` — troubleshoot restarted edges logging `puda.edge_nats_client - ERROR`, stale machine states, and NATS clusters advertising unreachable internal `connect_urls`.
- `references/vipsa-bears-nats-edge-restart-2026-07-28.md` — fix edge/controller NATS mismatches: changing PUDA CLI `nats_servers` is not enough; edit each ViPSA edge `.env` `NATS_SERVERS`, restart all edges, then verify edge logs and `puda machine list` via bears.
- `references/nats-connectivity-diagnosis-no-fix-2026-06-30.md` — read-only diagnosis workflow for user requests like “find where the NATS issue is, do not fix”: distinguish TCP-open, raw NATS PONG, PUDA read-only health, Tailscale path quality, and unreachable advertised internal `192.168.50.6` routes.

## CLI version pitfall

Do not upgrade the PUDA CLI during active ViPSA operations just to troubleshoot NATS unless the user asks. Observed `puda update` from v0.0.29 to v0.0.33 removed the `puda env` command and moved NATS selection to `puda config set nats_servers ...`; this can break existing workflows and skills that expect `puda env current`. If an update was attempted and disrupts env workflows, restore the saved binary backup and restore `~/.config/puda/config.json` with `active_env: bears`.

## Useful commands

```bash
puda machine --help
```bash
puda machine state <machine>
puda machine commands <machine>
puda machine watch <machine> --json
```

PUDA CLI v0.0.29 changed `puda machine state <machine>` to refresh continuously until interrupted (like `docker stats`) and there is no `--once` flag. For scripts/verification, wrap it with `timeout`, for example:

```bash
timeout 3 puda machine state light
```

Use `--nats-servers` only when the user provides an override or the active environment is known to need one. Flag placement differs by command family:

```bash
# machine commands: global flag before the subcommand is accepted reliably
puda --nats-servers <comma-separated-nats-urls> machine list --json
puda --nats-servers <comma-separated-nats-urls> machine state <machine_id>

# protocol run: flag belongs on the run subcommand
puda protocol run --file protocol.json --nats-servers <comma-separated-nats-urls>
```

If the configured env has several NATS URLs and one route hangs/timeouts while raw TCP ports are reachable, retry with a single known-reachable server override before giving up.