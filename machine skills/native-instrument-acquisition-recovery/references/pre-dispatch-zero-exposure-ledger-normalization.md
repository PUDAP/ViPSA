# Pre-dispatch zero-exposure reconciliation and ledger normalization

Use when an operation intent was created and the permanent ledger marked it UNKNOWN because a pre-acquisition safety proof failed, but the wire journal may prove that no instrument acquisition command was dispatched.

## Evidence gate

Classify as zero exposure only when all are true:

1. The operation failed inside `before_stress`/pre-acquisition verification.
2. The raw wire journal contains no acquisition request for that operation after its intent.
3. No receipt, rows, or trace-energy record exists for it.
4. Any acquisition request in the execution is identified and belongs to a separately completed prior operation.
5. Later cleanup independently proves source output OFF and matrix open.
6. No other unresolved operation exists for the device.

A failed `open_all` or other pre-cleanup call is not itself proof of zero exposure. The absence of the acquisition dispatch in the durable command journal is the decisive evidence.

## Compatible terminal representation

Inspect the ledger/controller predicate before selecting a state name. If it blocks on any operation with `state != COMPLETE`, do not leave a custom `ZERO_EXPOSURE` state. Normalize the proven operation as:

```json
{
  "state": "COMPLETE",
  "complete": false,
  "trace_energy_J": 0.0,
  "unknown_exposure": false,
  "reconciliation": {
    "zero_exposure": true,
    "no_replay": true,
    "wire_sha256": "..."
  },
  "original_fault_history": {
    "state": "UNKNOWN"
  }
}
```

Keep the device energy unchanged, preserve the full original UNKNOWN record, store the wire path/hash and exact command-count proof, clear the device UNKNOWN flag only after scanning the whole ledger, and retry with a fresh operation ID. Never reuse the abandoned ID.

## Preparation continuation

When a prior forming sweep completed and passed but the first conditioning operation was zero exposure:

- preserve the forming receipt and criterion;
- preserve the current verified pose;
- do not repeat forming or pre-approach;
- resume conditioning at its first missing sweep with a fresh ID;
- carry total stress and health counters forward;
- link the abandoned intent and zero-exposure reconciliation in the continuation run.
