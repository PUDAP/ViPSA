# Continuous DC-IV batch semantics and recovery

Use this reference when adapting a validated recipe batch to a different physical traversal or rebuilding a crash-safe executor.

## Preserve proposal identity while rebinding hardware

- Keep candidate ID, request ID, full-precision electrical parameters, source semantic hash, and source file hash unchanged.
- Create a separate execution binding that maps proposal order to the authorized physical-device order.
- Bind each physical device to its absolute grid target; do not edit the immutable optimizer handoff.
- Record both nominal grid XY and final optically aligned XY. They are intentionally different; never require aligned XY to equal nominal XY.

## Fresh-device alignment and approach

1. Prove output OFF, matrix open, empty error queue, exclusive ownership, and current pose.
2. Retract, move to the absolute nominal target, and capture fresh Camera 1 evidence.
3. Apply the established optical correction and verify the final residual is within the campaign gate (normally <=5 px).
4. Persist nominal target, aligned pose, image hash/path, residual, and readbacks.
5. Perform the pre-approach as its own durable motion operation. Optical alignment/pre-approach is not physical contact.

## Forming semantics

- The standard contact/forming criterion is **three consecutive qualifying current points within the outbound branch of one forming sweep**.
- It is not three consecutive forming sweeps.
- Evaluate only the outbound branch; the intentional return-to-zero must not create a false down-jump rejection.
- If a sweep does not form, persist a separate +5 Z motion intent/readback before the next fresh forming operation ID.
- Stop on the first sweep satisfying the within-sweep criterion; never add redundant forming sweeps.
- Preserve the bounded maximum-attempt rule and hard forming-energy limit.

## Conditioning and candidate cycles

- Preparation/conditioning is not candidate-cycle testing.
- Run the fixed conditioning sequence exactly; do not count it toward candidate endurance.
- A candidate cycle counts only when both native SET and RESET branches are complete and matched to the frozen command.
- Continuous batches must preserve one output-ON interval, exact point arrays/settings, per-segment identity, and final output-OFF proof.
- Write-branch energy warnings and cumulative-device waivers must be preserved with their exact scoped authorization; they do not relax UNKNOWN, cleanup, or no-replay rules.

## Failure and health semantics

- Run the required health read after every complete ten-cycle batch.
- Health reads are telemetry and safety evidence; they are not candidate-cycle failure votes.
- Apply the recipe stop rule to consecutive **candidate-cycle** metrics. For this campaign, stop only after three consecutive full candidate cycles meet the recipe-specific failure signal.
- An isolated invalid comparison or low contrast does not stop testing if later candidate cycles recover.
- Cap survivors are right-censored, not failures.

## Crash-safe batch boundary

Before every batch, persist the batch intent and every branch operation identity. After dispatch:

- Complete only from native evidence with exact segment/point/settings/output proofs.
- If transport or cleanup becomes uncertain, mark dispatched operations UNKNOWN, preserve available native rows, and do not replay them.
- Recover instrument safety independently (OFF/open/errors/pose/driver identity) before deciding whether a new non-overlapping physical range is allowed.
- Never relabel an infrastructure fault as scientific device failure.

## Regression tests

Hardware-free tests should cover:

- immutable proposal hashes and physical rebinding order;
- nominal-versus-aligned XY distinction and fresh Camera 1 residual gate;
- one-sweep forming success from three consecutive outbound points;
- durable +5 Z operations between failed forming sweeps;
- exact ten-cycle continuous batches and health after every batch;
- three consecutive candidate-cycle failures (not batch-health flags);
- right-censoring at cap;
- stale intent -> UNKNOWN and no replay;
- cleanup requiring output 0, matrix nil/empty, and errors [].
