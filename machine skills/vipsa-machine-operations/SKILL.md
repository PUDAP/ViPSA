---
name: vipsa-machine-operations
description: "Operate the ViPSA PUDA machine set in the bears env: Keithley/Keysight SMUs, 707B switch, lights, stage, and Zaber motion. Keep this skill updated as operational details are learned."
---

# ViPSA Machine Operations

## Persistent OpenFlexure position and strict limits

The stage edge persists logical X/Y/Z position in the host-local JSON file `stage/state/openflexure_position.json`. The file is atomically updated after every confirmed move and on graceful shutdown, is ignored by Git, and is mounted from the host for Docker deployments. Edge restarts, NATS resets, Hermes sessions, and PC reboots must load this state rather than resetting software position to zero. On reconnect the driver uses `G10 P0 L20` to synchronize GRBL work coordinates to the JSON position without physical movement.

All stage targets are hard-limited to `-300 <= x,y,z <= +300` logical steps. Limit checks occur before serial writes. Corrupt, out-of-range, pending, or uncertain state fails closed; do not delete or repair the JSON without explicit user reconciliation of the physical position. `set_zero`/`reset` is an explicit user-authorized declaration that the current physical pose is `[0,0,0]`. Graceful `shutdown`/`disconnect` persists state and must never move to zero. Untracked continuous Z motion and raw motion G-code are disabled. Always preserve signed movement commands exactly.

When verifying after an SDK update, old PUDA CLI KV output may be stale; use a fresh direct `get_position` transaction and inspect edge telemetry/logs for `position_limit_steps`, `position_state`, and `state_path`. On the live 2026-09-26 stage edge, `get_current_position` (still advertised by `puda machine commands stage`) returned `UNKNOWN_COMMAND`; direct `get_position` succeeded and returned `{x,y,z}`. For live safety preflights use the observed `get_position` command and compare against confirmed motion/persisted tracking; do not infer supported edge commands from stale CLI introspection. A limit test must use an out-of-range target and verify rejection plus unchanged JSON/readback; never test by moving to the physical boundary.

## Repaired OpenFlexure with mandatory collision controls (incident 2026-09-17; recommissioned 2026-09-18)

The OpenFlexure Y axis was physically damaged after coarse Zaber X travel reached `769055` during holder-edge mapping: the OpenFlexure assembly collided with an installed fixture underneath the probe-station platen. On 2026-09-18 the user confirmed that the Y axis had been repaired and the installed system recommissioned, lifting the blanket motion hard stop. The under-platen collision risk remains active: a tracked OpenFlexure Z retraction is not proof of coarse-stage clearance. Before broad holder motion, inventory above- and below-platen obstructions, establish conservative installed-system Zaber X/Y hard limits by physical dry-run while considering the full OpenFlexure/probe/cable/fixture envelope, and enforce those limits before every command. Preserve explicit staged authorization; when the user requests a validation move followed by a wait-for-go boundary, execute only that move and do not begin lateral travel until the go command.

Matrix readback parsing guard: `get_closed_channels` can return semicolon-separated `1A01;1B03`, not only comma-separated tokens. Preserve the raw reply, then normalize separators only in the parser before comparing the exact channel set. A delimiter-only parser rejection after a successful route does not mean routing failed; cleanup/verify nil before any fresh diagnostic, and never replay uncertain hardware commands.

Command-response parsing guard: a successful Zaber `move_x_by` response may omit the `data` field entirely. Treat a uniquely matched `status: success` as a returned command, use `.get('data', {})` for optional payloads, and obtain position through a separate read-only transaction. Never replay the move because a local parser raised `KeyError('data')`; reconcile exact before/after native positions first.

Use this skill whenever the user asks to operate, inspect, pause/resume, home, reset, or coordinate the **ViPSA machine set**

For a singular light action, first inspect live machine state and available commands. Prefer `puda machine run`, but if the edge rejects it because no run is active, use one validated non-empty UUID for the complete `START -> turn_on/turn_off -> COMPLETE` transaction. Always attempt cleanup and verify the final light machine state is `idle` with `run_id: null`. If a mismatch leaves the machine active, COMPLETE the exact live run ID before retrying. See `references/one-off-light-active-run-transaction.md` for the known-good command pattern and recovery procedure.

Reference: `references/electrical-machine-readiness-idn-and-direct-nats-2026-07-07.md` covers fresh readiness checks and the all-edge recovery workflow: stop active measurements first, avoid duplicate edge processes, distinguish reset-capable electrical edges from restart-only mechanical/light edges, recover self-contending USBTMC retry loops, restart a 707B edge when logical reset cannot recover an `ENODEV` VISA handle, verify actual hardware with `open_all` plus closed-channels `nil`, and retry partial measurements in a fresh run directory.

Reference: `references/compound-stage-zaber-premove-then-approach-2026-06-30.md` covers explicit chained stage-Z/Zaber pre-moves followed by default contact approach; report snap-in/snap-out as not stabilized and verify cleanup.

Reference: `references/stage-edge-coordinate-frame-and-historical-z-reconstruction.md` covers stage-edge origin resets and historical Z reconstruction. A reported `[x,y,z]` is run-local tracked state; never compare Z values across edge restarts as absolute physical heights without reconstructing the verified signed-move chain.

Reference: `references/exact-jog-chain-and-direct-machine-set-safety.md` covers exact signed stage/Zaber jog chains, lifecycle-aware use of `puda machine run` with protocol/Direct fallback when an edge requires START, per-move readback verification, motion→camera ordering, interrupted-operation handling, and the critical rule that a Direct context must own every machine touched by shared cleanup helpers.

Reference: `references/concise-vipsa-reporting-verbose-opt-in-2026-07-29.md` captures the user’s reporting preference for ViPSA operations: concise, tool-verified results by default; verbose edge logs, GRBL output, or every approach step only when explicitly requested.

Reference: `references/pea2pbbr4-pbit-substrate-optimization-2026-07-29.md` covers PEA2PbBr4 p-bit substrate screening for on-chip simulated annealing: one-step spincoat fabrication constraints, available process knobs, device-selection-as-effective-temperature framing, and sequential DOE/ViPSA characterization metrics.

Reference: `references/manual-device-revisit-absolute-z-and-approach-2026-06-30.md` covers paused-grid manual revisits where the user gives a relative safe Z move, a target grid device, an explicit absolute tracked Stage-Z pre-approach height, and then approach; compute the delta to the absolute Z target, verify readback before approach, and report no-contact-after-max honestly if pA/sub-nA persists.

Reference: `references/manual-s1-7x7-device6-revisit-2026-07-14.md` covers terse manual revisits to a prior S1 7x7 grid device from run artifacts: compute aligned absolute Zaber target from the stored grid target plus recorded alignment correction, keep stage at safe negative Z, force SMU outputs off and 707B open/nil before X/Y travel, move Zaber with absolute native `move_x_to`/`move_y_to`, and verify Zaber/stage readback plus idle states.

Reference: `references/pause-grid-job-cleanup.md` captures the verified pause/cleanup pattern for active ViPSA grid jobs: stop tracked run process, pause reporter cron, turn SMU outputs off, abort measurements, open/verify 707B, turn lights off, reset on run_id_mismatch if needed, then verify all involved machines are idle with null run ids. If PUDA/NATS responses time out during cleanup, do **not** claim safe cleanup; report cleanup verification as blocked/unverified and distinguish this from artifact evidence that no electrical phase started.

Reference: `references/manual-approach-stop-cleanup-and-reporting-2026-07-28.md` covers terse `stop` during standalone approach: kill the approach process, run SMU-off/abort, 707B open/nil, light-off, stage-abort/readback cleanup, verify all six machines idle/null, and report cleanup verification rather than only saying `Operation interrupted`.

Reference: `references/stage-clear-holds-and-single-edge-restart.md` covers clearing Stage motion/lifecycle holds before restart, identifying the correct generic `main.py` process by CWD and `/dev/openflexture` ownership, restarting exactly one Stage edge, and verifying it with a harmless read-only lifecycle transaction plus final `idle`/`run_id:null` state.

Reference: `references/interrupted-vipsa-approach-partial-artifact-reconciliation-2026-07-28.md` covers killed/interrupted `tools/vipsa_approach.py` runs where `approach_summary.json` / `approach_log.csv` are missing but per-command protocol artifacts may prove partial Stage-Z motion. Always inspect `approach_coarse_z_move_*_run.txt` and final stage readback before claiming no motion; validate-only files show the next unexecuted step.

Reference: `references/verbose-step-approach-stop-and-stage-edge-reconciliation-2026-07-28.md` covers user-requested verbose per-step approach runs, including step-size overrides (for example `--step 1`), `STEP_UPDATE`/polling patterns, watch-pattern rate-limit pitfalls, JSON-safe argparse/path serialization in approach runners, stop cleanup, and reconciling whether Stage-Z actually moved from per-command artifacts plus `/home/amdm/workspace/ViPSA/logs/edges/stage.log`.

Reference: `references/manual-stage-approach-stop-setzero-and-verbose-updates-2026-07-28.md` covers a compact checklist for this same manual Stage-Z/approach class: inspect partial artifacts before saying no motion happened, clear START-only stale stage runs after killed approaches, verify `set_zero()` by re-reading position when the final readback was interrupted, and prefer manual polling/batched updates when per-step watch notifications rate-limit.

Reference: `references/stale-shared-run-id-after-grid-stop-recovery-2026-07-27.md` covers the case where a killed grid/direct runner leaves `light`, `stage`, and `zaber` reporting `idle` with the same stale non-null `run_id`, blocking later PUDA protocols at START. Clear with reset/readback plus harmless full-metadata recovery protocols (`light.initialize/off`, `stage.get_current_position`, `zaber.get_current_position`) before retrying the requested measurement.

Reference: `references/local-vipsa-edge-restart-stale-run-recovery-2026-07-27.md` covers local ViPSA edge recovery when light/stage/707B protocols time out at START because edge subscribers are stale or duplicated: stop duplicate per-machine edge processes, restart only the affected edge, complete the exact stale run id if the restarted edge accepts the delayed START, verify `idle/run_id:null`, then retry and report only the verified successful retry.

Reference: `references/reusable-vipsa-motion-approach-scripts-2026-07-27.md` covers the reusable project scripts `tools/vipsa_move.py` and `tools/vipsa_approach.py` for protocol-first Stage-Z/Zaber movement and customizable Keithley-guided contact approach. Both default to dry-run and require `--execute` for physical/electrical side effects.

Reference: `references/local-nats-quick-check-and-approach-2026-07-27.md` covers continuing ViPSA quick resistance checks and approach after local JetStream NATS recovery: always pass explicit `nats://127.0.0.1:4222` script/PUDA overrides when project configs may still point at `bears`, verify read-only control first, compare repeated quick checks for consistency, and report sharp approach contact-edge outcomes without per-step spam.

Reference: `references/stage-edge-nats-endpoint-alignment-and-readback-2026-07-28.md` covers Stage-Z move failures after NATS/edge restarts: match the PUDA endpoint to the endpoint shown in the stage edge logs, split motion and readback into separate protocols when run-state is fragile, and report command success separately from numeric coordinate verification.

Reference: `references/stage-software-readback-vs-physical-motion-and-edge-reconnect-2026-07-28.md` covers the critical case where Stage-Z PUDA commands and `get_current_position()` report success/change but the user observes no physical motion: current stage readback is software-tracked, not hardware-verified; stop approach loops, audit/reconnect only the stage edge, and require visual confirmation or driver fixes before trusting automatic approach.

Reference: `references/manual-stage-z-false-success-direct-driver-recovery-2026-07-31.md` covers the follow-up recovery pattern after a manual Stage-Z command reports success but visibly does not move: stop duplicate/stale stage edge processes, perform the requested recovery move through the `Stage` driver (not raw G-code), inspect GRBL `MPos`/`ok`, restart exactly one stage edge, and report the prior PUDA readback as untrusted software-tracked state. **Controller `ok`/`MPos` is command-accounting evidence, not independent proof that open-loop mechanics moved.**

Reference: `references/stage-physical-motion-evidence-and-edge-restart.md` defines the evidence hierarchy for disputed Stage-Z motion: stop stacking uncertain moves, remove duplicate edges, restart exactly one edge, separate cached/controller readbacks from independent visual/encoder/mechanical confirmation, and never call PUDA success or GRBL `MPos` physical verification by itself.

Reference: `references/local-nats-edge-restart-stale-stage-and-light-recovery-2026-07-28.md` covers manual stage/light commands after local NATS dies or edge restart replays stale STARTs: restart local JetStream, start only affected edges, clear stale stage state with a harmless `get_current_position()` protocol, split stage move and readback into separate protocols when combined move→read loses run state, and report command success separately from numeric readback.

Reference: `references/discussed-device-vs-live-device-approach-retry.md` covers terse approach retries after a grid has advanced: reconcile the reply-chain device with live Zaber X/Y before any Z motion, ask when they differ, and honor the user's no-gross-retract policy between subsequent bounded attempts while preserving minimum-step over-current trims and safe retracts before X/Y travel.

Reference: `references/electrical-machine-readiness-idn-and-direct-nats-2026-07-07.md` covers checking whether the three ViPSA electrical machines are really reachable when `machine list`/state timestamps are stale, direct `identify()`/IDN results for the 2450 and Keysight, the fact that 707B does not expose `identify()` and must be reset after an unknown-command error, and a minimal socket-level NATS fallback when `nats.py` is unavailable.

Reference: `references/keithley-707b-usb-disconnect-valueerror-recovery-2026-07-31.md` covers the 707B failure mode where the edge receives PUDA commands but the PyVISA/USB write raises `[Errno 19] No such device` as `ValueError` inside `_send_switch_command()`, bypassing the driver's `VisaIOError` retry. Restart only the 707B edge, but identify processes by CWD and stop both any login-shell wrapper and surviving `uv run main.py` child before launching exactly one replacement; verify successful edge subscriptions and `get_closed_channels == nil`. If PyVISA resource discovery hits a per-process file-descriptor limit during restart, raise the replacement edge's soft limit (for example `ulimit -n 4096`) and retry, then check VISA resource visibility / replug or power-cycle the 707B if needed before rerunning electrical measurements.

The ViPSA machine is the subset of the active `bears` PUDA environment comprising:

- `keithley-2450` — Keithley 2450 SMU. Primary use: contact detection, resistance measurement, and DC IV sweeps.
- `keithley-707b` — Keithley 707B switch matrix / route controller. It electrically switches the DUT connection between the Keithley and Keysight SMUs.
- `keysight-b2902b` — Keysight B2902B / B2901BL-family SMU. Primary use: pulse-train measurements. User may refer to it as Keysight, B2901, B2901BL, B2902, or B2902B; PUDA machine ID observed here is `keysight-b2902b`.
- `light` — serial light controller
- `stage` — Arduino stage controller / motorized microscope stage
- `zaber` — Zaber X/Y stages

Do **not** treat unrelated `bears` machines (`biologic`, `first`, `opentrons`, etc.) as part of ViPSA unless the user explicitly expands the scope.

## Required context and companion skills

Load these before ViPSA work:

1. `puda-operations` — CLI login/config/env/machine workflow.
2. `puda-env` — environment routing and env-specific skill lookup, when installed. If `skill_view` reports this legacy skill is absent, use the environment/config discovery in `puda-operations`; its absence is not a hardware blocker. Preserve the explicitly authorized NATS endpoints.
3. This skill, `vipsa-machine-operations`.
4. For memristor electrical measurement tasks — DCIV sweeps, split-compliance sweeps, voltage pulse trains, resistance/read-probe interpretation, compliance behavior, Vset/Vreset extraction, ON/OFF ratio, plotting, or high-throughput device/substrate summaries — also load `vipsa-electrical-measurements`.
5. For user-facing ViPSA capability/reference Markdown files, use `references/vipsa-reference-markdown-generation.md` for the live-driver-method inventory and downloadable artifact workflow.

## Baseline environment

Observed working environment:

```text
Env:            bears
Description:    create tower (dev work)
NATS servers:   nats://100.109.131.12:4222,nats://100.109.131.12:4223,nats://100.109.131.12:4224
Logged-in user: vipsa
Config path:    ~/.config/puda/config.json
```

Always verify live state instead of assuming it remains true. On PUDA CLI versions that still support env commands, use:

```bash
puda env current
puda machine list
```

On PUDA CLI v0.0.33+ where `puda env` is removed, use:

```bash
puda version
puda config list
puda config get nats_servers
puda machine list --json
```

For ViPSA, if configured hostnames such as `bears:4222` are unreliable from WSL, retry read-only listing/state with the known Tailscale NATS servers `nats://100.109.131.12:4222,nats://100.109.131.12:4223,nats://100.109.131.12:4224` or single-server overrides. If all endpoints time out, report the known ViPSA machine set as unverified rather than live/available.

For a user question like “which machines are live?”, report the active env that was checked. If the active env is not `bears` but the surrounding context is ViPSA, check `bears` as well and explicitly separate the two results rather than answering only for an unrelated env. For ViPSA live checks, heartbeat discovery should include the six-machine set `keithley-2450`, `keithley-707b`, `keysight-b2902b`, `light`, `stage`, and `zaber`; then verify relevant state snapshots and report idle / `run_id: null` when available.

PUDA CLI v0.0.29 changed `puda machine state <machine_id>` to refresh continuously until interrupted. When a one-shot state snapshot is needed in scripts, use `timeout`, for example `timeout 3 puda machine state light`.

## First checks for any operation

1. Confirm PUDA CLI and login/environment routing. Check command availability before calling legacy env commands so modern CLI runs do not emit a misleading `unknown command "env"` error into otherwise successful summaries:
   ```bash
   command -v puda && puda --version
   if puda help env >/dev/null 2>&1; then
     puda env current
   else
     puda config list
     puda config get nats_servers
   fi
   ```
2. Confirm all ViPSA machines are visible:
   ```bash
   puda machine list
   ```
3. Inspect state before side effects:
   ```bash
   for m in keithley-2450 keithley-707b keysight-b2902b light stage zaber; do
     echo "===== $m ====="
     puda machine state "$m"
   done
   ```
4. For machine capabilities, query live signatures:
   ```bash
   puda machine commands <machine_id>
   ```

## Safety rules

- **Protocol-first rule:** for ViPSA machine operations, use `puda protocol` by default unless the user explicitly states otherwise. Direct/raw NATS control is not the default execution path; use it only for read-only diagnosis, explicit user-approved fallback/cleanup, or emergency safety handling when protocol control is impossible.
- **High-latency DERP protocol bridge:** if every known ViPSA NATS port is TCP-open and `tailscale ping` works only via DERP at >~1 s, but the Go `puda` CLI fails its initial NATS handshake with `i/o timeout`, preserve protocol-first execution by starting the short-lived bridge in `scripts/nats-latency-proxy.py`, then point `puda ... --nats-servers nats://127.0.0.1:<local-port>` at it. The bridge immediately supplies local NATS INFO/PONG while opening the slow upstream connection, buffers the initial client commands, then forwards transparently. Treat this bridge as process-scoped, not durable: a Hermes gateway restart or interrupted session may remove it. Before creating another bridge, list tracked processes and prefer an already-running bridge that has previously completed a PUDA protocol; verify it with a read-only machine-state request. A successful state lookup proves basic transport only, not that the protocol response dispatcher can subscribe successfully, so for an unproven/new bridge run a harmless one-command read-only protocol before any physical move. Require normal PUDA START/command/COMPLETE responses, a separate post-motion position protocol, and final machine-state verification. Stop newly created task-scoped bridges after the bounded operation; do not kill a pre-existing shared bridge unless its owner/scope is known. This is preferable to direct command publishing when the user has not authorized a raw-NATS fallback.
- Prefer **read-only inspection** (`list`, `state`, `commands`) unless the user explicitly asks for a side effect.
- Before changing electrical routing or SMU output, ensure the relevant SMU output is off or use the driver’s conservative helpers (`connect_switch_path`, `disconnect_switch_path`, `abort_measurement`, `reset`).
- Treat `keithley-707b` route changes as break-before-make: use `connect_named_route`, `connect_keithley_smu`, or `connect_keysight_smu` rather than manually closing multiple routes unless the user gives exact channels.
- Motion commands (`stage`, `zaber`) can physically move hardware. Confirm target/relative distance and units when not provided.
- **Stage X/Y safety:** the `stage` is a motorized microscope stage. Do not move `stage` in X or Y (`move_x_by`, `move_y_by`, `move_xy_by`, `move_xy_to`, `move_with_lim_by`) unless the user explicitly mentions X/Y movement. Z-only requests may use `move_z_by(height, feedrate=450)` with the signed height the user gives.
- For Zaber “microsteps” / “native units,” use `units: null` in PUDA protocol params; do **not** convert to `mm` or use `units: "mm"` unless the user explicitly requested millimetres.
- `stage.disconnect()` moves to zero before disconnecting. Do not use it casually if returning to zero is not intended.
- `light.change_intensity()` is a placeholder; do not promise intensity control unless firmware support is confirmed.

## General PUDA machine commands

Read-only:

```bash
puda machine list
puda machine list --json
puda machine state <machine_id>
puda machine commands <machine_id>
```

## PUDA protocol JSON and response recovery

When generating active protocol JSON by hand or from a script, include full protocol metadata, not only `commands`. Current `puda protocol run` rejects command-only files with `user_id is required in the protocol file`. Use a fresh `protocol_id`, active `project_id`, `user_id`, `username`, description, timestamp, and the command list. Existing project protocol files under the active PUDA project are a reliable source for the project/user metadata.

**Critical protocol-cloning guard:** PUDA executes the top-level `commands` array; a top-level `steps` array is ignored. When cloning an existing motion protocol to make a read-only query, replace `protocol["commands"]` itself and remove any stray `steps` key. Before execution, read back the generated file and assert that every command name is read-only (for example, only `get_current_position`). Never assume assigning `steps` replaced an inherited motion command. If an unintended relative motion occurs, immediately restore the exact verified pre-query position with the inverse relative move, then verify the restored readback and disclose the incident.

When invoking `puda protocol run` from Python, parse `stdout + stderr` together; the CLI can emit logs/responses outside stdout. If response extraction still fails, recover from the PUDA database `command_log` for the matching `run_id` or latest matching `machine_id`/`command_name`. For Keithley reads, extract `payload.response.data.result[*]["I_meas (A)"]` first, then `"Current (A)"`. For stage position, extract `payload.response.data.result` as `[x, y, z]`. Always run electrical cleanup even if parsing fails. See `references/protocol-metadata-and-command-log-recovery-2026-06-07.md` for the concrete recovery recipe.

Control-level commands exposed by the CLI:

```bash
puda machine pause <machine_id[,machine_id...]>
puda machine resume <machine_id[,machine_id...]>
puda machine reset <machine_id>
puda machine home <machine_id> [machine_id...]
puda machine update <machine_id> [--ref <git-url-or-image>] [--source-type git|docker]
```

Use `home` only for machines where homing is meaningful. For SMUs, observed `home()` returns no-op/false; for motion machines, homing can move hardware.

## Observed machine states and discovery pitfalls

On 2026-06-03, all six ViPSA machines responded to `puda machine state` as `idle` with `run_id: null`.

`puda machine list` only reports machines with recent heartbeat responses. Do not conclude a known ViPSA machine is absent solely because `list` omits it. For historical/known machines, probe the exact machine ID with:

```bash
puda machine state <machine_id>
puda machine commands <machine_id>
```

If `state`/`commands` work but a protocol run times out on the `START` command, report that the machine has a PUDA KV/state bucket and driver metadata but its edge is not currently responding to runs. Do not claim to have retrieved live instrument data such as VISA/LAN/GPIB addresses unless a command response actually returns it.

Keithley 2450 PUDA edge pitfall observed: a protocol involving `keithley-2450` may fail immediately at START with `cannot start, <same-run-id> is currently running`, leaving the machine state `active` for that run. In that case, do **not** claim the requested SMU command/measurement executed. First attempt to clear the stuck state with `puda machine reset keithley-2450` (the reset request may time out while still returning the state to `idle`), then verify `puda machine state keithley-2450`. Run a separate `keithley-707b`-only `open_all` + `get_closed_channels` cleanup protocol to ensure the switch matrix is disconnected. Report that the Keithley command path was blocked by START failure unless a later protocol response shows the SMU command actually succeeded. Troubleshooting evidence: after reset leaves `keithley-2450` idle, a one-command read-only `get_position` protocol still fails at START with `RUN_ID_MISMATCH` where the reported currently-running ID is the same new run ID; `keithley-707b` and `light` protocols start and complete normally. This isolates the problem to the `keithley-2450` edge/start handler or duplicate subscriber/state handling, not general NATS connectivity or the protocol runner.

## Machine capability notes learned so far

### Electrical-test address / identity checks

When asked to check addresses or identity for the electrical-test instruments, use safe read-only diagnostic commands first. See `references/electrical-address-discovery.md` for the full address-discovery workflow, direct NATS KV inspection recipe, PyVISA probe, and reporting standard.

1. Verify known PUDA machine IDs:
   ```bash
   for m in keithley-707b keithley-2450 keysight-b2902b; do
     puda machine state "$m"
     puda machine commands "$m" | sed -n '1,80p'
   done
   ```
2. If the edges are responsive, run a protocol with the read-only `identify()` command for the SMUs. For the switch, there may not be an `identify()` command exposed; `get_closed_channels()` is read-only but does not reveal address. Do not use routing commands just to check address.
3. If live protocol commands time out, inspect NATS JetStream KV command metadata to confirm capabilities, but remember that this metadata is generated from method signatures/docstrings and usually does **not** expose driver constructor args, `.env` config, or PyVISA resource strings.
4. A `START command failed ... timeout waiting for response` means the edge did not accept the run; report the timeout and stale state timestamps rather than inventing instrument addresses.

Example read-only protocol skeleton:

```json
{
  "commands": [
    {"step_number": 1, "name": "identify", "machine_id": "keithley-2450", "params": {}},
    {"step_number": 2, "name": "identify", "machine_id": "keysight-b2902b", "params": {}},
    {"step_number": 3, "name": "get_closed_channels", "machine_id": "keithley-707b", "params": {}}
  ]
}
```

### `keithley-2450`

Role: Keithley 2450 source-measure unit. Primary use: contact detection, resistance measurement, and DC IV sweeps.

Useful methods reported by `puda machine commands keithley-2450`:

- Session/setup: `initialize()`, `reset()`, `reset_device()`, `clear()`, `close_session()`
- Safety/output: `abort_measurement()`, `set_output(enabled: bool)`
- Source/sense config: `set_source_function(function)`, `set_source_level(function, value)`, `set_source_range(function, value=None, auto=True)`, `set_sense_function(function)`, `set_sense_range(function, value=None, auto=True)`, `set_protection(function, value)`, `configure_measurement_format(functions)`
- Measurements: `hold_voltage_measure_current(voltage, current_compliance, ...)`, `hold_current_measure_voltage(current, voltage_compliance, ...)`, `query_reading()`, `run_voltage_pulse_train(voltages, current_compliance, pulse_width_s, ...)`
- Switch integration: `connect_switch_path()`, `disconnect_switch_path()`
- Diagnostics: `identify()`, `get_error()`, `read_errors()`
- Position telemetry: `get_position()` returns fixed payload
- `home()` has no defined SMU homing sequence.

SCPI dialect guard: do not mix native 2450 and 2400-emulation headers. The 2450 reference manual (2450-901-01 Rev. E, §18 data-acquisition conversion table) places `:FORM:ELEM` and `:SENS:CURR:PROT` in the **2400** column; native 2450 uses trace-buffer element queries and `:SOUR:VOLT:ILIM`. On 2026-09-15 the active native-list driver emitted both legacy `:SENS:CURR:PROT` and native ILIM; the legacy header is the manual/source-supported cause candidate for its final -113. An offline recording-transport regression fails on the original and passes after removing the legacy line, but this is not hardware isolation. The public PUDA surface currently exposes no compliance/range/output getters or raw SCPI query, so a clean error queue after safe range setters is not full settings verification. Stage unchanged/configuration checkpoint evidence: `runs/pea_current_plus5_campaign_20260915/contact_method_iteration02/`. Candidate there is explicitly NOT_DEPLOYED. Do not invoke knowingly legacy configuration helpers to recreate the error, race the edge with direct VISA, or acquire before supported output-off setting/readback verification.

For single-point resistance by applying a specified voltage and reading current, prefer the high-level method `hold_voltage_measure_current(voltage, current_compliance, settle_s=..., read_count=1, reset=True)`. In a full DUT protocol, use the conservative sequence: `set_output(false)` → `keithley-707b.connect_keithley_smu()` → `hold_voltage_measure_current(...)` → `set_output(false)` → `keithley-707b.open_all()` → `get_closed_channels()`. The measured resistance is computed by the caller as `R = voltage / current` using the returned current value; protect against zero/near-zero current. If a small-voltage resistance check (for example `0.01 V`) returns a current very close to the configured current-compliance limit, interpret/report this as likely current compliance and a likely shorted DUT rather than as a normal precise resistance value.

Contact-approach probing workflow learned for Keithley + Z stage: because the algorithm has thresholds, abort checks, and Z-motion loops, run it as an outer Python orchestrator that sends small PUDA protocol commands one at a time rather than as one static protocol. Verify machines idle when possible, `set_output(false)`, `connect_keithley_smu()`, then loop: `hold_voltage_measure_current(voltage=test_voltage, current_compliance=10*upper_current_threshold, settle_s=settle_delay, read_count=1, reset=True on the first read and False thereafter)` → compare `abs(I)` to thresholds → `stage.move_z_by(height=<signed step>)` → local `sleep(settle_delay)`. If current exceeds the upper threshold, retract by `-0.5*step` and every 10 backsteps add `-2.5*step`; after stabilization, fine approach by `0.25*step` up to 20 attempts if current is below lower threshold. For the final high-current guard, do not rely on a single `-0.1*step` retraction: remeasure and repeat bounded small trim retractions until `abs(I)` is inside the requested window or a hard trim limit is reached. Always cleanup with `set_output(false)`, `keithley-707b.open_all()`, `get_closed_channels()`, and final machine states when available. If PUDA CLI state checks time out through NATS after a verified direct operation, report the CLI-state blocker separately and rely only on direct cleanup evidence: Keithley output-off response, 707B `open_all` response, `get_closed_channels() == nil`, and stage position readback. In successful +Z runs with lower/upper thresholds ordered as lower < upper, contact can be detected after coarse approach and then reported as in-window, but include signed current; for the user's current PEA-based devices/probing polarity, negative current at positive applied voltage indicates open circuit / very high HRS, not retained LRS. Use the 👇 emoji when reporting approach/contact-approach results.

For terse post-alignment requests like “turn off the lights and perform approach,” or just “approach” immediately after a move-to-device/alignment, use the established electrical approach defaults instead of asking for parameters: `test_voltage=0.01 V`, `lower=1e-8 A`, `upper=1e-7 A`, `settle=0.2 s`, forward `+Z`, and a conservative step such as the most recently used value or `0.5`. Choose `max_attempts` to cover the immediately preceding intentional Z retraction/pre-move while staying bounded (for example 120 attempts at 0.5 after a -35 to -50 Z move). If the user explicitly overrides the approach step size “just this once,” apply only that single parameter and keep the established thresholds/direction/settle defaults. First turn lights off when doing electrical approach, then run the Keithley-guided approach. If the first live approach read is already inside the target window, do not command any Z motion; confirm/stabilize, report `in_window` with `net_z_steps: 0.0`, then cleanup. Do not skip an explicit later `approach` request merely because a previous compact resistance check looked pA/open-like; re-read live and gate motion from the fresh approach current. If the bounded loop remains pA/sub-nA and below the lower threshold, stop as `no_contact_after_max`, cleanup, and report “no contact detected” rather than continuing automatically or implying success. When `approach` follows one or more separately verified manual +Z pre-advance commands, start a fresh bounded electrical approach from the latest readback: do not repeat the manual moves, do not treat large cumulative travel as contact evidence, and report approach-block travel separately from the prior pre-advance. This default does not apply to visual/probe-deflection approaches, where the user still expects a plan/approval before Z motion. See `references/terse-post-alignment-approach-2026-06-30.md`, `references/approach-after-open-like-resistance-immediate-in-window-2026-07-01.md`, and `references/manual-z-preadvance-then-terse-approach.md` for verified terse-command execution and reporting patterns.

Interrupted align→approach handoff: if alignment completed but `/new`, a gateway restart, or another interruption occurred before the electrical approach began, a later terse `approach` request should resume at the standalone approach phase rather than repeating the successful alignment. Re-establish any short-lived NATS bridge, inspect fresh `keithley-2450`, `keithley-707b`, `stage`, and `light` states, and clear stale non-null run IDs before routing or motion. A `puda machine reset` may time out while still clearing a machine to `idle`/`run_id: null`; always re-read state and use the verified post-reset state, not the reset command's exit status alone. Then turn lights off and apply only the user's newly supplied approach override (for example `step_size=1`) while preserving the established voltage, thresholds, direction, settle time, bounded attempt count, and cleanup. For long bounded loops, run a tracked background process, inspect the saved `summary.json` after completion, and verify output-off, 707B `nil`, stage readback, and all final idle/null states before reporting.

Final approach trimming pitfall: after over-current contact, a bounded trim loop can overshoot below the lower contact threshold, especially when the contact transition is sharp. Never command Z increments smaller than the hardware-supported minimum (`0.25` steps). If a final fine `+0.25` step jumps just above `upper_current_threshold`, do one minimum valid retract (`-0.25`) and re-read before leaving the tool over-contacted. If the post-retract current falls below `lower`, report **contact edge / safely below contact**, not a fully stabilized contact, even if the computed resistance looks finite. Record both sides of the bracket—last below-threshold Z/current and first above-threshold Z/current—and do not oscillate between them when no hardware-valid position lies in-window. Include final current relative to thresholds, net Z change, final stage position, cleanup (`set_output(false)`, `open_all`, `get_closed_channels`), and final idle/readback states in the concise report. See `references/direct-nats-command-path-and-align-approach-edge-2026-06-09.md` for a concrete align→approach edge case and `references/minimum-step-contact-edge-bracketing-2026-07-22.md` for the minimum-resolution bracketing/stop pattern.

Post-approach handoff rule for alignment → approach → DCIV chains: do not automatically run DCIV after approach. If contact was detected and final current is within the requested window, ask for DCIV sweep parameters next. If no contact was detected after `max_attempts`, report final current, total Z travel/readback, and cleanup state, then ask whether to approach further or proceed with DCIV despite no detected contact. If final current remains above `upper_current_threshold` after trim attempts, report it as not stabilized and ask before DCIV.

When the user explicitly combines a Z move and DCIV in one request (for example “move z up by 1 step and then run a DCIV”), treat the DCIV as authorized after the motion, but still run a non-stressing Keithley 10 mV precheck before the sweep. Abort and cleanup if the precheck is short-like/near compliance; otherwise proceed with the established conservative split DCIV recipe or the user’s specified recipe. See `vipsa-electrical-measurements/references/z-increment-then-dciv-precheck-2026-06-09.md`.

When the user explicitly combines a manual Z move and a resistance/contact check (for example “move z up by 25 steps and check resistance”), execute the signed Z move first with a full-metadata `stage.move_z_by` protocol, verify stage position in a separate protocol, then run the compact Keithley/707B low-bias diagnostic (`0 V`, `±10 mV`, `±50 mV`, low compliance), compute paired differential resistance, and cleanup/output-off/open-all. See `references/manual-z-increment-then-resistance-check-2026-06-25.md`.

Post-approach no-contact diagnostic: if the user suspects the contact is not properly made, or asks whether a pA/sub-nA read is open circuit vs true high-resistance HRS, do not jump to forming/DCIV. First use a non-stressing Keithley diagnostic: turn lights off if requested, route DUT to Keithley, read current at several small biases (`0 V`, `±10 mV`, `±50 mV`, optionally `±100 mV`) with low compliance, and check whether current scales with voltage. If ambiguous, perform a tiny Z-sensitivity check using `+0.25` or `+0.5` forward Z increments with a low-voltage read after each step. A sudden current jump with Z suggests incomplete contact; stable voltage-scaled current suggests real high-HRS; pA noise floor with no voltage dependence suggests open/poor contact or HRS beyond measurement sensitivity. Always cleanup (`set_output(false)`, `open_all`, `get_closed_channels`). The detailed recipe is in `vipsa-electrical-measurements/references/open-vs-high-hrs-contact-diagnostic-2026-06-06.md`.

For terse live requests like `check resistance`, use the same non-stressing Keithley/707B route but default to a compact low-bias resistance diagnostic (`0 V`, `±10 mV`, `±50 mV`, `1 µA` read compliance) and concise reporting. If `±10 mV` reaches the read compliance, report a bound such as `R <= ~10 kΩ at 10 mV` and classify it as definitely conductive / short-like rather than a precise resistance. See `vipsa-electrical-measurements/references/quick-low-bias-resistance-check-2026-06-18.md`.

For one-time contact-approach step-size overrides and the final-trim overshoot pitfall, see `references/contact-approach-step-size-override-and-trim-overshoot-2026-06-08.md`. For a concrete step-size-1 approach that reached the 10–100 nA window after 32 `+Z` moves, plus the explicit-cleanup-after-script-error pattern, see `references/contact-approach-step1-cleanup-2026-06-10.md`. For consecutive user-authorized step-size-1 retries through the PUDA latency bridge, preserve cumulative Stage-Z readback, give each request a separate bounded move budget, and report persistent pA current as no contact; see `references/repeated-step1-approach-protocol-bridge-2026-07-21.md`. More generally, after any custom bounded approach ends `no_contact_after_max`, a terse immediate `approach` means a fresh bounded block from the current verified Z using the complete preceding recipe—target window, voltage, compliance, direction, step, settle time, and move limit—rather than reverting to generic defaults; see `references/repeat-custom-bounded-approach-after-no-contact.md`. If that repeated block stays at the pA floor and then jumps directly to compliance on one coarse step, run only the configured bounded minimum-step trim; if it remains compliance-limited, stop as `still_over_current_after_trim`, report the last-below/first-above bracket plus gross/trim/net travel, and do not silently continue forward on a later terse request. See `references/repeated-step1-compliance-cliff-after-no-contact-2026-07-25.md`. For a coarse `+1.0 Z` / `0.5 Z` trim override that hit a very sharp contact edge and could not stabilize in-window, see `references/contact-approach-coarse1-trim0p5-sharp-edge-2026-06-24.md`; report this honestly as contact-edge/too-coarse-trim rather than success.

For user-approved conservative post-approach DCIV/forming, execute in bounded branches with inspection between branches rather than committing blindly to the full planned sweep. If a low-voltage positive branch at low compliance is already compliance-limited near `+0.05` to `+0.10 V` and measured voltage collapses near zero, stop the remaining branches, cleanup (`set_output(false)`, `open_all`, `get_closed_channels`), and report a short-like/over-contact safety stop. The electrical details and PUDA data-recovery note are in `vipsa-electrical-measurements/references/conservative-dciv-forming-safety-stop-2026-06-06.md`. If the user then explicitly asks for a whole DCIV anyway (for example, “run a whole DCIV” or “do an additional negative/reset side first”), honor the requested branch order while keeping a hard danger-current/instrument-fault guard; report planned compliance hits as outcomes rather than silently reusing the earlier safety-stop policy.

For conditional health→motion requests, do the electrical condition first and only move if the measured condition is met. For example, if the user says to move Z down and move Zaber only if the device is shorted/perma-SET, run low-bias Keithley reads first; pA/sub-nA high-resistance readings should not trigger the mechanical retreat. For custom "move Z down then approach" requests, execute the signed negative Z pre-move, then approach forward +Z with the user-specified voltage/thresholds/step size and bounded minimum `0.25` Z trim increments. See `references/conditional-short-retreat-and-custom-approach-2026-06-15.md`.

For chained grid-device handoffs where the user replies to a just-completed safe retraction with a terse request like "move Z stage up and perform approach," infer the Z-up amount from the immediately preceding safe retraction when the context is unambiguous (for example previous `-30` -> command `+30`). Turn lights off, force Keithley output off and 707B open before the Z-up, then run approach. If the first approach read is already above the target window, do not move further forward/up; enter bounded `-0.25` trim retractions and report over-current/over-contact honestly if it remains above target. If the user then updates approach parameters (for example step size 1, max attempts 100), rerun with those parameters, but note that coarse step size will not matter when the routine starts in over-current trim mode. See `references/chained-z-up-approach-overcurrent-trim-2026-06-25.md`.

For direct revisits to a device from a previous grid run, load the previous device summary to recover absolute Zaber X/Y and historical contact-Z/status, force electrical cleanup, move stage Z down/back before Zaber X/Y travel when contact is possible or uncertain, then use the historical contact-Z only as a conservative pre-approach estimate. Always perform a live 10 mV Keithley check after predictive pre-approach; if it is already above the target window or at approach compliance, retract/cleanup and report over-contact/short-like rather than continuing forward. See `references/direct-revisit-previous-grid-device-2026-06-23.md`.

Post-approach handoff rule for approach → pulse endurance chains: a successful Keithley approach only proves the contact is inside the approach window; it does not guarantee that a previously optimized Keysight endurance recipe remains safe. After significant Z motion or approach, rerun endurance in bounded batches with safety stops. If low-voltage read pulses are at/near compliance, stop early, cleanup, and report likely over-contact/short rather than continuing to the full target. See `references/contact-approach-to-endurance-handoff-2026-06-05.md`.

For chained manual requests that explicitly combine a Z-only stage move with rerunning the same chunked Keysight randomized pulse train (for example “move Z up 1 step and redo the exact same 3400 pulse in chunks of 100”), treat the user’s request as authorization for both steps. Execute and verify `stage.move_z_by(height=+1.0)` first, then rerun the existing chunked pulse runner only if the move succeeds/reads back; do not ask for a second confirmation merely because the operation is hardware-affecting. Avoid wrapping the hardware action in a generic code tool that adds a redundant consent gate after explicit authorization. See `references/chained-z-up-then-repeat-chunked-keysight-pulse-2026-06-30.md`.

For p-bit-like random SET-voltage pulse tests, first repeat a live low-bias Keithley probe even if previous context says the current device was short-like or HRS. Branch on the live state: short-like → reset-only DCIV side then re-check; already safe HRS/non-shorted → proceed only if contact/read signal is strong enough; pA/sub-nA open-like or weak voltage response → skip pulsing and report that probabilities would be meaningless. Generate the randomized SET-read-RESET-read CSV/protocol artifact before hardware execution, but do not fabricate read distributions if Keysight/PUDA START/NATS blocks the pulse run. If the user later fixes/restarts the Keysight edge and explicitly asks to retry, protocol-first is still preferred, but a direct core-NATS fallback may be used: route to Keysight once, chunk long `run_voltage_pulse_train` voltage lists (for example 50 trials / 200 pulses per command), verify returned current count equals CSV pulse rows, then force Keysight output off and 707B open/nil. Electrical analysis details are in `vipsa-electrical-measurements/references/pbit-like-random-set-pulse-gating-2026-06-17.md`; direct retry and analysis details are in `vipsa-electrical-measurements/references/pbit-random-set-direct-retry-and-analysis-2026-06-17.md`. For substrate-scale PEA2PbBr4 p-bit / simulated-annealing optimization, use `references/pea2pbbr4-pbit-substrate-optimization-2026-07-29.md`: treat device selection by sigmoid slope as hardware-discrete effective-temperature binning, optimize the substrate population rather than a single device, and use sequential DOE over solvent ratio/concentration → spin conditions → anneal time.

Long grid-trial live-update rule: if a long ViPSA grid run is being monitored over Telegram, do not spam per-step approach-loop messages (`approach read N`, `approach forward N`, `approach retract trim N`) unless the user explicitly asks for that detail. Report device-level moves, status changes, resistance/DCIV/pulse phases, and final approach results instead. If the user changes approach thresholds, read voltage, or compliance mid-run, stop the old process, cleanup electrical outputs/routes, verify safe switch state, archive any partial restart-device folder, prune the summary from the restart device onward, patch the continuation runner constants and `approach.json`/summary params together, then resume from unfinished devices with the updated values recorded in the run summary. After restart, verify the new runner is alive and that the first new device artifacts record the updated approach parameters; if no-recording mode is active, also verify no new `camera*_resume_*.mp4` files appear. If the reason for changing thresholds is that prior devices look pre-shorted/over-contacted, soften approach rather than continue with the normal 10–100 nA window; a working soft continuation target is `1–20 nA at 10 mV`, `0.25` stage-Z steps, and about `200 nA` Keithley read compliance. If future devices should get extra handling after `no_contact_after_max`, patch the continuation runner so each no-contact-at-max case performs a visual/alignment recheck plus a guarded sequential higher-voltage Keithley contact diagnostic (for example `0 V`, `+10 mV`, `+50 mV`, `+100 mV`, `+200 mV`, `+500 mV` at about `1 µA` read compliance), saves the per-device diagnostic JSON, then continues the existing open/weak-contact flow. If the user asks which device is currently being tested, verify from the live runner process and the active runner `OUT` directory, not from stale background notifications; the current device is the newest `device_*/summary.json` with `status: started` and no `finished_utc`, while the newest completed folder is only the last finished device. If state probes time out while the runner PID remains alive, report the device as in-progress/possibly stalled rather than inventing a measurement phase. If the user says `do not record` / `stop recording` during an active grid/resume run, treat it as an immediate instruction to stop video creation: stop the active runner, delete just-created resume video artifacts if appropriate, cleanup/verify hardware safety, patch or regenerate the continuation runner with camera `Recorder` creation and start/stop calls disabled, restart only after the no-recording patch is in place, and verify no new `camera*_resume_*.mp4` files appear. If the user wants to insert a remeasurement of a prior/poor-contact device after the current device, use a watcher that waits for the current device to finish, stops the old runner, archives and reruns the requested device, then resumes from the next normal traversal device when requested; do not leave the run paused if the user says to continue automatically. If the user instead says to skip the current device and start/restart the grid from a specific later/other device, immediately stop the active runner and any watcher/helper automation, mark the skipped device as `status: skipped` without deleting its folder, archive any stale target-device folder, generate a continuation runner with `START_AT_DEVICE=<target>`, and ensure previous manual-handoff-only logic is not accidentally reused for the new target. See `references/grid-trial-resume-live-updates-2026-06-06.md`, `vipsa-grid-measurement/references/soft-approach-grid-resume-and-contact-edge-dciv-2026-06-22.md`, `references/grid-run-no-recording-stop-and-resume-2026-06-24.md`, `references/grid-no-contact-alignment-and-higher-voltage-diagnostic-2026-06-24.md`, `references/grid-run-active-device-status-after-manual-interrupt-2026-06-24.md`, `references/grid-midrun-approach-parameter-change-2026-06-24.md`, `references/grid-insert-rerun-device-then-continue-2026-06-25.md`, `references/grid-skip-current-device-and-restart-from-target-2026-06-25.md`, and `references/fresh-substrate-grid-current-device-dciv-retry-2026-06-26.md` for starting a new substrate grid from the current contacted device while reusing a verified manual approach and applying strict reset-negative / low-current DCIV retry rules.

Grid measurement pause/stop rule: when the user asks to pause or stop a long grid measurement, stop the active grid process and immediately verify hardware safety before reporting success. Cleanup/verify the full six-machine set (`keithley-2450`, `keithley-707b`, `keysight-b2902b`, `light`, `stage`, `zaber`), force/verify SMU outputs off where applicable, run/verify `keithley-707b.open_all()` + `get_closed_channels()` (`nil`/none expected), and inspect the run folder summaries to report the last completed device and any device left in `started` state. A Keysight reset may time out while still clearing the machine to `idle` with `run_id: null`; re-read state before declaring cleanup blocked. If all PUDA/NATS state/control responses time out, report the cleanup verification as blocked/unverified rather than saying the hardware is safe; still report artifact/log evidence separately, e.g. a partial device that stopped after alignment with no approach/DCIV/pulse artifacts. See `references/grid-measurement-pause-and-cleanup-2026-06-22.md` and `vipsa-grid-measurement/references/explicit-redo-boundary-and-pause-unverified-cleanup-2026-07-01.md`.

Manual grid restart/handoff rule: when the user requests a specific physical handoff before resuming a grid run (for example "move Z down, move to device 6, move Z up, approach, then restart from there"), split the work into verified phases instead of hiding all motion/approach/measurement in one opaque runner. Archive stale device folders for the restart range so old `DONE.json` files do not skip the requested device; run the requested Z/Zaber moves and standalone approach first; **turn lights off before electrical approach/measurements unless explicitly told otherwise**; then start a continuation runner that reuses the recorded approach result for the first device rather than repeating the handoff. If unsupported `puda machine reset` calls leave `stage`, `light`, or `zaber` in `error`, recover with a harmless full-metadata protocol (`light.initialize(startup_command="off")` + `turn_off`, and/or read-only position calls) and verify `idle`/`run_id: null`. See `references/manual-grid-restart-device-handoff-2026-06-24.md`.

For long contact-approach continuation runs, do not wrap a many-minute `python3 approach_*.py` execution inside `execute_code`, because that tool has a 5-minute wrapper cap even if the nested terminal timeout is higher and can leave the Python process running. For loops with dozens of separate PUDA protocols, prefer a tracked background terminal process with `notify_on_complete=true` over foreground `terminal(timeout=600)`, because even the 600-second foreground cap can expire before the script reaches its `finally` cleanup. If a wrapper/foreground timeout occurs, immediately check for the still-running Python/PDUA PID, read the partial `summary.json`, do not repeat any Z motion blindly, then run explicit recovery cleanup/readback. If 707B cleanup is blocked by `cannot start, <old-run-id> is currently running` while state shows `idle` with a non-null run id, reset `keithley-707b`, verify `idle/run_id:null`, then rerun `open_all` + `get_closed_channels`. See `references/foreground-timeout-long-approach-cleanup-2026-07-26.md` for the concrete timeout/recovery pattern.

For paused-grid manual approach retries where the user changes the lower threshold or asks for extra attempts, first reconcile the conversational target device with the **live** physical device from Zaber X/Y and grid/alignment artifacts. If the reply chain discusses device N but live X/Y is another device, do not default to the live device and do not move Z; state the mismatch and ask whether to return safely to N or operate where the probe currently is. Once target identity is resolved, treat the retry as a bounded continuation from the verified current stage Z, not a full grid restart, unless explicitly requested. Patch the continuation runner threshold and use the same threshold in the standalone retry script; if an older killed runner later reports buffered `in_window` output under a previous threshold, classify it as stale. If the user adds an extra retry budget after a primary no-contact limit (for example “after 120 steps, retry another 100”), record the primary and extra budgets separately in `approach.json` (`primary_max_attempts`, `extra_retry_attempts`, combined `max_attempts`) and update downstream no-contact status checks; do not leave old `no_contact_after_max` as the only recognized terminal status. **Do not insert a generic `-50` or attempt-sized gross retract between subsequent approach blocks when the user has said retries should continue forward from current Z.** Keep only minimum-step negative safety trims after over-current/overshoot and a separate safe retract before any X/Y travel. If a manual approach process stalls or is killed, recover by aborting/readback of stage position plus SMU-off/open-all cleanup before continuing. For repeated low-current/no-contact retries, check no other runner is active, persist the log after every read/move, continue from the current stage-Z readback, and report final no-contact honestly instead of auto-running DCIV or pasting per-step logs. See `references/extended-low-current-approach-retry-2026-06-24.md` for the concrete 5e-10/1e-8 threshold, +0.5/+1.0 Z-step continuation pattern and concise reporting fields, `references/large-z-continuation-no-contact-2026-06-24.md` for a later +100 step-1 continuation that stayed below threshold through Z≈199.25 with verified cleanup, and `references/discussed-device-vs-live-device-approach-retry.md` for the target-identity/no-gross-retract correction.

Direct fallback timeout/stale-run pitfall: if a direct-NATS contact-approach script times out or is killed, assume the shared approach run may still be active on `keithley-2450`, `keithley-707b`, and `stage`. Probe with a harmless direct command; if START reports `cannot start, <old-run-id> is currently running`, publish direct `complete` with that exact old run id to every involved machine, then force `keithley-2450.set_output(false)`, `keithley-707b.open_all()`, verify `get_closed_channels() == "nil"`, and read stage position before retrying or reporting. During flaky NATS periods, `nats.py` `flush()` can time out even when direct publish/subscribe transactions work; fallback scripts may subscribe, sleep briefly, publish, and wait for matching response by `machine_id`/`run_id`/command instead of treating flush failure as proof the command path is unusable. Do not use legacy `-0.1` Z trims in these scripts; the minimum valid Z increment is `0.25`. See `references/direct-approach-timeout-stale-run-and-nats-flush-2026-06-24.md`.

### `keysight-b2902b`

Role: Keysight B2902B / B2901BL-family source-measure unit. The physical instrument may be described by the user as Keysight B2901BL, while the PUDA driver/machine may use B2902B-family naming. Primary use: pulse-train measurements.

Useful methods reported by `puda machine commands keysight-b2902b`:

- Session/setup: `initialize()`, `reset()`, `clear()`, `close_session()`
- Safety/output: `abort_measurement(adr=None)`, `set_output(enabled: bool)`
- Source/sense config: `set_source_function(function)`, `set_source_level(function, value)`, `set_source_range(function, value=None, auto=True)`, `set_sense_function(functions)`, `set_sense_range(function, value=None, auto=True)`, `set_protection(function, value)`, `configure_measurement_format(functions)`
- Measurements: `hold_voltage_measure_current(voltage, current_compliance, ...)`, `hold_current_measure_voltage(current, voltage_compliance, ...)`, `query_reading()`, `run_voltage_pulse_train(voltages, current_compliance, pulse_width_s, ...)`
- Switch integration: `connect_switch_path()`, `disconnect_switch_path()`
- Diagnostics: `identify()`, `get_error()`, `read_errors()`
- Position telemetry: `get_position()` returns fixed payload
- `home()` has no defined SMU homing sequence.

Keysight pulse-train pitfall: observed `keysight-b2902b.run_voltage_pulse_train()` rejects an unexpected `settle_s` keyword. For pulse trains, pass `voltages`, `current_compliance`, `pulse_width_s`, and `reset` unless live command metadata proves the driver signature has changed.

Keysight multi-command START-state pitfall: a validated protocol that coordinates `keysight-b2902b` and `keithley-707b` can successfully route to Keysight, then fail the next Keysight command with `Send START command to start a run before sending commands`; similarly, a multi-command Keysight cleanup can succeed on the first command and fail on the second. For Keysight low-bias resistance checks during this failure mode, split the workflow into short protocols: route/setup, Keysight-only read, Keysight-only output-off, and 707B-only `open_all`/`get_closed_channels`. Parse `I_meas (A)`/`Current (A)` and `V_meas (V)` from the Keysight read and compute `R = V_meas / I_meas`. If the user restarts the Keysight edge, retest the full combined protocol before continuing the split-protocol workaround; a restart has cleared this stale run-state/subscriber condition and allowed `set_output(false) → connect_keysight_smu → hold_voltage_measure_current → set_output(false) → open_all → get_closed_channels` to complete in one run. See `references/keysight-resistance-split-protocol-start-loss-2026-06-24.md` and `references/keysight-edge-restart-restores-multicommand-2026-06-24.md`.

Keysight direct-NATS stale-run/retry pitfall: during advertised-route outages, direct fallback for Keysight+707B may start successfully once, then a timed-out wrapper can leave a stale run active. If a fresh `keysight-b2902b.start` returns `RUN_ID_MISMATCH` with an old currently-running run id, publish `complete` with that exact old run id to both `keysight-b2902b` and `keithley-707b`, then retry with a fresh run id and require successful START responses before sending any pulse train. In this outage pattern, `nats://100.109.131.12:4224` has worked better for direct Keysight control than `:4223`; use subscribe-then-publish response matching and avoid depending on `flush()` during long waits. The electrical measurement details are in `vipsa-electrical-measurements/references/keysight-single-set-100read-retention-2026-06-29.md`.

Special note: `connect_switch_path()` sends the named route `keysight` to the 707B wrapper if available. `disconnect_switch_path()` currently sends `open all` because only one SMU is connected at a time.

### `keithley-707b`

Role: Keithley 707B switch matrix / routing wrapper.

Useful methods reported by `puda machine commands keithley-707b`:

- Session/setup: `reset()`, `close()`, `close_session()`
- Route safety: `open_all()`
- Channel control: `open_channel(channel)`, `close_channel(channel)`
- Named route helpers: `connect_named_route(route_name, slot=None)`, `connect_keithley_smu(slot=None)`, `connect_keysight_smu(slot=None)`
- Diagnostics: `get_closed_channels()`

Important behavior: `connect_named_route()` calls `open_all()` before closing the new route so route changes are break-before-make.

Reusable active electrical sequence for “connect DUT to Keithley SMU, start output, stop output, close/open all connections”:

1. Validate current environment and states first (`puda env current`, states for `keithley-2450` and `keithley-707b`).
2. Build and validate a PUDA protocol rather than hand-running interdependent commands when coordinating the SMU and switch.
3. Conservative command order:
   - `keithley-2450.set_output(enabled=false)` before any routing change.
   - `keithley-707b.connect_keithley_smu()`; observed route closes channels `1A01` and `1B03`.
   - `keithley-2450.set_output(enabled=true)` only after routing succeeds.
   - `keithley-2450.set_output(enabled=false)` before disconnecting.
   - `keithley-707b.open_all()`.
   - `keithley-707b.get_closed_channels()` to verify final disconnection; expected safe result is `nil`/no closed channels.
4. Final verification: both machines should return to `idle` with `run_id: null`. Report the final electrical state (output off, no closed channels) without preserving ephemeral run IDs in the skill.

Minimal protocol command list:

```json
[
  {"step_number": 1, "name": "set_output", "machine_id": "keithley-2450", "params": {"enabled": false}},
  {"step_number": 2, "name": "connect_keithley_smu", "machine_id": "keithley-707b", "params": {}},
  {"step_number": 3, "name": "set_output", "machine_id": "keithley-2450", "params": {"enabled": true}},
  {"step_number": 4, "name": "set_output", "machine_id": "keithley-2450", "params": {"enabled": false}},
  {"step_number": 5, "name": "open_all", "machine_id": "keithley-707b", "params": {}},
  {"step_number": 6, "name": "get_closed_channels", "machine_id": "keithley-707b", "params": {}}
]
```

### `light`

Role: Serial light controller.

Useful methods reported by `puda machine commands light`:

- Connection/setup: `connect()`, `initialize(startup_command='off')`, `disconnect(turn_off_first=True)`
- Light control: `turn_on()`, `turn_off()`, `set_green()`, `set_red()`, `set_rainbow()`, `control_lights(command)`
- Valid `control_lights(command)` values observed: `on`, `off`, `green`, `red`, `rainbow`, `circle`
- `circle` sends a white-light pulse/wave around the optical path by selectively and sequentially turning on LEDs on the strip; it repeats the wave 3 times. For camera capture, start the camera recording first, then send `control_lights(command="circle")`, then stop recording after the 3-wave sequence has ended.
- For exact camera-1 `circle` capture requests, do **not** add unrequested multi-second pre-roll and do **not** start the post-circle wait after waiting for the command response. Start timing immediately after publishing `circle`, collect the response asynchronously, stop capture at the requested delay, then verify a non-empty playable MP4 before sending. If direct MP4 startup produces an empty/near-empty file, capture to `.ts` and remux to MP4. See `references/camera1-circle-video-capture-2026-06-09.md`.
- Placeholder: `change_intensity(percentage)` exists but intensity control is not implemented in Arduino firmware.

Direct-NATS fallback: this is **not** the default execution path for ViPSA operations. The user explicitly prefers PUDA protocol for machine operations unless stated otherwise. Use direct/raw NATS only for read-only diagnosis, explicit user-approved fallback/cleanup, or emergency safety handling when protocol control is impossible. When authorized, and when `puda protocol run` or `puda machine state` is routed through a stale endpoint but the edge machines still respond on the active ViPSA NATS servers, use a one-command direct transaction. Probe the active NATS ports; `100.109.131.12:4223` and `:4224` can be more reliable than `:4222` for direct control. Subscribe to `puda.<machine>.cmd.response.immediate` and `.queue`, publish `start` to `puda.<machine>.cmd.immediate`, publish the driver method to `puda.<machine>.cmd.queue`, then publish `complete` to `.immediate` with the same `run_id`. In the 2026-06-09 align→approach session, plain `nc.publish(...)` on `:4223` worked for `light`, `zaber`, `stage`, Keithley, and 707B commands; do not assume JetStream publish is always required. If `nats.py` `flush()` times out during a known NATS advertised-address/reconnect issue, do not treat that alone as proof the direct path is unusable: subscribe first, sleep briefly, publish without `flush()`, and wait for matching response messages by `machine_id`/`run_id`/command name. If a machine reports `RUN_ID_MISMATCH` with a currently-running run ID and the user has authorized stale-run cleanup, publish `complete` with that exact reported run ID, then verify with a read-only command. Gate every direct-NATS transaction on a successful START response: if START fails, do not publish/interpret the queued driver command as executed, and for chained requests like Z-move→DCIV do not run electrical stress unless the Z move returns success and is read back/verified.

Duplicate-start exception: in a direct fallback transaction, if the `start` response is `RUN_ID_MISMATCH` and the error message says the **same fresh run_id** is currently running, this can mean the edge accepted a duplicate START for the same run. Do not loop the same failing protocol runner. Prefer core NATS `nc.publish` over JetStream publish, proceed only if subsequent queued commands under that same run_id succeed, and still complete/cleanup. See `references/direct-contact-check-protocol-runner-duplicate-start-2026-06-13.md` for the contact-check fallback recipe and reporting standard.

Duplicate/stale subscriber recovery: after an outage, a machine can show `idle`/`run_id: null` and accept `START`, but the queued driver command can still return `RUN_ID_MISMATCH` / `expected active run`, likely because the command hit a stale duplicate subscriber. Treat this as a PUDA control-path/run-state issue, not a physical/electrical result. For resumed direct-NATS fallback, use short fresh per-command transactions (`start` → one queued command → `complete`), complete any old run ID mentioned by `cannot start`, retry the whole transaction with a fresh UUID on queued-command `RUN_ID_MISMATCH`, and bound per-attempt timeouts for fast commands so long grid runs do not hang silently. See `references/direct-nats-duplicate-subscriber-run-state-recovery-2026-06-24.md`.

See `references/direct-nats-command-path-and-align-approach-edge-2026-06-09.md`, `references/direct-nats-run-id-mismatch-z-dciv-2026-06-10.md`, and `references/puda-protocol-first-and-nats-layer-debug-2026-06-10.md` for transaction, stale-run cleanup, layered diagnosis, and reporting patterns. See `references/nats-advertise-direct-light-resistance-approach-2026-06-29.md` for the WSL/Tailscale advertised-route outage pattern where PUDA CLI follows unreachable `192.168.50.6` URLs, but bounded direct light/resistance/approach commands can still be verified by response subjects without relying on `flush()`. See `references/pea-signed-current-and-direct-approach-cleanup-2026-06-29.md` for PEA signed-current interpretation and direct cleanup verification after a contact approach.

Protocol pattern learned for simple light toggles:

```json
[
  {"step_number": 1, "name": "turn_on", "machine_id": "light", "params": {}},
  {"step_number": 2, "name": "turn_off", "machine_id": "light", "params": {}}
]
```

A one-step `turn_on` or a two-step `turn_on` → `turn_off` sequence validates with `puda protocol validate` and runs successfully with `puda protocol run`; response data returns `{ "result": true }` for both commands and `light` returns to `idle` with `run_id: null`. For these simple generated protocols, validation can be done from anywhere, but run the protocol from the ViPSA project directory (`/home/vipsa/vipsa-puda-project`) so the CLI can find the project `puda.config`; otherwise `puda protocol run` may fail with `project puda.config file not found in current directory` even though validation passed. For terse `turn on lights` requests after electrical cleanup, keep the scope to a one-command `light.turn_on()` protocol and final `light` state verification; do not add camera/snapshot work unless requested. See `references/simple-light-on-after-electrical-work-2026-06-30.md` for the concise verified reporting pattern.

Light stuck-active recovery: if a light protocol fails at START with `cannot start, <old-run-id> is currently running`, check `puda machine state light`. A light state can report `idle` while still carrying a stale non-null `run_id`; that stale `run_id` can still block protocol START, so treat `idle + run_id != null` as requiring cleanup before retrying. If a light-only protocol on local ViPSA NATS starts but the queued command fails with `Send START command to start a run before sending commands`, inspect for duplicate light edge subscribers/processes (for example two `/home/amdm/workspace/ViPSA/light` `main.py` processes from a manual `start_all_edges.sh`). Stop the duplicate edge set, restart only the light edge if it no longer responds to START, complete any stale active run id, then retry a fresh `start` → `turn_on`/`turn_off` → `complete` transaction and verify `puda --nats-servers nats://127.0.0.1:4222 machine state light` returns `idle`/`run_id:null`. If the user asks to reset the connection, `puda machine reset light` may clear the stale `run_id` but return `Unknown or restricted command: reset` and leave the machine in `error`. Recover with a validated PUDA protocol containing `initialize(startup_command="off")` followed by the user's intended final command: `turn_off()` for an off/recovery request, or `turn_on()` for a lights-on request. Then verify `light` is `idle` with `run_id: null`. If normal protocol-run routing is itself blocked but raw NATS responses expose a stale run id, complete that exact stale id on `puda.light.cmd.immediate`, then retry a fresh direct/raw `start` → queued `turn_off` → `complete` cleanup and require `turn_off` `data.result: true`; this is a cleanup fallback, not the default control path. For simple lights-on requests where the full-metadata protocol validates but fails before execution because of the known NATS timeout/advertised-address issue, a direct no-flush transaction can be used and must be verified by queued `turn_on` success plus final `puda --nats-servers <single-server> machine state light` returning `idle`/`run_id: null`; see `references/light-on-protocol-timeout-direct-noflush-2026-06-29.md`. Also see `references/light-stuck-active-recovery-and-camera-release-2026-06-10.md` and `vipsa-image-capture/references/camera2-snapshot-stale-light-direct-cleanup-2026-06-23.md`.

For timed light patterns shorter than PUDA protocol step granularity (for example “flash green twice, 0.5 seconds on”), run small single-command protocols sequentially from an outer script and use local `sleep` between PUDA runs. Verify each run succeeded before continuing so the final state is safe (`turn_off` if the sequence fails).

For user requests like “run rainbow on the lights,” “turn the lights on, wait 5 seconds, then green, then rainbow,” or typo-filled terse requests like “turn the lighrs green and rhen rainbow,” treat it as an immediate simple light-control task (not a documentation/reporting task) and do not ask for clarification. Do **not** reinterpret a lights-only sequence as a camera-capture/snapshot task; only capture images if the user explicitly asks for camera/snapshot/image output. Do not try to invent a protocol-level wait unless live commands show one exists. Use separate validated/runnable light commands with an outer sleep only when the user requested a delay. For a standalone “rainbow” / “run rainbow” request, run a one-step full-metadata PUDA protocol with `light.set_rainbow()`, then verify `puda machine state light` is `idle` with `run_id: null` and report `data.result: true` if present. Use `printf '%s\n' '--- marker ---'` rather than bare `printf '--- marker ---\n'` in shell scripts to avoid Bash treating a leading `--` in the format as an option. Sequence outline:

1. `turn_on` if requested
2. local `sleep <seconds>` only if requested
3. `set_green`
4. `set_rainbow`
5. verify `puda machine state light` returns `idle` and report final intended pattern/color (rainbow for green→rainbow sequences)

If any step fails, attempt `turn_off` unless the user explicitly requested lights remain on/patterned, and report the failure rather than continuing the color sequence blindly.

For user requests like “turn on the lights, take snapshot with both cameras, then turn off the lights and display the images,” use the lighted camera snapshot workflow in `references/lighted-camera-snapshots.md`: turn lights on via PUDA, capture stills from the existing MediaMTX RTSP camera streams (prefer RTSP/TCP over direct DirectShow when the cameras are already being streamed), turn lights off in a cleanup path, verify the light is idle, then attach the non-empty image files with `MEDIA:`.

For status questions like “is light on now?”, do **not** infer lamp on/off from `puda machine state light`; that state only says whether the light edge is executing a command. Use the existing camera stream as the observable truth: open the MediaMTX WebRTC/HLS/RTSP camera feed, inspect whether the sample area is brightly illuminated or dim, and report both the PUDA execution state and the visual evidence. See `references/light-state-visual-check.md`.

When using Windows `ffmpeg.exe` from WSL for these snapshots, pass the output path as a Windows path such as `C:\\Users\\amdm\\AppData\\Local\\Temp\\name.jpg`; then verify and attach the equivalent WSL path `/mnt/c/Users/amdm/AppData/Local/Temp/name.jpg`. Passing a `/mnt/c/...` path directly to `ffmpeg.exe` can fail with Windows-side `Permission denied`.

Camera release/restart pattern: if the user asks to release camera 1 or camera 2, identify the Windows `ffmpeg.exe` publisher that holds the physical DirectShow device, not the completed one-shot snapshot process. Query `Win32_Process` for `ffmpeg` commands containing `camera1`/`camera2` and stop only the matching publisher PID; verify the target camera publisher is gone and any other requested camera stream remains running. If the user later asks to restart the stream, PowerShell `Start-Process` quoting can be brittle; a reliable fallback is to start the Windows ffmpeg binary directly from WSL as a tracked background process publishing DirectShow → RTMP/MediaMTX, then verify RTSP with a one-frame capture before using it. See `references/light-stuck-active-recovery-and-camera-release-2026-06-10.md` and `references/camera-publisher-restart-release-and-lighted-snapshot-2026-06-12.md`.

### `stage`

Role: Arduino stage controller.

Useful methods reported by `puda machine commands stage`:

- Safety/setup: `abort_motion()`, `set_zero()`, `go_to_zero()`, `disconnect()`
- Position: `get_current_position()` returns `(x, y, z)` or `(None, None, None)` if disconnected
- Relative motion: `move_x_by(steps)`, `move_y_by(steps)`, `move_xy_by(stepsX, stepsY)`, `move_z_by(height, feedrate=450)`
- Absolute XY motion: `move_xy_to(x_pos, y_pos)`
- Bounded motion: `move_with_lim_by(stepsX, stepsY)` returns `None` on success, `-1` when movement exceeds limits, `0` when not connected/failure

### Stage no-motion despite successful command

When `stage.move_z_by` reports success but no physical motion is visible:

1. Record Camera 2 and quantify before/after image displacement.
2. Inspect edge logs for exact G-code, GRBL `ok`, and `<Idle|MPos:...>` change.
3. If GRBL accepts G-code and changes `MPos` but Camera 2 shows no displacement, PUDA/NATS/edge/serial delivery is working. Prioritize motor power, ENABLE/SLEEP/RESET, Z driver, Z-motor wiring/coils, and mechanical coupling. GRBL is open-loop: `MPos` does not prove shaft motion.
4. With the edge stopped, read `?`, `$I`, `$G`, and `$$`; then restart exactly one Stage edge.
5. Do not issue progressively larger moves while physical movement is unverified.

Safety pitfall: inspect the live `Stage.abort_motion()` implementation before use. The current ViPSA driver sends `!` followed by `G90 G1 Z0 F100`; this is an absolute Z move, not a harmless hold clear. Do not use it for diagnostic cleanup until corrected and validated.

Important behavior: `disconnect()` moves to zero before disconnecting.

For an explicitly requested Stage-Y round-trip jog (for example `+10` then `-10`), use one sequential two-command protocol, require success for each signed move, then run a separate position-read protocol and verify final idle/null state. Do not claim the final coordinate proves return to the starting point unless a pre-move readback was captured; the command pair only establishes an algebraic net displacement of zero. The PUDA runner supplies START/COMPLETE lifecycle messages automatically rather than as driver commands in the protocol array. See `references/manual-stage-y-round-trip-jog.md`.

Operational pattern for Z-only microscope stage moves:

- In the user's current ViPSA convention, **Down** means backward Z / negative signed height. A request like `move stage z down 200 steps` maps directly to `stage.move_z_by(height=-200, feedrate=450)`.
- For terse requests like `move z down by 30 steps`, act directly and keep scope to the `stage`: check active env/CLI and `stage` idle, generate a full-metadata one-command protocol, validate it, run it from `/home/vipsa/vipsa-puda-project`, then verify with a separate position read and final `stage` state. Do not ask for clarification when axis, direction, and step count are explicit.
- If a stage Z protocol fails at START with `cannot start, <old-run-id> is currently running`, treat it as a stale run, not as executed motion. `puda machine reset stage` may report `Unknown or restricted command: reset` and transient `state: error` while still clearing the stale `run_id`; immediately re-read state, retry the validated stage protocol, then verify with a separate `get_current_position()` readback. Only report motion after the retry command succeeds and readback/state verification completes.
- If the local terminal/client is interrupted during `puda protocol run`, do **not** assume the physical move failed and do not repeat it blindly. Preserve the pre-move readback and run artifacts, recover stale state if needed, then issue a fresh read-only `get_current_position()` protocol and compare the signed delta. Continue a chained alignment only after the requested delta is verified; stop on partial/unexpected deltas. See `references/interrupted-stage-motion-reconciliation.md`.
- Verify `stage` is idle before moving, run a protocol with `move_z_by`, then verify final `puda machine state stage` is idle. If position readback is needed, prefer a fresh separate `get_current_position` protocol after the move; a combined `move_z_by` → `get_current_position` protocol can execute the move but fail the readback step with `Run ID mismatch: expected active run`. See `references/stage-z-move-position-readback-2026-06-24.md` for a concrete verified example.
- If the separate position read returns numeric values, report the readback compactly (for example `x=0, y=0, z=-30`) alongside the signed commanded move and final `idle`/`run_id: null` state. If it returns `[null, null, null]`, report that the driver returned no numeric X/Y/Z readback rather than inventing a coordinate; the motion can still be confirmed by the successful `move_z_by` response plus final idle state.
- If the user or video evidence says the stage motor is not physically moving, do **not** treat a successful `move_z_by` response or tracked Z readback as physical-motion confirmation. Stop further motion unless explicitly asked, mark tracked Z as untrusted, and follow `references/stage-command-success-vs-physical-motion-2026-06-25.md`.
- Stage driver pitfall confirmed 2026-07-28/29: the PUDA stage edge can report `move_z_by` success and increment `get_current_position()` from internal counters even when the stage is not physically moving. Raw GRBL over `/dev/openflexture` can move the stage, and a direct Python script importing `Stage` from `/home/amdm/workspace/ViPSA/stage/driver.py` can also move it, while the PUDA edge path may fail to produce physical motion. Treat this as evidence of an edge-runtime/serial-handshake/status-verification issue, not a hardware motor failure or instruction to bypass the driver. PUDA should call `Stage` methods; it should not write G-code directly. If motion is questioned, stop approach loops, use visual verification and/or temporary `Stage.move_z_by` serial logging (`in_waiting_before`, exact G-code repr, GRBL `ok/error`/`<Idle|MPos...>` lines), and quiet verbose logging afterward because the user prefers concise updates unless asked. For the debug recipe, direct-driver verification script, verbose edge serial logging, stale GRBL banner/input-buffer observation, and reporting format, see `references/stage-edge-vs-direct-driver-motion-debug-2026-07-29.md`, `references/stage-edge-serial-driver-debugging-2026-07-29.md`, and `references/stage-edge-serial-stale-buffer-and-motion-verification-2026-07-29.md`.
- If protocol execution fails at NATS connection/setup, stop and report that the validated protocol did not run; do not silently retry with direct/raw NATS unless the user explicitly authorizes fallback.
- If `puda protocol validate` succeeds but `puda protocol run` or `puda machine state` times out on NATS, retry once with a single known ViPSA NATS server override and separately probe TCP reachability only as diagnosis. TCP `open` does **not** prove the command executed. For physical Z motion, only report success when a PUDA/direct response confirms `move_z_by` and position/state verification completes; otherwise report “no confirmed stage motion.” If the user asks to diagnose rather than fix, keep checks read-only and distinguish TCP-open, raw NATS PONG, PUDA read-only health, Tailscale packet loss/DERP path, and unreachable advertised NATS `connect_urls`; see `puda-operations/references/nats-connectivity-diagnosis-no-fix-2026-06-30.md`. See `references/stage-motion-nats-timeout-and-stale-tasklist-2026-06-18.md`.
- Local ViPSA-Ubuntu recovery for a removed/stale NATS peer: if `tailscale ping <old-nats-ip>` says `no matching peer`, MagicDNS for `bears` fails, local edge logs show repeated `puda.edge_nats_client` connection errors to the old IP, and the user asks to resolve rather than merely diagnose, a bounded protocol-first recovery is to run a local JetStream NATS (`nats-server -js -sd ~/.local/share/puda-nats -p 4222`), set `puda config set nats_servers nats://127.0.0.1:4222`, patch the relevant ViPSA edge `.env` `NATS_SERVERS` to localhost, restart only the needed edge(s), then verify with a read-only protocol before any move. This restores PUDA START/command/COMPLETE semantics locally but does not by itself prove physical motor motion beyond the driver response/readback. See `references/local-jetstream-nats-recovery-for-stale-vipsa-peer-2026-07-27.md` for the detailed recovery checklist and Tailscale direct-vs-DERP interpretation notes.
- For terse manual stage-Z jogs followed by light-on commands, use the compact protocol-first pattern in `references/manual-stage-z-and-light-commands-2026-06-24.md`: verify idle, run a one-command `move_z_by`, read position with a separate protocol, retry readback once with a single known-good NATS server if only the readback connection flakes, and report concise verified results.
- For combined requests to update PUDA, run a simple Stage-Z jog, and capture camera 1 when the remembered ViPSA project path is missing, use the temp-project workflow in `references/temp-project-stage-z-and-cli-update-2026-07-25.md`: pipe `y` into `puda update`, verify the new version, treat “No project skills to update” as a successful `puda skills update` check, create a temporary PUDA project for full-metadata stage/light protocols, use the known ViPSA NATS override, verify stage readback/state, and wrap camera light control in cleanup.
- For requests to video-record a manual Z jog (for example “move Z down by 25 steps and send a video”), use `references/stage-z-motion-video-capture-2026-06-24.md`: turn light on, start an OpenCV RTSP recorder before the PUDA motion, execute one signed `stage.move_z_by`, include short post-roll, verify non-empty MP4/frame count, run separate position readback, turn light off, verify stage/light idle, and attach `MEDIA:/absolute/path.mp4`.
- Report concise signed motion and position readback; do not mention X/Y unless they changed.
- For singular stage commands, `puda machine run` can be used but the edge still requires an active run lifecycle: `puda machine start stage --run-id <uuid>` → `puda machine run stage <command> '<params>' --run-id <same uuid>` → `puda machine complete stage --run-id <same uuid>`. If `machine run` returns `Send START command to start a run before sending commands` immediately after a successful start, check for duplicate `stage/main.py` edge processes. Stop duplicate stage edges, restart exactly one stage edge, complete any stale active run ID, then retry. Verify with `get_current_position` before/after and final `stage` idle/null state.
- `puda machine run` may print only “command completed successfully” and omit the command response payload, including `get_current_position()` coordinates. When numeric Stage-Z evidence is required, follow the singular move with a separate full-metadata, read-only `puda protocol run` from a valid PUDA project so the response payload is printed/logged. Do not invent a pre-move coordinate from the signed delta when the pre-read payload was hidden; report the verified post-move tracked Z and final `idle`/`run_id: null`. Keep the established caveat that this driver coordinate is software-tracked, not independent proof of open-loop physical motion.

Operational pattern for Z-only microscope stage moves with lights:

```json
{
  "commands": [
    {"step_number": 1, "name": "turn_on", "machine_id": "light", "params": {}},
    {"step_number": 2, "name": "move_z_by", "machine_id": "stage", "params": {"height": -50}},
    {"step_number": 3, "name": "turn_off", "machine_id": "light", "params": {}}
  ]
}
```

This pattern was validated with `puda protocol validate` and `puda protocol run`; both `light` and `stage` returned to `idle`. Keep X/Y params absent unless explicitly requested.

### `zaber`

Role: Zaber X/Y stages.

Useful methods reported by `puda machine commands zaber`:

- Connection/setup: `disconnect()`, `get_devices()`, `configure_units(distance_units=None, velocity_units=None, acceleration_units=None)`, `get_default_units()`
- Position: `get_current_position(units=None)` returns X/Y positions as telemetry
- Motion: `move_x_by(distance, units=None)`, `move_y_by(distance, units=None)`, `move_x_to(position, units=None)`, `move_y_to(position, units=None)`
- Motion tuning: `set_maxspeed_x(speed, units=None)`, `set_maxspeed_y(speed, units=None)`, `set_acceleration_x(acceleration, units=None)`, `set_acceleration_y(acceleration, units=None)`, `set_holding_current(current=50)`

Important behavior: if units are omitted and class default is `None`, commands use native controller units. Ask for or confirm axis/direction/units before moving when the user does not specify them.

When the user says **microsteps** or **native units**, encode `units: null` in the PUDA protocol params. Do not use `units: "mm"` unless the user explicitly asks for millimetres. See `references/zaber-native-motion.md` for the native-unit workflow and protocol template.

For manual Zaber jogging, offer button choices when possible (for example `⬅️ X -100`, `➡️ X +100`, `⬆️ Y +100`, `⬇️ Y -100`) and execute the selected signed native-unit move directly. See `references/zaber-manual-jog-and-position.md` for the jog-button workflow and position-recording pattern.

When the user asks to return to the “last tested device” after a known manual Zaber offset, reconstruct the prior target from the latest verified Zaber readback plus the inverse of the offset, state the calculated coordinates, then use absolute native-unit `move_x_to` / `move_y_to` after any requested safe Stage-Z down/retraction. Read back both Stage-Z and Zaber X/Y and verify both machines idle. See `references/manual-offset-return-to-last-tested-device-2026-06-30.md` for the concrete X/Y reconstruction and return sequence.

For a browser-hosted manual jog control panel, use the pattern in `references/manual-web-jog-panel-2026-06-08.md`: a small Python stdlib `ThreadingHTTPServer` with the existing MediaMTX `camera1` page in an iframe, server-side PUDA command endpoints for Zaber/Stage jogs and optional light on/off buttons, Zaber native units by default, read-position buttons for verification, and Stage X/Y buttons disabled behind an explicit enable checkbox. When the panel is opened from another device, do not embed `localhost` camera URLs; use the same reachable host/IP as the camera links. Verify the page and read-only position endpoints before reporting success; do not test real jog moves or light toggles unless the user explicitly requests them. For restoring the current deployed panel, starting it on port 8765, and verifying Start/Complete plus read-only Stage/Zaber position endpoints without motion/light side effects, see `references/manual-jog-panel-restore-and-readonly-verification-2026-06-26.md`. If the panel loads but the camera viewport is blank while MTX streams work, treat the iframe host as stale until proven otherwise: probe the current camera WebRTC URL, patch `CAMERA1_URL`, run the panel from its `.venv` with `nats-py`, and verify the iframe `src` plus video element. For backup-panel restores, stale camera iframe fixes, `nats-py` venv setup, and adding a dark low-bias **Quick resistance check** button that runs the canonical Keithley/707B diagnostic without requiring Start, see `references/manual-jog-panel-quick-resistance-button-2026-07-26.md`.

Manual panel lifecycle gating is documented in `references/manual-jog-panel-run-controls-2026-06-12.md`: Start creates a shared manual `run_id` and sends PUDA `start` to all ViPSA machines, Complete sends `complete` and disables the panel, Reset-all calls `puda machine reset` for all ViPSA machines, and all jog/light/read controls stay disabled until Start succeeds.

For multi-device/grid runs with live updates, report coarse physical/electrical events (safe Z retract, Zaber X/Y travel, alignment, post-align pre-approach, routing, resistance/DCIV/pulse phases, device status changes), but **do not spam per-step contact-approach loop updates** such as every `approach read N`, `approach forward N`, or trim-retract step. Default grid travel order is `stage.move_z_by(-50)` → Zaber X/Y target → vision align → `stage.move_z_by(+40)` → electrical approach unless explicitly overridden. Report the final approach status/result for each device instead. This matches the user's explicit correction from a grid trial: “do not spam me with approach steps.”

For Zaber position readback, parse X/Y from `response.data.x` and `response.data.y`; do not assume a `response.data.result` wrapper. When asked to record a position, capture both native/default units and `units: "mm"`, record the values in the PUDA project log, and report final `zaber` state.

If a prior run leaves Zaber `active` with an old `run_id`, and `puda machine reset zaber` returns `Unknown or restricted command: reset` / transient `state: error`, try a harmless full-metadata PUDA protocol containing `zaber.get_current_position(units=null)` before giving up. A successful read-only start/complete can restore `zaber` to `idle`; verify `idle`/`run_id: null` before any motion. Details: `references/zaber-stale-active-readonly-recovery-2026-06-22.md`.

Light stuck-active cleanup and camera publisher release details are captured in `references/light-stuck-active-recovery-and-camera-release-2026-06-10.md`; use them when light reports a stale active run, `machine reset light` leaves `state=error`, or the user asks to release a camera stream.

Contact approach final trimming detail is captured in `references/contact-approach-final-trim.md`; use it when implementing the bounded final high-current guard loop. The standard defaults and validated one-command-protocol orchestration pattern are summarized in `references/contact-approach-defaults-run.md`. For post-alignment “turn off lights and perform approach” sequences using established defaults, see `references/post-align-lightoff-approach-2026-06-06.md`. Additional 2026-06-05 align/approach/resistance session notes, including Windows-ffmpeg path handling and interrupted-run resume checks, are in `references/session-2026-06-05-align-approach-resistance.md`. For stage-heavy electrical approach loops, explicitly wait for `stage` to return `idle` after every `move_z_by`; see `references/stage-state-wait-between-z-moves-2026-06-09.md` for the PUDA START-conflict recovery pattern.

Protocol patterns learned:

```json
{
  "step_number": 1,
  "name": "get_current_position",
  "machine_id": "zaber",
  "params": {"units": "mm"}
}
```

The `units: "mm"` parameter works for `get_current_position`, returning X/Y in millimetres.

```json
{
  "step_number": 1,
  "name": "move_x_by",
  "machine_id": "zaber",
  "params": {"distance": 500, "units": "mm"}
}
```

A `move_x_by` request for `distance=500`, `units="mm"` was rejected by the controller with `BADDATA: The command's data was incorrect or out of range`; the stage position remained unchanged and the machine returned to `idle` after a follow-up read.

## How to update this skill as learning accumulates

After any real ViPSA operation, patch this skill with:

- exact command used
- machine(s) affected
- observed output/status
- operational pitfall or safe default learned
- whether the action is read-only or physically/electrically active

Do **not** store ephemeral run IDs, transient timestamps, or one-off experiment results here unless they teach a reusable operation pattern.
