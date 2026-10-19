# Direct-NATS RUN_ID_MISMATCH during Z-move + DCIV chains

Use this when a ViPSA command path reaches NATS but PUDA/edge run state rejects queued commands.

## Observed failure pattern

During a request to move `stage` Z by `+1.0` step and then rerun DCIV:

- `puda protocol run` failed before motion due intermittent NATS connect/read timeouts.
- Raw TCP showed NATS ports could still return `INFO`, so TCP-open was not enough proof that PUDA control was healthy.
- A direct transaction reached the stage edge, but `stage.move_z_by` returned `RUN_ID_MISMATCH`.
- The START response may include `cannot start, <old-run-id> is currently running`; a queued command sent after a failed START is rejected and must be treated as **not executed**.
- Cleanup commands can also be rejected if their START/queue transaction is malformed or if run state is stale.

## Durable workflow lesson

For direct-NATS PUDA fallback, the transaction must be gated:

1. Subscribe to both response subjects:
   - `puda.<machine>.cmd.response.immediate`
   - `puda.<machine>.cmd.response.queue`
2. Publish `start` on `.cmd.immediate` and wait for a START response with `response.status == success` for the fresh `run_id`.
3. If START fails with a currently-running run ID, publish `complete` on `.cmd.immediate` using that exact old run ID, wait for/record the COMPLETE response, then start a new fresh transaction.
4. Only publish the driver method to `.cmd.queue` after START success is confirmed.
5. Wait for the queued method response and require `response.status == success` before claiming motion/electrical work occurred.
6. Publish `complete` with the same fresh `run_id`; verify a safe readback or idle state afterward when possible.

## Safety rule for chained motion/electrical requests

For commands like “move Z 1 step and run DCIV,” the DCIV authorization is conditional on the motion actually succeeding:

- If the Z move fails, is rejected, or cannot be verified, do **not** run DCIV.
- If NATS/PUDA state is unstable, do not keep retrying electrical stress blindly; report that no confirmed motion/stress occurred.
- A TCP port being open or a NATS `INFO` banner being returned is only a transport diagnostic, not proof that PUDA START/queue/COMPLETE state is healthy.

## Reporting standard

When blocked by this state:

- Say explicitly whether Z motion was confirmed.
- Say explicitly whether electrical stress/DCIV was executed.
- Include cleanup commands attempted and whether final safe state was verified or could not be verified.
- Do not include ephemeral run IDs in the user-facing final unless they are needed for immediate operator debugging; keep them in saved logs/references only.
