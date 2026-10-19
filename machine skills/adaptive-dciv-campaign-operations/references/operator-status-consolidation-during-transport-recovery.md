# Operator-facing status during transport recovery

Use this communication pattern when an adaptive campaign is running while NATS/edge recovery produces several internal attempts.

## Consolidate attempts into scientific state

Do not narrate every retry as if it were a new measurement event. Report the distinction explicitly:

- **verified scientific progress:** completed cycles/batches;
- **transport attempts:** zero-exposure starts, lifecycle timeouts, or cleanup retries;
- **current hardware state:** OFF/open/idle/UNKNOWN status;
- **current action:** one active batch or one recovery gate.

A series of zero-exposure attempts should be summarized as one recovery episode. State that they did not stress the device, did not advance counters, and were preserved under fresh operation IDs.

## Answer the requested artifact first

When the user asks for a plot during a live run:

1. generate and return the requested plot and source data;
2. give only a one-line campaign status if useful;
3. do not append an unrelated transport traceback or speculative warning to the plot response;
4. report a background fault separately only after its exposure and safety classification is known.

This prevents a successful plotting request from being conflated with an unrelated controller recovery.

## Recommended concise status format

```text
Device N: X verified cycles. Batch Y is [running/recovering].
Transport recovery: K zero-exposure attempts, no replay.
Safety: output OFF, matrix open, active UNKNOWN [none/present].
Next: [specific bounded action].
```

Use technical detail (run IDs, hashes, process IDs, full recovery chronology) only when the user asks or when it changes the decision. For ordinary updates, prefer the scientific boundary and safety state.

## When the user asks “what is going on?”

Answer directly before continuing tools:

- identify whether the problem is communications, acquisition, cleanup, or device behavior;
- state the latest verified cycle count;
- state whether any uncertain exposure exists;
- state whether measurements are currently running;
- state whether prior attempts were replayed.

Avoid a long chronological reconstruction unless requested.
