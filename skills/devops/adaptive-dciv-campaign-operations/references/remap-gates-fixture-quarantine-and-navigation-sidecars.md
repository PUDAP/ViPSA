# Remapped campaigns: identity, gate revisions, and safe integration

## Durable workflow

1. Separate physical DUT identity from source recipe identity everywhere: physical grid geometry, recipe waveform/compliance/timing, compiled bindings, readiness, exposure claims, journals and plots. Pin explicit operator assignment artifacts; a later individual override supersedes an earlier arithmetic mapping. Preserve all prior failed-device exposure, including forming and partial preparation without candidate cycles. Do not automatically shift assignments again after another failure.
2. Version forming qualification independently from unchanged waveform parameters. Test the actual gate imported/consumed by the running worker, not only a predicate or JSON description. Verify first qualification prevents subsequent forming attempts and Z advance. Preserve independent near-compliance health stops, preparation-once per physical DUT and cumulative cycle caps.
3. Keep fake-transport fixtures outside production inventory roots. A SYNTHETIC directory name does not justify ignoring a physical exposure claim. Establish provenance through test construction, raw wire identities and full file manifests. Quarantine approved misplaced fixtures under the shared owner lock, preserving every file and verifying hashes; rerun the actual production occupancy check afterward. Avoid concurrent fixture writers during production preflight.
4. Interrupted navigation requires exact returned START/command/COMPLETE evidence, fresh safety/readback and retained original INTENT history. An administrative sidecar is not successful native execution. Use explicit reviewed provenance, canonical owner/navigation locks, exclusive durable creation and independent readback. Retain the canonical database; validate the exact historical prefix plus bounded, plan-specific new suffixes. Every unrelated unresolved operation still blocks. Do not rewrite or delete original records, replay travel, or replace the database.
5. Derive absolute clearance and preapproach from the current verified terminal pose and authorized offsets. Do not carry an earlier device's absolute corridor into a suffix validator. A pinned applied implementation must remain unchanged; a corrected executor/validator requires a separately reviewed version.
6. Distinguish offline tests, live safety capture, navigation COMPLETE, optical checkpoint, preapproach readback and actual acquisition dispatch. Report the precise current-device blocker or actual phase/run ID. Future endpoint geometry gaps do not block an independently valid current device.
7. For zero-candidate plot requests, extract only exact COMPLETE forming/preparation operations, verify raw hashes/identities and commanded row counts, preserve acquisition order and signed raw currents. Plot commanded voltage versus log|I|, label physical device and recipe separately, and mark partial preparation and NO CANDIDATE ACQUIRED. Deliver PNG+CSV without rerunning hardware.

## Validated B2 example (not universal gate policy)

The operator changed the next assignment to physical device 25 / unchanged recipe 22. The revised gate required three consecutive positive-forward samples with |I| >=90 microampere, a complete finite commanded PF 0..+8 V trace, removal of the former whole-forward 20% drop veto, and no later forming/Z advance after the first qualifying sweep. Tests covered two hits, nonconsecutive hits, missing endpoint, nonfinite samples after a hit, absolute negative current, source-array parity, runtime gate consumption, once-only preparation and lifetime cap. This was a versioned campaign-specific authorization, not a default for other devices/campaigns.

Misplaced synthetic device-25 claims initially blocked production occupancy. An evidence-preserving quarantine outside the inventory tree resolved that conflict; the real inventory then passed. Fresh live checks and native navigation/preapproach readbacks subsequently preceded actual forming dispatch. The successful lesson is verified isolation plus real inventory recheck, not claim deletion or a synthetic-prefix exemption.

## Integration pitfalls

- A source/hash pin must be populated and independently verified; passing a fake connector test does not make an offline-only adapter launchable.
- Whole-database hashes are review snapshots, not forever-valid pins after legitimate append-only navigation events. Preserve an exact historical snapshot and validate its unchanged prefix plus finite approved suffix grammar.
- Do not edit code whose hash is embedded in an already-applied administrative record.
- After subagent timeout, inspect saved artifacts and independently run tests; timeout alone proves neither completion nor absence of useful work. Continue one coordinated implementation instead of proliferating competing versions.
- Readiness timestamps attest fresh observations only; do not extend old observations to clear expiry.
