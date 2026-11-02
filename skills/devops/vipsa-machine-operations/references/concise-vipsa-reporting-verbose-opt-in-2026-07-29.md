# Concise ViPSA operations reporting and verbose opt-in (2026-07-29)

## Trigger
Use for ViPSA machine operations, approach loops, alignment/approach handoffs, stage-edge debugging, resistance checks, and grid device updates.

## Rule
Default to concise, tool-verified updates. Do not send verbose per-step logs, large JSON blocks, or streaming step updates unless the user explicitly asks for them.

## What to report by default
- Requested action executed or blocker encountered.
- Key numeric result(s): current/resistance, target/device, offset/residual, stage/Zaber readback where relevant.
- Cleanup and final machine state evidence: outputs off, 707B open/nil, `idle/run_id:null`.
- Attach the relevant image/media only when it helps or was requested.

## When verbose is appropriate
Only include detailed edge logs, GRBL serial output, or every approach read/move when the user explicitly asks for verbose output/audit/debug logs. If verbose logging was temporarily enabled for debugging, turn it back into concise reporting afterward.

## Example concise forms
- “Moved Z down `20` via PUDA; stage idle/null.”
- “Quick resistance check: ±10 mV hit `1 µA` compliance; 707B nil; outputs off.”
- “🎯 Device 10 aligned, residual `2.82 px`. 👇 Approach ended over-current at `~1 µA`; cleanup verified.”
