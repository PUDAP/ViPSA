---
name: kanban-workflows
description: "Use when operating Hermes Kanban boards, orchestrators, workers, and coding-agent lanes for durable multi-agent work queues."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kanban, workers, orchestrator, queue, multi-agent, codex-lane]
    related_skills: [hermes-agent, ai-coding-agents]
---

# Hermes Kanban Workflows

## Overview

This umbrella skill covers durable Kanban task orchestration in Hermes: decomposing work, assigning tasks to workers/profiles, operating worker tools, linking dependencies, and routing coding-agent lanes such as Codex.

## When to Use

- Creating or managing Hermes Kanban boards/tasks.
- Acting as an orchestrator that decomposes and assigns work.
- Acting as a worker that must complete/block/comment/heartbeat.
- Running a specialized coding-agent lane from a Kanban task.

## Roles

### Orchestrator
Decompose work into independently verifiable tasks. Keep task prompts self-contained, specify artifacts and tests, link dependencies, and avoid doing worker implementation directly unless explicitly asked.

### Worker
Read the task, inspect linked context, perform the work, verify it, then mark complete or block with a concrete reason. Heartbeat during long work and leave comments with artifact paths, commands run, and unresolved risks.

### Coding-Agent Lane
When routing to Codex or another coding agent, translate the Kanban task into a standalone agent prompt with repo path, branch policy, allowed files, test commands, and required final evidence.

## Common Pitfalls

1. Orchestrators should not hoard implementation; create tasks when parallelism or durable tracking helps.
2. Workers must not ask the absent user for routine context; block only when truly blocked.
3. Completion without verification creates false board state; include command output or artifact IDs.
4. Keep board comments concise but sufficient for the next worker to resume.

## Verification Checklist

- [ ] Task has clear owner/profile and dependencies.
- [ ] Worker final state is complete or blocked, not abandoned.
- [ ] Evidence is attached in comments or final output.
- [ ] Coding-agent lane output was independently verified.
