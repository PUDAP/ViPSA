# Local edge-host discovery before remote administration

Use this when a PUDA command path fails and the NATS endpoint is a remote host such as `bears`.

## Durable rule

A NATS host is not proof that hardware edges run on that host. Before SSH or remote service administration:

1. Enumerate local processes and map each candidate PID through both `/proc/<pid>/cwd` and its command line.
2. Inspect the expected edge workspace and `logs/edges/` for fresh startup/subscription records.
3. Check the edge `.env` only for its configured NATS endpoints.
4. Restart the edge on the host where its process and device path actually live. Do not infer edge placement from the NATS hostname.
5. For protected drivers, launch from the protected deployment directory rather than the generic workspace copy.

For the common ViPSA deployment, `light`, `stage`, `zaber`, and `keithley-707b` may run locally under `/home/amdm/workspace/ViPSA`, while the Keithley 2450 may use a separately protected deployment. The remote `bears` machine can be only the NATS cluster.

## Post-failure evidence rule

Do not infer the failed hardware operation from the final traceback line. Decode the raw wire journal and inspect device-native state/logs. A compound travel controller can complete stage clearance successfully and then fail on the next machine's START. Resume from the last independently confirmed boundary; never repeat completed motion.

If a restarted edge consumes a retained START with no queue command, verify the log contains no movement command, complete that exact run ID, then query fresh position. Never use stage reset to clear a stale run because it can redefine logical coordinates.
