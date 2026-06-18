---
name: youtube-summarizer
description: Produce faithful summaries, notes, chapters, takeaways, action items, and timestamped outlines from YouTube transcripts. Use when Codex must summarize one video or playlist item at different detail levels while grounding every important claim in transcript evidence and avoiding unsupported additions.
---

# YouTube Summarizer

Summarize transcript content, not assumptions about the video.

## Workflow

1. Obtain normalized timestamped data with `$youtube-transcript`.
2. Select an output profile from [references/summary-profiles.md](references/summary-profiles.md).
3. For long transcripts, run `scripts/chunk_transcript.py` and summarize each chunk independently.
4. Merge chunk summaries by topic, removing repetition without dropping disagreements or caveats.
5. Attach timestamps to major claims, chapters, examples, and action items.
6. Add a limitations note when captions are partial, generated, translated, or noisy.

## Default output

- One-sentence thesis
- Five to ten key points
- Timestamped chapter outline
- Important examples or evidence
- Action items, if the speaker gives any
- Caveats and unclear passages

## Grounding rules

- Do not add facts from the title, thumbnail, comments, or general knowledge unless labeled external context.
- Distinguish the speaker's claim from established fact.
- Preserve uncertainty, criticism, and conflicting viewpoints.
- Quote sparingly; prefer paraphrase with timestamps.
- Never create a timestamp that does not map to a source segment.

## Chunking

```bash
python scripts/chunk_transcript.py transcript.json \
  --max-chars 12000 \
  --overlap-seconds 15 \
  --output chunks.json
```

Read [references/long-video-method.md](references/long-video-method.md) for multi-hour videos and playlists.
