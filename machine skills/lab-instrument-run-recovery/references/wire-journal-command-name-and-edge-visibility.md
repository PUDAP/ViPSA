# Wire-journal decoding and edge visibility after EOF

Use this addendum when a dispatched instrument command loses its NATS reply.

## Decode the actual deployed command

- Decode each `wire.jsonl` `raw_b64` envelope programmatically.
- Summarize machine, command name, step, response status/code, and result data keys.
- Match the real deployed command name (for example `source_voltage_measure_current_continuous_segments`) rather than searching only for a generic “continuous batch” phrase.
- A command intent with no matching native result remains possible exposure even when the ledger has zero rows and no receipt files.

## Recover the edge without broad infrastructure disruption

An edge process may remain alive yet temporarily disappear from `puda machine list` after `UnexpectedEOF`, while its log still shows the original active run and later `RUN_ID_MISMATCH` responses.

1. Keep the campaign scheduler paused.
2. Inspect the tracked edge process and recent log.
3. Retry a targeted `puda machine reset <machine_id>` once the edge is visible.
4. Restart only that edge process if harmless control remains unavailable; never restart NATS as a recovery shortcut.
5. Require explicit output OFF, output readback `0`, matrix `open_all`, closed-channel readback `nil`, and empty instrument errors before moving on.
6. Preserve UNKNOWN branch intents permanently, quarantine at the last verified cycle boundary, and never replay the ambiguous batch.
