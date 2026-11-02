---
name: productivity-integrations
description: "Use when automating productivity SaaS and document workflows: Airtable, Google Workspace, Linear, Maps, Notion, OCR/PDFs, PowerPoint, and meeting pipelines."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [productivity, docs, sheets, gmail, airtable, linear, notion, maps, pdf, powerpoint]
    related_skills: []
---

# Productivity Integrations

## Overview

This umbrella skill covers structured productivity work across SaaS APIs and document formats. It provides a routing layer for records, mail/calendar/drive/docs/sheets, task trackers, geocoding, Notion, PDFs/OCR, slide decks, and meeting-summary pipelines.

## When to Use

- CRUD/upsert/query work in Airtable or Notion.
- Gmail, Calendar, Drive, Docs, or Sheets operations.
- Linear issue/project/team workflows.
- Geocoding, POI lookup, routes, or timezones.
- Extracting text from PDFs/scans or editing PDFs.
- Creating, reading, or editing PowerPoint decks.
- Operating Teams meeting summary pipelines.

## Integration Modes

### Records and Databases
For Airtable/Notion/Sheets, identify base/database/sheet IDs, schemas, filters, and idempotency keys before writing.

### Workspace APIs
For Google Workspace, verify scopes and use purpose-built scripts/CLIs. Read back created/updated resources by ID.

### Project Tracking
For Linear, map team/project/state/label names to IDs and avoid duplicate issues by searching first.

### Maps
Include provider, coordinates, route assumptions, and timezone/date context.

### Documents and Decks
Preserve original files, write outputs to new paths unless instructed, and verify by extracting/readback or rendering thumbnails.

### Meeting Pipelines
Treat transcript ingestion, speaker labeling, summarization, and delivery as separate verifiable stages.

## Common Pitfalls

1. SaaS APIs require stable IDs; names alone can be ambiguous.
2. Document edits are destructive if performed in place; keep backups.
3. OCR can hallucinate or reorder text; sample-check important pages.
4. Calendar/timezone operations must include timezone explicitly.

## Verification Checklist

- [ ] Target IDs/scopes resolved.
- [ ] Writes are idempotent or explicitly intended.
- [ ] Created/edited resources were read back.
- [ ] Files have output paths and backups when appropriate.
