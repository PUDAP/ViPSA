---
name: software-development-workflows
description: "Use when planning, debugging, testing, reviewing, spiking, or delegating software-development work inside a codebase."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [software-development, planning, debugging, testing, review, spike, subagents]
    related_skills: [ai-coding-agents, github-workflows]
---

# Software Development Workflows

## Overview

This umbrella skill consolidates general software-development process skills. Use it as a class-level playbook for deciding whether to plan, spike, debug systematically, write tests first, request review, use debugpy/node inspectors, or delegate through subagents.

## When to Use

- Writing or executing implementation plans.
- Debugging failing code or production-like behavior.
- Practicing test-driven development.
- Requesting or performing pre-commit review.
- Running throwaway spikes to validate an idea.
- Using Python debugpy or Node inspect.
- Coordinating subagent-driven development.

## Workflow Modes

### Planning
Write small, verifiable tasks with paths and acceptance checks. Plans belong in files when the user asks for plan mode; otherwise execute directly.

### Systematic Debugging
Reproduce first, inspect evidence, form hypotheses, test one variable at a time, then fix root cause. Avoid shotgun edits.

### Test-Driven Development
Create a failing test for the desired behavior, implement the smallest fix, then refactor with tests green.

### Code Review
Run local quality gates where available, inspect diff for security/correctness/maintainability, and separate blocking from non-blocking comments.

### Spike
Use a disposable experiment to answer a specific uncertainty. Keep spikes isolated and either discard or intentionally promote learnings.

### Debuggers
Use debugpy for Python and Node inspect/CDP for JavaScript when print/log inspection is insufficient. Capture breakpoints, call stacks, and variable state.

### Subagent-Driven Development
Delegate bounded tasks with full context, but verify child output and integrate only after tests/diff review.

## Common Pitfalls

1. Planning without execution is not completion unless the user requested plan-only mode.
2. Debugging starts with reproduction, not edits.
3. Tests must actually fail before implementation in TDD.
4. Subagent summaries are self-reports; verify artifacts yourself.

## Verification Checklist

- [ ] Chosen workflow mode matches the task.
- [ ] Evidence, tests, or review output backs the result.
- [ ] Changes are scoped and reversible.
- [ ] Final answer names commands run and outcomes.
