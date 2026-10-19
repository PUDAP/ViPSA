# Controller handoffs and completed-cycle snapshots

Use for an in-place instrument endurance run whose operator changes interleaved reads, authorizes exceeding an energy budget, or asks for plots/status while acquisition continues.

## Preserve stress across handoffs

- Apply a next-cycle policy change at the first not-yet-started cycle; finish any existing partial cycle under its recorded policy without replaying its completed operations.
- Carry native operation IDs, acquisition order, cumulative sampled energy and periodic health-check sweep counts across every controller generation. Include preparation sweeps if the original controller included them.
- Branch-energy waivers and cumulative-energy ceilings are distinct. Honor an explicit, current-device cumulative override at both pre-dispatch and post-operation checks, preserving the counter. Unknown/nonfinite accounting, native integrity, owner, routing, control and cleanup faults remain blockers.
- A complete sweep that fails only at a post-acquisition budget guard can be acknowledged without changing its original fault status: verify ordered native count/list identity, finite measured V/I/time, monotone timing, independently recomputed already-charged energy and successful cleanup; attach the proof and resume at the missing operation.
- When prior proof helpers require a cleared device unknown flag, validate each historical proof against a read-only preview of the proven reconciled state before changing the live flag. Never clear another unknown exposure by association.

## DCIV-only analysis

At comparable measured low bias, report positive `abs(I_PB)/abs(I_PF)` and negative `abs(I_NF)/abs(I_NB)` separately. Preserve exact selected native indices, commanded/measured voltages, signed currents, compliance/status, operation IDs and any interpolation. Flag clamped, voltage-collapsed or offset-dominated comparisons rather than reporting clean ratios. Within-sweep contrast is not retained-state evidence. Remove routine standalone reads only when authorized; preserve any agreed periodic health checks. Keep sweep arrays, timing and compliance unchanged.

## Live plots

Read one stable ledger/receipt snapshot, select completed operations with verified cleanup, and merge controller generations by canonical device/cycle/operation identities. Include a historically fault-labeled sweep only with its exact reconciliation proof and manifest provenance. Exclude preparation and incomplete cycles from endurance overlays. Verify distinct cycle count, native point counts, contiguous point order and duplicate absence in code. Preserve PF/PB/NF/NB acquisition order; overlay all branches on one commanded-voltage/log-absolute-current axis with one colour per cycle and branch line styles. Save CSV, PNG, SVG and a provenance manifest. Do not issue hardware commands, stop acquisition, or rerun stress to make a plot.

## Status and apparent pauses

Match delayed exit notifications to the originating process/session and execution directory. Verify the current controller, recent progress and absence/presence of its terminal record before calling a new failure or launching any replacement. State full cycles completed separately from the current cycle/branch; qualify cleanup as belonging to the last completed operation. Retrieve metrics from saved native data rather than estimating from process uptime.

Buffer retrieval, serialization, cleanup, routing and list qualification introduce real between-operation time, even without programmed dwell. Removing reads does not remove those gaps. Explain their scientific relevance instead of claiming uninterrupted cycling. Failure criteria must be explicit and distinguished from irreversible destruction; an isolated SET-side compliance hit is not failure.
