---
name: youtube-qa
description: Answer factual, analytical, educational, and comparison questions using one or more YouTube transcripts as the evidence base. Use when Codex must chat with a video, locate where a topic was discussed, explain a segment, verify whether a speaker made a claim, or provide timestamped answers without hallucinating beyond the transcript.
---

# YouTube Q&A

Answer from transcript evidence and make the evidence boundary visible.

## Workflow

1. Retrieve normalized transcripts with `$youtube-transcript`.
2. Convert long transcripts into chunks with `$youtube-summarizer`.
3. Run `scripts/rank_passages.py` for a lightweight first-pass retrieval.
4. Read the top passages plus neighboring context.
5. Answer with timestamps and identify the relevant video when multiple videos are loaded.
6. If evidence is absent or ambiguous, say so directly.

## Answer contract

Use:

1. Direct answer
2. Evidence with timestamp links or `HH:MM:SS`
3. Qualification or uncertainty

Do not say “the video proves” when the transcript only records a speaker's opinion.

## Retrieval

```bash
python scripts/rank_passages.py chunks.json \
  --query "What does the speaker recommend for retention?" \
  --top-k 6
```

Read [references/qa-grounding.md](references/qa-grounding.md) for answerability and citation rules.
