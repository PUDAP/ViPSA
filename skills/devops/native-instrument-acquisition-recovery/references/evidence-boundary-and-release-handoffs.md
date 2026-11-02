# Evidence boundaries and release handoffs

## Storage exhaustion: controller labels are not the acquisition boundary

An ENOSPC interruption can prevent status, receipt, and final-cleanup journal commits even after the native command returned. In the observed recovery, the journal still claimed preparation had not started, while an offline native audit proved four forming attempts, preparation 01–07 and the intervening health read had completed. A stale position-read INTENT also had a native returned receipt. The first missing stress operation was preparation 08, not forming or approach.

Use this as an evidence-order example, not a reusable device number or live recovery authorization:
1. Preserve the original journal and raw lifecycle files.
2. Match exact run/command IDs, ordered requests/replies, arrays, hashes, rows and energy; inspect evidence beyond the last committed journal entry.
3. Resolve stale acknowledgements additively. Never infer zero exposure from a stale phase label.
4. Restore storage within explicitly approved deletion scope; verify available space before further durable writes. Cache deletion does not itself authorize experiment-data deletion.
5. Require fresh owner-locked native idle, schema, OFF/open/error and pose proofs before executing only the proven missing suffix.

The recovery implementation passed its offline suite and was launched; its live completion was not observed in this review. Do not describe the launch as a successful live recovery.

## Slow audits and owner freshness

Complete the expensive immutable-history audit under exclusive leases before minting a genuinely new, challenge-bound owner attestation. Preserve scope, reviewed schema digest, TTL limits and evidence mutation monitoring. Renewing only timestamps is not a new attestation. Prior command returns establish historical issuance/completion, not current pose.

## Historical evidence versus new read-only receipts

A historical suffix validator must retain its exact original file inventory while separately validating later discovery/read-only namespaces. Do not demand that the entire shared wire directory forever equal an old suffix inventory; do not accept arbitrary additional directories either. Verify later lifecycle identities, commands, parameters, hashes and state, rejecting unexplained motion/stress or intents.

## Release and asynchronous handoff discipline

- Treat child timeout, serial test runner exit, freeze creation, frozen readback and live execution as distinct events.
- Reuse a surviving notified background runner; do not restart expensive duplicate suites or wait out child lifetimes with repeated polling.
- Tests finishing before the final packaging import fails are not a frozen release. Check exact expected suite names/counts, successful results and unchanged tested-source hashes before completing the packaging step with the correct module search path; then independently verify the freeze.
- Mark superseded delayed process notices as such. Never count a failed or source-drifted test as current release evidence.
- Test the actual next-stage handoff, not only an API-exists stub: readiness, navigation, image checkpoint and acquisition have separate permissions and acceptance criteria.
- Report 'worker launched' separately from 'motion completed' and 'measurement acquired'. Repeated user start authorization does not require repeated consent, but never bypass unresolved native evidence.

## Independent outcome labels

Preserve UNKNOWN safety-stop audit flags independently of native-data-confirmed recipe failure. Recompute cycle failure signals and streaks from actual cycles: nine consecutive failures after one nonfailure can validly yield a cycle-10 latch with a ten-cycle minimum. A near-compliance health stop must not trigger further stress or a health retry merely to clear UNKNOWN.
