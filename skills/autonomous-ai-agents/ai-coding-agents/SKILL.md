---
name: ai-coding-agents
description: "Use when delegating software work to autonomous coding CLIs such as Claude Code, Codex, OpenCode, or other agent subprocesses."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [agents, coding, claude-code, codex, opencode, delegation, subprocess]
    related_skills: [hermes-agent]
---

# AI Coding Agent Delegation

## Overview

This umbrella skill covers using external autonomous coding agents as workers. It consolidates provider-specific CLI notes into one class-level workflow: choose the right agent, isolate its work, pass complete context, supervise output, and verify artifacts yourself.

## When to Use

- Delegating feature work, refactors, bug fixes, or code review to Claude Code, Codex, OpenCode, or similar CLIs.
- Running independent agent processes in tmux/background sessions.
- Comparing outputs from multiple coding agents.
- Building a human/agent handoff prompt for a bounded code task.

## Agent-Specific Notes

### Claude Code
Strong for repo-scale edits and codebase navigation. Give explicit acceptance tests, branch/worktree constraints, and permission boundaries. Capture final diff and test output yourself.

### Codex
Strong for patch-oriented implementation and review. Provide paths, failing commands, and exact expected behavior. If used inside a queue/lane, keep prompts self-contained because the worker has no parent chat memory.

### OpenCode
Useful as an alternative coding agent or reviewer. Treat its claims as unverified until you inspect the diff, run tests, and read generated files.

## Standard Delegation Loop

1. Inspect repo status and choose isolation (`git worktree`, branch, container, or temp copy).
2. Write a self-contained prompt with goal, constraints, files, tests, and forbidden actions.
3. Run the agent with tracked process/session output.
4. Review its diff and logs; do not trust self-reported success.
5. Run relevant tests/builds yourself.
6. Commit or hand off only verified changes.

## Common Pitfalls

1. Agents over-edit when prompts omit scope; name allowed files/components when possible.
2. Background agents can silently hang; use tracked processes, tmux capture, or completion notifications.
3. Subagents cannot ask the user questions; include all missing context or keep task narrow.
4. Never report success based only on an agent's final message.

## Verification Checklist

- [ ] Work isolated from the user's dirty tree.
- [ ] Prompt includes tests and acceptance criteria.
- [ ] Diff inspected by the supervising agent.
- [ ] Tests/builds run outside the delegated agent.
