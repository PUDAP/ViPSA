---
name: research-intelligence
description: "Use when collecting research intelligence from papers, feeds, markets, wikis, and structured knowledge sources."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [research, arxiv, rss, markets, wiki, intelligence, monitoring]
    related_skills: [research-paper-writing]
---

# Research Intelligence

## Overview

This umbrella skill covers discovery and monitoring workflows that gather information before synthesis or writing: arXiv search, blog/RSS watching, Polymarket market data, and local/interlinked LLM wiki querying.

## When to Use

- Searching scholarly preprints or paper metadata.
- Monitoring blogs/RSS feeds for topic changes.
- Querying prediction markets, prices, order books, or history.
- Building/querying a local knowledge wiki for LLM or ML topics.
- Preparing evidence for a later literature review or report.

## Source Modes

### arXiv
Search by keyword, author, category, or ID. Capture title, authors, date, abstract, URL, and why each result matters. Prefer reproducible query strings.

### Blog/RSS Monitoring
Treat feeds as change streams. Store last-seen IDs/timestamps, summarize deltas, and separate factual excerpts from commentary.

### Polymarket / Market Data
Report market slug/ID, best bid/ask or price, liquidity, timestamp, and caveats. Do not overinterpret thin markets.

### LLM Wiki / Knowledge Base
Use for local knowledge retrieval and cross-linking. Keep source provenance and avoid treating generated summaries as primary evidence.

## Common Pitfalls

1. Mixing source retrieval and final synthesis hides uncertainty; keep notes/provenance.
2. Feeds and markets are time-sensitive; include timestamps.
3. Search APIs paginate; inspect enough results before concluding absence.
4. Query wording strongly shapes recall; retry with synonyms.

## Verification Checklist

- [ ] Source IDs/URLs/timestamps recorded.
- [ ] Query parameters are reproducible.
- [ ] Deltas distinguished from full historical state.
- [ ] Claims trace back to retrieved sources.
