# Pulse initialization: bounded retries and honest background results

Validated lessons from PEA pulse work; this is not a validated Bayesian optimization recipe.

## Rejected trial versus campaign stop

Classify gates before launch. Read compliance, persistent excessive conductance and uncertain command delivery are hard safety stops. Baseline drift is also a trial-validity criterion: with an approved bounded retry policy, one marginal rejection need not end the entire campaign. Preserve rejected trials, withhold SET on invalid initialization, count retries against the total attempt budget, and resume only missing replicates.

Observed example: a baseline drift of 25.26% exceeded the unchanged 25% criterion and prematurely ended a three-replicate anchor. Bounded replacement subsequently completed that anchor; a later anchor had two consecutive failures (31.41% and 29.77%), correctly ending the revised study. Do not describe one rejection as repeated RESET failure, or initialized data as successful switching.

## Background evidence

Worker dispatch is not experimental execution; screening is not Bayesian optimization. Report actual surrogate fits and acquisition-selected experiments separately from initialization. A worker can time out while reporting after its hardware runner exited and cleaned up. Inspect saved runner status, process status, raw command responses and final readbacks before resuming, repeating stress, or claiming cleanup. Preserve artifacts and use a bounded safe runner with finally cleanup; never abandon hardware to a worker deadline.

## Timing and validity

Keithley timed-list sample spacing includes acquisition overhead: nominal 50 ms slots yielded approximately 63 ms sample spacing in this experiment. Separate lifecycle-managed commands also add latency. Instrument timestamps do not independently establish physical pulse widths or RESET-end-to-read relaxation. Freeze or exclude unverified timing from optimization; retain telemetry. Sparse pulse V/I samples alone do not establish pulse-integrated energy.

If a user authorizes exploratory BO after screening fails, soft feasibility outcomes may inform the search; invalid baseline trials must not be counted in a sigmoid and hard safety limits remain. This session had not established a working optimizer or optimum at the time these lessons were recorded.
