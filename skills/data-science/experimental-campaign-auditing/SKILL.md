---
name: experimental-campaign-auditing
description: "Use when auditing experimental commands and elapsed time."
version: 1.0.0
metadata:
  hermes:
    tags: [experiment-logs, provenance, commands, timing, interruptions]
    related_skills: [puda-data, hermes-state-operations]
---

# Experimental Campaign Auditing

Audit saved experiment logs and orchestration history without issuing hardware commands. This complements measurement-data extraction; it does not prescribe electrical recipes or interpret switching.

## Scope and boundaries

Start with original project metadata, run summaries, request/response logs and read-only instrument database records. Conversation history is secondary evidence. Build an included/excluded campaign manifest distinguishing materials, physical substrates, selected sites, primes, optimization versus yield, original runs, resumes and supplementary retests.

Resolve first-command-to-final-plot boundaries from actual events. The final device means final traversal position, not the highest numbered device. If only runner-start/device-finish fields exist, label them proxies; never silently claim exact command-to-plot timing. Disclose late backfills that undermine apparent full-grid completion.

## Command accounting

- Instrument submissions, ACKs, lifecycle events and agent/tool invocations are separate layers; do not add them together.
- Count actual execution evidence, not loaded plans. Saved acquired operations can establish lower bounds where request logs are missing; data points are not individual sweep commands.
- Deduplicate copied logs/results, correlate submission/ACK by run ID, step, machine and command, and preserve uncertain matches. Deduplicate conversation tool-call IDs across mirrors and compactions.
- Flatten recorded nested calls, but do not invent script-loop iterations as tool invocations.
- Separate explicit substrate attribution from contextual time-window candidates. Multi-purpose scripts remain mixed/ambiguous rather than being forced into electrical, plotting or planning.
- Verify category/status sums against the same population. Missing movement or plotting records are not proof of zero activity.

## Interruptions

Keep runner stops, failed protocol attempts, continuation launches and operator pauses distinct. They overlap and are not additive unique interruptions.

Require actual failure/status evidence. `read_errors` command names, descriptions containing `error`, successful preflights and `forming_success` do not establish an interruption. Stale `running` summaries are unresolved, not confirmed stops. Deduplicate multiple failure lines from one attempt.

## Time reconstruction

Use timezone-aware timestamps and cross-check local CLI times against UTC responses. Union bounded spans into a non-overlapping partition. Unknown gaps remain unclassified—not automatically human waiting, plotting or planning. Send-to-response duration includes command/transport overhead and is not pure stimulus-on time.

Saved per-operation elapsed fields may recover electrical-call duration without UTC placement. Match and deduplicate operations, avoid overlap with already timed commands, and report missing chronological placement. Verify every aggregate residual is nonnegative and every substrate partition reconciles with its window.

Confirmation-request-to-user-response intervals are wait candidates, not proven idle time. Error/recovery extends beyond failed commands; zero recovered failed-command duration does not mean zero error time.

## Approach versus characterization

Reassign forming/contact electrical sweeps out of non-forming characterization when the operator requests this bifurcation. Do not count forming twice. Preserve conditioning/endurance scope and call-overhead semantics.

Show XY travel/alignment, Z motion and readback/control separately. Not every Z move is approach: retraction/pre-approach may be included. If workflow boundaries or contact-increment intent are missing, mark FULL approach duration unavailable and show recovered components only. A forming-only subtotal is not the complete approach time.

## Artifacts and user delivery

Provide boundary/source manifests, command/interruption ledgers, timing CSVs, a date-column/time-row calendar, readable summary figures, methodology and a reproducible bundle. Verify site counts, category/status sums, elapsed partitions, image legibility and archive integrity.

For this user's explicit **files-only** handoff, deliver attachments without surrounding prose; put uncertainties and methodology in the files. Wait for a named bot's actual request rather than initiating an unsolicited handoff.

See `references/audit-reconciliation-pitfalls.md` for source and accounting checks.
