# Minimal machine ownership for electrical-only DCIV retries

Use this when a Pratap-style forming/SET/RESET runner needs only a Keithley 2450 and 707B, but a shared helper's default `MACHINES` list also contains light, stage, Zaber, or a second SMU.

## Failure pattern

A runner can fail before routing or electrical stress when it opens a Direct context over the entire rig and then performs a metadata-only `stage.get_current_position()`. A stale/unresponsive mechanical edge can time out even though the required electrical pair is healthy. If the run summary has `cycles: []` and no raw/CSV cycle artifact, record that no DCIV cycle was acquired; do not imply a completed or partially completed sweep.

## Durable fix

1. Own only machines whose commands the runner will actually issue. For a Keithley-2450 + 707B DCIV path, use a Direct context over exactly those two machines.
2. Replace broad shared cleanup helpers with task-specific cleanup limited to the owned set:
   - Keithley 2450 output off
   - 707B `open_all`
   - verify closed channels are `nil`
3. Do not include stage, Zaber, light, or another SMU merely to collect metadata or reuse a broad helper.
4. Preserve the most recent verified mechanical readback in metadata with its source and timestamp/context. Never fabricate a fresh readback and never restart a mechanical edge just to satisfy electrical-run metadata; restart may erase software-origin coordinates without physical motion.
5. Read-only `puda machine state` snapshots may be stored as best-effort observability, but stale timestamps must not block an otherwise safe electrical-only run.
6. Before retrying after a pre-sweep orchestration failure, verify instrument identity, drain/check the Keithley error queue, force output off, open/verify the 707B, and use a fresh output directory.

## Very-high-HRS contact interpretation

Do not reject contact from pA/nA magnitude alone. A plausible very-high-HRS contact is supported when paired safe biases show:

- current polarity following voltage polarity;
- differential current scaling with the bias span (for example, approximately 5× from ±10 mV to ±50 mV);
- closely agreeing differential resistance across the two bias pairs.

An offset-dominated path that retains one current sign is more open-like. Record both the script's coarse classification and the operator interpretation/evidence in metadata.
