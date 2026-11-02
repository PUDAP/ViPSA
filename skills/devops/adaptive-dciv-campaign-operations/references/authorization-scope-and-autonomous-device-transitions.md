# Authorization scope and autonomous device transitions

## Trigger

Use this rule for a fixed multi-device DC-IV campaign when the user has already authorized the remaining recipe/device sequence.

## Durable behavior

- Treat the authorization as covering travel, alignment, preparation, candidate bias, health reads, and the configured automatic transition between the named devices.
- A recipe-specific failure terminates only that device. After verified OFF/open cleanup and no unresolved UNKNOWN exposure, advance to the next authorized device without asking for renewed motion or bias permission.
- A hard-cap survivor likewise advances after its terminal evidence and cleanup are verified.
- Status requests and plot requests do not pause the campaign.
- Never infer authorization beyond the named sequence or mutate immutable recipes.

## Mandatory pause conditions

Prior authorization does not waive fail-closed safety. Pause only when a fresh gate cannot be resolved, including:

- dispatched but unreceipted exposure;
- unverified output-OFF or matrix-open cleanup;
- uncertain stage motion or pending motion state;
- missing durable storage or a full filesystem that could lose receipts;
- mismatched device/recipe identity;
- transport failure where exact native evidence cannot prove zero exposure or completion.

Resume automatically after a transient non-exposure fault only when independent evidence restores the full safe state and the original authorization still applies. Use new operation IDs and preserve the failed attempt append-only; never replay an uncertain acquisition.
