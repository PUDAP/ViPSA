# Scientific memory and multi-agent lab contracts

## Three truth layers
- Raw acquisition and permanent exposure ledger: physical history, including UNKNOWN exposure.
- Versioned scientific observations: derived metrics linked to source artifacts and analysis code.
- Conversation/task context: explanatory summaries and workflow state, not authorization or physical evidence.

Scientific memory must never clear UNKNOWN exposure, assign fabricated failure lifetimes, or authorize hardware.

## Proposed scientific-memory implementation
Use a dedicated SQLite evidence store, separate from Hermes state.db. Represent substrates, devices, preparation, candidate executions, artifacts, observations, hypotheses and typed relationships. Store raw files externally; register paths, hashes, execution IDs, contract versions, metric namespaces, units, uncertainty, validity, cycle windows, censoring and analysis-code versions.

Relationships include derived_from, replicates, supersedes, supports, contradicts and comparable_under_protocol. Ingest at verified boundaries; deduplicate by execution/artifact identity. Reanalysis produces a new version instead of silently overwriting old evidence. Keep within-sweep branch contrast distinct from independently retained ON/OFF. A continuation can add observations without resolving earlier exposure uncertainty or changing a frozen scoring window.

This architecture is a proposal, not a deployed or tested memory service. Acceptance requires raw-to-metric traceability, reproducible extraction, no continuation double-counting, preservation of right-censoring and superseded history, and no hardware/ledger mutation during ingestion.

## Single-owner multi-agent design
- Coordinator: campaign contract, routing and concise operator reporting.
- Executor: sole hardware owner, rig lease, acquisition and cleanup.
- Designer: DOE/BO diagnostics and explicit proposals; no direct stress dispatch.
- Analyst/curator: validated metrics, provenance and scientific memory.
- Reviewer: independent milestone scrutiny, not a bottleneck on every cycle.

Durable handoffs include campaign/device/candidate/execution IDs, source hashes, contract version, requested action, acceptance criteria and evidence paths. Distinguish dispatch, publication, acknowledgement, running and verified completion. A named-profile CLI invocation launches work in that profile; it does not prove delivery into an existing Telegram conversation or gateway canonical session. Verify actual artifacts and executor receipts before claiming success.

## AGENTS.md usage
Use a shared root constitution for mission, roles, evidence precedence, handoffs, recovery and completion. Add nested acquisition/analysis/optimization/memory guidance and links to machine-readable schemas and SOPs. AGENTS.md does not enforce permissions, schedule agents or grant hardware authorization; leases, controlled writer APIs and dispatch validators do.

Hermes documentation consulted: https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files and https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban . Verify current semantics before deployment: Git repositories support a root-to-CWD context chain; outside Git, startup checks CWD rather than arbitrary ancestors. Nested guidance can be discovered progressively. Higher-priority context files or overrides may replace AGENTS.md. Directory instructions never transfer a role's privileges. Keep live campaign status out of static context files.

## Communication and diagnostic lessons
Be succinct when reporting campaign status. Continue safe authorized analysis and verified recoverable software work without renewed generic GO, but identify unresolved exposure/control/contract gates specifically. Do not manufacture an autonomous-work percentage without measured active-work and intervention accounting. For poor GPs, compare held-out same-fold mean/ridge baselines and censor-aware models; a better diagnostic baseline does not itself validate production acquisition.
