# Manual jog panel run controls — 2026-06-12

## Trigger

Use this when maintaining the ViPSA manual jogging web panel or any direct/manual-control UI that operates PUDA machines outside a normal static protocol.

## User requirement captured

The panel should not allow jog/read/light hardware controls until the operator explicitly starts a manual-control run. It should expose:

- **Start**: begin a fresh shared manual run to avoid `run_id` conflicts.
- **Complete**: end that manual run and disable the panel again.
- **Reset all**: reset all ViPSA PUDA machines and clear panel session state.

Start should send a PUDA `start` command to every machine directly used by the panel controls. For the current manual jogging panel this is:

```text
light
stage
zaber
```

Reset-all still targets the full ViPSA set (`keithley-2450`, `keithley-707b`, `keysight-b2902b`, `light`, `stage`, `zaber`). Do not require non-panel electrical machines for Start/Complete: if one of them is stale/offline (for example `keysight-b2902b` timing out on START), the jog panel would remain locked even though the actual jog/light machines are healthy. Complete should send `complete` to the same panel machines with the active run id.

## Implementation pattern

PUDA CLI may not expose standalone `puda machine start` / `puda machine complete` even though `puda protocol run` sends those lifecycle commands internally. For a manual panel that must hold a run open across button clicks:

1. Generate one UUID `run_id` on Start.
2. Publish the normal PUDA machine lifecycle `start` command over the same NATS command subjects the machines consume.
3. Store the active `run_id` server-side.
4. Reject or disable all hardware endpoints unless an active manual run exists.
5. Send all panel actions under the active `run_id`.
6. On Complete, send lifecycle `complete` to all relevant machines and clear the server-side active session.
7. On Reset all, run `puda machine reset <machine_id>` for every ViPSA machine, then clear session state regardless of individual reset outcomes.

## UI gating rules

- Before Start: only Start and Reset all should be available; jog/read/light controls disabled.
- After Start succeeds on all required machines: enable panel controls.
- Stage X/Y controls still require the separate explicit safety checkbox after Start.
- After Complete or Reset all: disable the panel again.

## Verification

After code changes, verify without moving hardware:

1. Start the panel server and confirm the page shows Start / Complete / Reset all controls.
2. Confirm jog/read/light controls are disabled before Start.
3. Exercise Start → Complete with no jog/motion.
4. Verify every ViPSA machine returns `idle` and `run_id: null`.
5. Confirm reset errors are surfaced in the UI instead of silently ignored.

## Pitfall

Do not implement Start as just a browser/UI boolean. The important part is the PUDA lifecycle: a real `start` must reserve the machines under a fresh run id, and `complete` must clear that exact run id. Otherwise later protocols can hit `run_id_mismatch` or manual commands can collide with automated runs.
