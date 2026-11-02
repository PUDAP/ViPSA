# Restoring a campaign driver without overstating qualification

Use after an authorized deployment choice when a currently working single-sweep driver cannot preserve an earlier continuous campaign protocol.

## Restore the exact deployment, not merely its original commit

1. Preserve the current working source, tests, byte hashes and remote commit. Keep logs and experimental data out of the Git commit. A scoped export worktree based on the remote base avoids accidentally pushing unrelated local-ahead commits.
2. Find the retained campaign deployment and compare its complete source hashes with historical live receipts. A deployment directory named after an earlier commit may contain subsequent validated fixes; checking out that old commit alone may lose native encoding, trigger-model or current-range fixes.
3. Test the retained deployment offline before replacing the edge. Exercise continuous output transitions, complete SET/RESET pairing, zero-voltage boundaries, supported range ceilings and forced-OFF failure handling.
4. Hold the existing shared controller owner. Verify no active acquisition worker, independently read output OFF, open/read matrix nil, preserve error evidence and obtain fresh Stage/Zaber pose.
5. Stop only the verified SMU Python process and its actual wrapper, not the all-edge launcher. Start exactly one protected edge from its retained deployment directory using the active NATS configuration and a tracked background process. This can preserve the newer workspace driver unchanged.
6. Verify readiness and query actual identity, REAR terminals, capabilities and deployment fingerprints. Audit all edge Python processes globally by cwd/executable; distinguish a uv wrapper from a duplicate edge.
7. Prove every frozen candidate SET and RESET list on the instrument with output OFF. Use the actual campaign compiler, keep full-precision compliance, and program a supported measurement-range ceiling without rounding compliance to that ceiling. Preserve native receipts before parsing. Check exact point counts, ordered native levels, OFF and empty error queue after each proof; verify final zero configuration, cleanup and unchanged pose.

## Qualification boundaries

Keep these distinct: offline tests passed; exact source restored; native output-OFF lists verified; independent physical timing/energy protection qualified; exposure executed and verified. The first three do not establish the latter two. Do not fabricate physical timing evidence or set qualification flags merely because the old driver ran previously. Conversely, an optional guarded-subsystem metadata flag is not by itself proof that every native campaign path is unavailable: inspect the actual acquisition method and its scoped qualification/authorization contract. Stop if that contract genuinely lacks evidence.

Restore the confirmed acquisition boundary. A continuous ten-cycle native batch cannot silently be replaced with independent branch calls that switch output OFF after each sweep. One-process-per-cycle recovery guidance applies only to a protocol whose native boundary is one cycle.

## Verified reference example and limits

The retained source at `/home/amdm/data/vipsa/deployments/keithley-2450-protection-2a521f7/keithley-2450/` matched the campaign's expected driver SHA256 `32de646cecc933aec25964897fa71503c757c72f2fe6342f7fc3566acc6525df`. Eight offline native regression tests and sixteen candidate-list OFF proofs succeeded after targeted restoration, with OFF/nil/empty-errors and unchanged pose verified. Newer workspace source remained preserved. This validates restoration and OFF-proof technique only: fresh partial-preparation execution and the new multi-device campaign had not been verified. Do not represent the pending executor adaptation as a tested measurement workflow.

## Reporting and operator handoffs

Show proposed recipes in chat while executing from authoritative full-precision files. Preserve actual clarification-form answers in a separate execution overlay when an optimizer's immutable package still contains stale null protocol fields. A first-device handoff is a completed prefix: manual contact, positive forming, negative forming and conditioning each have separate provenance. Resume only the missing suffix; do not replay positive forming or import another substrate's counters because its stored pose happens to match.
