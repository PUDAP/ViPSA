# Selective electrical-edge activation

Verified recovery pattern from a ViPSA session; use fresh discovery rather than assuming historical paths or ports remain current.

1. User authorization to enable two edges does not authorize all-edge startup, stage reset/motion, or automatic resumption of a failed measurement. Inspect each entrypoint, check duplicate processes, then start only the requested services from their own directories as tracked long-lived processes. In the verified setup, each used `uv run main.py`.
2. Startup logs can show replay of durable START commands left by earlier controller timeouts. Recover the exact active run shown in fresh logs; never copy historical run IDs.
3. Try ordinary lifecycle COMPLETE first. If it refuses as offline despite fresh edge logs, the successful fallback used `nc.jetstream().publish('puda.<machine>.cmd.immediate', payload)` with command `complete` and the exact active run ID. The payload included normal machine/user/version/timestamp headers and command fields. This fallback is lifecycle cleanup only, not blanket authorization for direct stress commands.
4. JetStream PubAck proves persistence only. Require matching edge response `status: success` and a fresh `idle`, `run_id: null` transition before proceeding.
5. Return to a full-metadata PUDA protocol from the active project. The verified safe sequence was `keithley-2450.set_output(enabled=false)`, `keithley-707b.open_all`, and `get_closed_channels`; all succeeded and the last returned `data.result: nil`. Use driver-only commands in the protocol; CLI supplies START/COMPLETE.
6. Verify successful final COMPLETE for both edges and continued process liveness. Say output-off command succeeded unless independent hardware output readback was actually obtained.

## Reporting and scope

Keep activation confirmation concise. Do not claim measurement started or resume a prior failed runner solely because activation succeeded. During autonomous Pratap testing, routine per-device messages should contain only completed plotted data; concrete safety/control blockers warrant concise exception reports.

## Pitfalls

- Cached machine discovery/state may disagree with fresh edge responses. Do not treat either as absolute without cross-checking.
- Core publish timeouts and JetStream publish acknowledgements are different evidence. Only matching execution responses establish effects.
- Do not reset the Stage to clear run-state errors: reset can redefine the current location as zero.
- Do not perpetuate the session's temporary failures as permanent endpoint/tool limitations.
