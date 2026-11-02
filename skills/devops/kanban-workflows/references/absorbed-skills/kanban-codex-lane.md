# Absorbed skill: kanban-codex-lane

Original package: `autonomous-ai-agents/kanban-codex-lane` archived after consolidation into `kanban-workflows`.

Support files copied: ['templates/ -> templates/kanban-codex-lane/'].

## First 80 lines of original SKILL.md for provenance

```markdown
---
name: kanban-codex-lane
description: Use when a Hermes Kanban worker wants to run Codex CLI as an isolated implementation lane while Hermes keeps ownership of task lifecycle, reconciliation, testing, and handoff.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kanban, codex, worktrees, autonomous-agents, prediction-market-bot]
    related_skills: [kanban-worker, codex, hermes-agent]
---

# Kanban Codex Lane

## Overview

This skill defines the lightweight Hermes+Codex dual-lane convention for Kanban workers. Hermes is always the task owner: it calls `kanban_show`, decides whether Codex is appropriate, creates or selects an isolated workspace, starts and monitors Codex, reconciles any diff, runs verification, and writes the final `kanban_complete` or `kanban_block` handoff. Codex is an input lane only. Codex output is not a task completion signal, not a trusted reviewer, and not allowed to write durable Kanban state directly.

The convention exists so a Hermes worker can use Codex for bounded implementation help without changing the dispatcher. The dispatcher must still spawn Hermes workers. A worker may optionally spawn Codex inside its own run, then accept, partially accept, or reject the lane after independent review and tests.

## When to Use

Use the Codex lane when all of these are true:

- The Kanban task is a coding, refactor, documentation, test, or mechanical migration task with clear acceptance criteria.
- A bounded diff can be evaluated by Hermes in one run.
- The repo can be copied or checked out in an isolated git worktree/branch.
- Hermes can run the relevant tests itself after Codex exits.
- The prompt can state all safety constraints and files that must not change.

Do not use the Codex lane when any of these are true:

- The task requires human judgment that is not already captured in the Kanban body.
- The worker lacks repo access, Codex auth, or time to reconcile the result.
- The change touches secrets, credential stores, private user data, or production order-entry systems.
- A small direct edit is faster and safer than spawning another agent.
- The task is research-only and should produce a written handoff rather than a diff.
- The worker would be tempted to mark Done based only on Codex self-report.

## Ownership Rules

1. Hermes owns the Kanban lifecycle. Codex must never call `kanban_complete`, `kanban_block`, `kanban_create`, gateway messaging, or any Hermes board CLI as a substitute for the worker.
2. Hermes owns final acceptance. Treat Codex commits/diffs as untrusted patches until reviewed and verified.
3. Hermes owns test execution. Codex may run tests, but those runs are advisory; repeat required verification from Hermes with the repo's canonical wrapper.
4. Hermes owns safety. If Codex changes safety boundaries, risk gates, live trading behavior, or secrets handling, reject the lane even if tests pass.
5. Hermes owns cleanup. Kill stuck Codex processes and remove temporary worktrees when they are no longer needed.

## Required Worktree and Branch Pattern

Never run Codex directly in a shared dirty checkout. Use a branch/worktree name that ties the lane to the Kanban task and keeps untrusted edits isolated.

Recommended variables:

```bash
TASK_ID="${HERMES_KANBAN_TASK:-t_manual}"
REPO="/path/to/repo"
BASE="$(git -C "$REPO" rev-parse --abbrev-ref HEAD)"
SAFE_TASK="$(printf '%s' "$TASK_ID" | tr -cd '[:alnum:]_-')"
BRANCH="codex/${SAFE_TASK}/$(date -u +%Y%m%d%H%M%S)"
WORKTREE="/tmp/${SAFE_TASK}-codex-lane"
```

Create the isolated lane:

```bash
git -C "$REPO" fetch --all --prune
git -C "$REPO" worktree add -b "$BRANCH" "$WORKTREE" "$BASE"
git -C "$WORKTREE" status --short --branch
```

If the current Kanban workspace is already an isolated git worktree created for this task, you may create a sibling Codex branch inside it only if `git status --short` is clean except for intentional Hermes edits. Otherwise create a separate temporary worktree and cherry-pick or copy accepted commits back after reconciliation.

Cleanup after reconciliation:

```bash
git -C "$REPO" worktree remove "$WORKTREE"
git -C "$REPO" branch -D "$BRANCH"  # only after accepted commits were copied/cherry-picked or intentionally rejected
```

Keep the worktree if it is needed as an artifact for review; record it in `codex_lane.artifacts` and mention it in the handoff.
```
