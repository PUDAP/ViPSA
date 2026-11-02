# Autonomous campaign continuation and delivery ordering

Use this note when a long multi-device DCIV campaign must continue across chat turns, agent sessions, or scheduler ticks.

## Separate control scopes

A status cron/reporter is observational and is not the hardware campaign. A request to stop or remove the cron job stops only that monitor unless the user also explicitly stops the measurement campaign, motion, or hardware workflow. Do not cancel an otherwise valid device-start instruction merely because its reporter was removed.

## Single-owner continuation

Before any foreground agent or persistent continuation job acts, it must inspect:

- the exclusive hardware-owner lock;
- tracked measurement and motion processes;
- the optimizer runner cursor and pending candidate;
- the active handshake request and dispatch registration;
- device terminal records and done markers;
- permanent-ledger operation states and UNKNOWN status;
- live output, matrix, and pose when hardware action is contemplated.

If another controller owns the lock or a bounded process is still active, observe it rather than launching a duplicate. Resume only from a verified terminal boundary. Never infer missing work from a scheduler tick alone, and never replay a completed branch merely because a chat response or scheduler delivery was missed.

At each completed device, close bookkeeping in this order: verify terminal and ledger → generate and validate artifacts → independently verify OFF/open cleanup → deliver the user-facing completion artifact → verify the delivery handle → record matched optimizer acknowledgement → advance the cursor → begin the next pristine device.

## Delivery evidence is post-delivery

Do not set `delivered: true`, invent a delivery handle, or ingest a handshake that requires delivery evidence before the message or artifact has actually been delivered. File generation, enqueueing, or intending to send is not delivery. If optimizer ingestion requires a delivery record, leave the device at a safe completed boundary until real delivery is confirmed, then write the record and acknowledge it.

## Scheduler termination

A continuation job should stop or pause itself after Device 50 is fully matched and recorded. It should fail closed and report only for unresolved safety, UNKNOWN exposure, ownership conflicts, or evidence that cannot be reconciled; normal recipe-specific device failure is a completed device outcome and must advance to the next device.
