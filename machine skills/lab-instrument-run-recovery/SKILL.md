---
name: lab-instrument-run-recovery
description: "Use when a live lab run is interrupted or loses hardware."
version: 1.0.0
metadata:
  hermes:
    tags: [lab-automation, recovery, partial-data, usb, safety]
---

# Lab Instrument Run Recovery

## Scope

Use when a live instrument run is interrupted, externally terminated, loses an instrument/USB session, leaves stale run IDs, or returns only part of a multi-operation protocol. The goal is to preserve completed history, establish a safe state, and resume only from a scientifically defensible boundary.

## Recovery order

1. **Stop orchestration and detect survivors.** Check whether shell wrappers, Python children, or instrument commands remain active. A terminated tracked process does not prove its child or native instrument sweep stopped.
2. **Inventory artifacts before retrying.** Enumerate returned raw responses, per-operation CSV/JSON files, partial summaries, and operation indexes.
3. **Classify each operation:**
   - `completed_verified`: exact expected record count and saved artifact;
   - `not_started`: no command evidence and no stress;
   - `outcome_unknown_after_possible_partial_stress`: command may have started but no complete trace returned;
   - `failed_before_hardware_action`: routing/preflight/control rejection before stress.
4. **Force a safe electrical state.** Command outputs off, open the switch matrix, and require a real closed-channel readback of `nil`/empty.
5. **Recover instrument control.** Clear stale logical state, repair only the affected edge/session, and verify harmless hardware control before measurement.
6. **Reconcile mechanical state by readback.** Never repeat a move merely because the CLI returned an error; compare exact before/after positions first.
7. **Resume only from the first defensible missing boundary.** Never repeat completed stress. Obtain explicit authorization before repeating an in-flight operation classified as possible partial stress.
8. **Write a fresh run directory.** Link the interrupted source and merge artifacts only after preserving provenance and operation indexes.

## Partial-operation ledger

For every operation preserve:

- operation index and phase;
- commanded endpoint/compliance/timing;
- expected and returned record counts;
- raw and normalized file paths;
- instrument timestamps where available;
- completion classification;
- whether a retry would repeat possible stress.

A missing CSV after process termination is not proof of zero stress. Conversely, a route failure before the sweep command is evidence that no electrical stress occurred.

## Cleanup verification pitfall

Do not treat missing data as a safe matrix state. This anti-pattern is unsafe:

```python
verified = str(closed_channels).lower() in ('nil', 'none', '[]', '')
```

If the query failed and `closed_channels is None`, it falsely verifies safety. Require all of:

- `open_all` command status is success;
- `get_closed_channels` command status is success;
- the returned hardware value is explicitly `nil`, empty list, or the instrument’s documented open-state token;
- affected machine is idle with null run ID.

## USB/VISA session recovery

When an edge responds over the message bus but hardware writes return a disconnect/stale-session error:

1. Do not rerun measurement.
2. Verify the instrument resource is visible to the OS/VISA layer.
3. Reset logical PUDA state, but do not assume that recreates the driver session.
4. If harmless hardware verification still fails, restart **only the affected edge process**.
5. Stop every wrapper/child belonging to that edge and confirm no duplicate owner remains.
6. Start exactly one replacement edge and wait for fresh queue/immediate subscriptions.
7. Verify with harmless commands such as matrix `open_all` plus closed-channel readback.
8. If the resource is absent, stop and request physical replug/power-cycle.

## Mechanical command reconciliation

Message-bus or database errors can disagree with physical execution. If a move transaction reports rejection, timeout, or stale-run confusion:

- do not resend immediately;
- complete/clear the exact visible run when possible;
- obtain a fresh position readback;
- if the observed delta equals the authorized move, mark it completed and never repeat it;
- if unchanged, retry only after state is idle/null;
- if ambiguous, stop rather than accumulating motion.

## Grid-run safety after repair or collision

For a newly recommissioned positioning system, begin with the current device only when possible:

- preserve current lateral alignment;
- prohibit lateral travel in the first bounded run;
- complete or safely stop the current-device electrical sequence;
- cleanup and retract;
- pause before the first broad X/Y move until installed-system physical clearance and conservative bounds are verified.

## User stop decision

When the user chooses to stop a partial device:

- combine only verified completed operation rows;
- generate a partial plot clearly labeled with the completed operation range;
- record the first missing/in-flight operation and its uncertainty;
- record zero completed endurance cycles if endurance never began;
- verify cleanup and final mechanical positions;
- update the project log with a link to the partial run.

## Reporting

Use concise, auditable wording:

- what completed;
- what may have partially stressed;
- what was not repeated;
- cleanup evidence;
- final stage/coarse-stage positions;
- whether lateral motion occurred;
- exact fresh or partial artifact directory.
