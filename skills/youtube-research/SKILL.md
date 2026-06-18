---
name: youtube-research
description: Conduct structured research across YouTube videos, channels, or playlists using transcript evidence plus clearly separated external sources. Use when Codex must compare creators, synthesize multiple videos, build a literature-style review, extract recurring themes, inspect competing claims, create a source matrix, or produce a timestamp-cited research brief.
---

# YouTube Research

Build a traceable evidence set before writing conclusions.

## Workflow

1. Define the research question, inclusion criteria, time window, and desired depth.
2. Build a source list with video ID, URL, title, channel, publication date, and selection reason.
3. Retrieve each transcript with `$youtube-transcript`.
4. Run `scripts/build_corpus.py` to create a provenance-preserving corpus.
5. Extract claims, evidence, examples, methods, caveats, and disagreements per source.
6. Create the source matrix described in [references/research-method.md](references/research-method.md).
7. Synthesize patterns only after per-source analysis.
8. Separate transcript-derived findings from web research or analyst inference.

## Deliverable

- Research question and scope
- Source selection method
- Source matrix
- Findings by theme
- Agreements and contradictions
- Timestamped evidence
- Gaps and confidence
- Follow-up questions

## Corpus builder

```bash
python scripts/build_corpus.py transcripts/*.json --output corpus.json
```

For current metadata, platform policy, or external fact verification, search the web and cite primary sources. YouTube transcripts remain primary evidence for what speakers said.

## Integrity rules

- Do not rank a source as authoritative solely by views, subscribers, or production quality.
- Record unavailable or captionless videos instead of silently excluding them.
- Avoid duplicate counting when clips reuse the same original content.
- Mark sponsor messages, opinions, anecdotes, and empirical claims distinctly.
