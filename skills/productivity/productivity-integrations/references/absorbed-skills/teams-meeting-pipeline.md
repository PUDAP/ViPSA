# Absorbed skill: teams-meeting-pipeline

Original package: `productivity/teams-meeting-pipeline` archived after consolidation into `productivity-integrations`.

Support files copied: none.

## First 80 lines of original SKILL.md for provenance

```markdown
---
name: teams-meeting-pipeline
description: "Operate the Teams meeting summary pipeline via Hermes CLI — summarize meetings, inspect pipeline status, replay jobs, manage Microsoft Graph subscriptions."
version: 1.1.0
author: Hermes Agent + Teknium
license: MIT
prerequisites:
  env_vars: [MSGRAPH_TENANT_ID, MSGRAPH_CLIENT_ID, MSGRAPH_CLIENT_SECRET]
  commands: [hermes]
metadata:
  hermes:
    tags: [Teams, Microsoft Graph, Meetings, Productivity, Operations]
    related_docs:
      - /docs/guides/microsoft-graph-app-registration
      - /docs/user-guide/messaging/teams-meetings
      - /docs/guides/operate-teams-meeting-pipeline
---

# Teams Meeting Pipeline

Use this skill whenever the user asks about Microsoft Teams meeting summaries, transcripts, recordings, action items, Graph subscriptions, or any operational question about the Teams meeting pipeline. Works in any language — the triggers below are examples, not an exhaustive list.

Everything operator-facing is a `hermes teams-pipeline` subcommand run via the terminal tool. There are no new model tools for this pipeline — the CLI is the surface.

## When to use this skill

The user is asking to:
- summarize a Teams meeting / extract action items / pull meeting notes
- check pipeline status, inspect a stored meeting job, or see recent meetings
- replay / re-run a stored job that failed or needs a fresh summary
- validate Microsoft Graph setup after changing env or config
- troubleshoot "meeting summary never arrived" or "no new meetings are ingesting"
- manage Graph webhook subscriptions (create, renew, delete, inspect)
- set up automated subscription renewal (see pitfall below)

Multilingual trigger examples (not exhaustive):
- English: "summarize the Teams meeting", "pipeline status", "replay job X"
- Turkish: "Teams meeting özetle", "action item çıkar", "toplantı notu", "pipeline durumu", "replay job"

## Prerequisites

Before using the pipeline, verify these are set in `~/.hermes/.env`:

```bash
MSGRAPH_TENANT_ID=...
MSGRAPH_CLIENT_ID=...
MSGRAPH_CLIENT_SECRET=...
```

If any are missing, direct the user to the Azure app registration guide at `/docs/guides/microsoft-graph-app-registration` — they need an Azure AD app registration with admin-consented Graph application permissions before the pipeline will work.

## Command reference

### Status and inspection (start here)

```bash
hermes teams-pipeline validate              # config snapshot — run first after any change
hermes teams-pipeline token-health          # Graph token status
hermes teams-pipeline token-health --force-refresh   # force a fresh token acquisition
hermes teams-pipeline list                  # recent meeting jobs
hermes teams-pipeline list --status failed  # only failed jobs
hermes teams-pipeline show <job-id>         # full detail of one job
hermes teams-pipeline subscriptions         # current Graph webhook subscriptions
```

### Re-running / debugging

```bash
hermes teams-pipeline run <job-id>          # replay a stored job (re-summarize, re-deliver)
hermes teams-pipeline fetch --meeting-id <id>   # dry-run: resolve meeting + transcript without persisting
hermes teams-pipeline fetch --join-web-url "<url>"   # dry-run by join URL
```

### Subscription management

```bash
hermes teams-pipeline subscribe \
  --resource communications/onlineMeetings/getAllTranscripts \
  --notification-url https://<your-public-host>/msgraph/webhook \
  --client-state "$MSGRAPH_WEBHOOK_CLIENT_STATE"
```
