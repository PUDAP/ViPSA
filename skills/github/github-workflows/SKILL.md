---
name: github-workflows
description: "Use when operating GitHub repositories end-to-end: auth, repo management, issues, branches, PRs, reviews, CI, and codebase inspection."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, gh, git, pr, issues, review, ci, repository]
    related_skills: []
---

# GitHub Workflows

## Overview

This umbrella skill covers the complete GitHub lifecycle. A maintainer should load one GitHub operating manual, then use labeled subsections for authentication, repository setup, issues, PRs, code review, CI triage, releases, and codebase inspection.

## When to Use

- Authenticating or troubleshooting `gh`/git access.
- Creating, cloning, forking, or configuring repositories.
- Creating, triaging, labeling, or updating issues.
- Branching, committing, opening PRs, monitoring CI, or merging.
- Reviewing PR diffs or leaving comments.
- Inspecting repository language/LOC/structure before work.

## Workflow Sections

### Authentication
Run `gh auth status` before assuming credentials. For HTTPS remotes, check credential helpers; for SSH, check `ssh -T git@github.com`. Do not print tokens. Use OAuth/device flow or documented token scopes when access is missing.

### Repository Management
Inspect remotes and default branch before mutating. For new repos, set visibility, description, topics, and branch protection deliberately. For forks, track upstream explicitly.

### Issues
Use existing templates when present. Search before creating duplicates. Include reproduction steps, expected/actual behavior, environment, labels, and assignee/milestone only when known.

### PR Workflow
Create a focused branch, commit coherent changes, push, open PR with a body that links issues and describes verification. Monitor CI and address failures before claiming completion.

### Code Review
Review the diff, not just filenames. Check correctness, security, tests, compatibility, and maintainability. Prefer concrete comments tied to lines; summarize blocking vs non-blocking findings.

### Codebase Inspection
Use lightweight structure/LOC inspection before large edits. Identify generated/vendor directories and test layout so estimates and review scopes are grounded.

## Common Pitfalls

1. `gh auth login` credentials do not necessarily cover all GitHub APIs or Copilot APIs.
2. PR reviews should be based on fetched diff/branch state, not stale local assumptions.
3. CI failures are part of the deliverable; inspect logs before reporting success.
4. Never expose secrets from `gh auth token`, remotes with embedded credentials, or workflow logs.

## Verification Checklist

- [ ] `gh auth status`/git remote state checked when relevant.
- [ ] Target repo/branch/issue/PR number verified from live output.
- [ ] Side effects have URLs/IDs and were read back.
- [ ] CI/test status checked before declaring done.
