# Fresh-substrate restart with a historical training cutoff

Use when the operator restarts Bayesian optimization from an earlier round on a new substrate, delegates proposal generation to a separate optimizer, and authorizes execution after its handoff.

## Separate three identities

- **Training population:** exact historical observations permitted for model fitting.
- **Proposal round:** the fresh optimization round being generated.
- **Execution population:** new physical devices on a fresh substrate.

A request to regenerate round 2 from initial sampling plus round 1 excludes historical round 2 and later from fitting, even if those results are locally available. Require an explicit included-device/observation list and source hashes from the optimizer; a round label on a CSV is not sufficient evidence. Preserve old observations unchanged. Do not substitute executor-generated recipes for a specifically assigned Bayesian bot.

## Freeze the physical handoff without disturbing contact

1. Check for active workers and existing owner locks before querying hardware.
2. Obtain fresh read-only Stage/Zaber pose, output state and matrix state through matched native responses; do not infer the origin from the prior substrate's last device.
3. Record the user-established first contact as **manual contact provenance**, not electrically proven contact. Preserve its live aligned XY and tracked Z. Do not automatically retract, align or approach this first device merely because later grid devices need those phases.
4. A later pose change invalidates automatic reuse of the captured contact; reconcile rather than moving blindly to the stored Z.
5. Write a new execution namespace, immutable origin evidence, grid CSV and executor request. Do not inherit old substrate IDs, consumed-device records, per-device Z ceilings, recovery waivers or stale completion sentinels.

## Primed grid labels and traversal

For a requested 10×10 grid with positive native pitches, use row-major physical numbering and an explicit ASCII-prime label field (`1'` … `100'`). Keep numeric device number, display label and traversal index separate.

For zero-indexed row r and column c:

- number = 10*r + c + 1
- X = X_origin + c*pitch_x
- Y = Y_origin + r*pitch_y
- reverse odd-indexed rows for serpentine traversal.

Thus traversal begins `1'…10',20'…11',21'…30'`, not sequential labels across every row. Validate count, uniqueness, bounds and adjacent native-coordinate distance programmatically. Grid capacity is not a request to consume every device immediately: bind only the proposed batch and explicitly authorized later batches.

## Optimizer-to-executor contract

Require the exact requested number of frozen recipes, recipe IDs/digests, source-data provenance/inclusion list, actual electrical arrays or an exact compiler specification, timing, compliance, cycle caps, stop policy and ordered fresh-device bindings. Preparation/conditioning and candidate cycles remain separate. An incomplete handoff remains pending; do not invent missing limits.

Before execution, instantiate and test the actual new controller constructors and every candidate array. Compare capabilities with the **currently loaded** edge, not an old campaign's driver: a legacy native-list edge does not automatically expose guarded or continuous-batch methods. Only launch after shared-owner acquisition, fresh safety/pose proof, qualified arrays and an unambiguous no-replay ledger.

## Conditional execution and watchers

The user's 'once the bot hands recipes, run them' authorizes automatic progression after verified gates, not a second go request at every successful step. It does not waive hardware safety or provenance checks.

A stable read-only handoff detector may wake a validation agent when the canonical handoff file changes. Keep detector output free of timestamps; hash immutable file bytes. Silence unchanged/no-handoff states. Check for an already active executor before any competing getter or launch. Document the canonical handoff path to both roles; creating a watcher is not proof that the optimizer received the request or that any measurements started.

Report states precisely: grid prepared, awaiting recipes, handoff validated, worker launched, native result verified. The workflow in this session was verified only through grid creation/readback and watcher registration; optimizer delivery and the new campaign execution were still pending. Do not present that pending portion as a tested executor implementation.
