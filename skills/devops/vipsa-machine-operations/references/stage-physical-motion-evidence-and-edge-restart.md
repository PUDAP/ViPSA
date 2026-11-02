# Stage-edge restart and physical-motion evidence hierarchy

## Trigger
Use when a PUDA stage-Z command reports success/readback change but the user says the stage did not move, or when motion stops suddenly after previously working.

## Required response to a disputed move
1. Stop issuing additional Z motion; do not stack a retry onto an uncertain physical position.
2. Treat PUDA `success`, driver `get_current_position`, and changed software Z as **unverified controller/software state**, not proof of mechanics.
3. Audit for duplicate stage-edge processes/process groups holding `/dev/openflexture`. Stop every stale duplicate, verify the serial device is released, then start exactly one edge.
4. Drain/inspect startup serial text. A stale `Grbl 1.1h ...` banner can contaminate the first response after reconnect.
5. Use the project `Stage` class for any recovery move; do not send ad-hoc raw G-code.
6. Capture raw GRBL status around the command when possible. `ok` and `MPos` prove command acceptance/controller position accounting, but **still do not prove physical motion** on an open-loop stage.
7. Physical confirmation requires an independent source: user observation, camera displacement, external gauge/encoder, or another mechanical reference. If none exists, report “controller-reported move; physical movement unverified.”

## Restart discipline
- Restarting an edge can reset/rebase a driver-local position counter. Never add pre- and post-restart software Z values as though they share one physical coordinate frame.
- After restart, run a read-only PUDA transaction and end with `idle`, `run_id: null` before any requested move.
- If the user explicitly says the previous requested move did not occur, a retry is authorized only after the edge/serial recovery above. Report the retry separately from the failed software-tracked attempt.

## Reporting rule
Never say “moved successfully” solely from PUDA success, cached Z, `ok`, or `MPos`. State exactly which evidence was observed and whether independent physical confirmation exists.
