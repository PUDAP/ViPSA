# Duplicate edge consumers and delayed START recovery

Use when a successful START is followed by a lifecycle rejection, or a restarted edge receives an earlier timed-out START. This is a recovery pattern, not a reason to assume any particular endpoint is permanently correct.

1. Inventory all instrument-owning processes by exact working directory, executable, parent PID and selected nonsecret environment. Identical `main.py` command lines are insufficient. Never infer wrapper/child correspondence from PID order.
2. Preserve the verified protected/pinned instrument deployment. Remove only confirmed duplicate owners; do not replace protected code with a generic checkout or restart the whole rig.
3. Inspect the process's actual `NATS_SERVERS` override as well as `.env` and CLI config. A process can be connected elsewhere despite its on-disk default. Select the endpoint from live evidence.
4. A START timeout does not prove non-delivery. After reconnect/restart, inspect native responses and current lifecycle ownership. Complete only the exact stale run whose history proves it was read-only or otherwise safe to end. Never use stage reset to clear ownership: reset changes coordinate zero.
5. When CLI completion rejects a live edge due to discovery metadata, the exercised fallback is a single logged immediate NATS COMPLETE for that exact run. Subscribe and flush before publishing, match machine/run ID/command/step, and require a successful native response. Do not fabricate idle status from the publish acknowledgement.
6. Obtain a fresh native position query before motion. Inspect the current driver decorators: a helper named `get_current_position` may not be exposed, while `get_position` returns `{x,y,z}`. Do not call go-to-zero/reset merely to obtain a position.
7. For a requested absolute Z target, compute the signed delta from the fresh coordinate, validate limits, and issue exactly one move under a new owned lifecycle. Require native move success, fresh after-position, confirmed persisted state/no pending target, and final idle/null.
8. Disable automatic reconnect/replay for physical commands. Persist dispatch before sending; if its response is missing, stop UNKNOWN and reconcile from read-only evidence rather than replaying.

Verification also includes SMU output OFF and matrix open/nil before motion. Position telemetry is tracked-coordinate evidence, not independent physical-height metrology. Successful local recovery does not authorize permanently changing cluster configuration.
