# Autonomous continuation after verified campaign gates

## Trigger

Use this note when a multi-device or multi-batch campaign already has standing authorization and a preparation, candidate batch, health check, plot request, or transport-recovery gate completes.

## No-idle rule

A successful completion notification is an action trigger, not merely a reporting event. Validate the durable terminal/ledger evidence and immediately launch the next safe bounded operation covered by the existing authorization. Do not wait for another “start” message, and do not leave a prepared device idle solely because the user asked for a plot or status update.

Read-only plotting and CSV generation should run from saved data in parallel with the next authorized hardware phase, or after that phase has safely launched. Plotting must never compete for the campaign owner lock or modify electrical/motion state.

Pause only for:

- unresolved UNKNOWN or post-dispatch ambiguity;
- unverified OFF/open/cleanup or pose;
- an actual transport/control gate that prevents direct command proof;
- a declared scientific stop criterion;
- an operator stop or exhausted authorization.

## Health-read semantics

Post-batch health reads must retain their declared role. If recipe failure is defined by a minimum-cycle plus consecutive-cycle rule, a health row that reaches read compliance with measured-voltage collapse is not a valid independent resistance/state estimate. Record it as compliance-limited and diagnostically invalid, but do not silently replace the configured cycle-level stop rule. If the campaign separately declares that health condition a hard safety gate, the hard gate wins and testing stops.

## Reporting

Report the completed boundary and the newly launched operation together. Avoid a status-only response when a next authorized action is ready. State process/run identity, physical and verified cycle ranges, native point count, and whether candidate stress crossed dispatch.
