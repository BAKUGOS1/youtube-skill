---
name: youtube-transcript
description: Retrieve, normalize, translate, and format timestamped YouTube captions or transcripts. Use when Codex must extract spoken content from a YouTube URL or video ID, select preferred caption languages, distinguish manual from auto-generated captions, preserve timestamps, or prepare transcript data for summarization, Q&A, research, subtitles, or downstream agents.
---

# YouTube Transcript

Retrieve the smallest reliable transcript artifact that satisfies the request.

## Workflow

1. Confirm the input is a YouTube URL or video ID.
2. Prefer existing captions through `youtube-transcript-api`.
3. Respect the requested language order; do not silently translate unless asked.
4. Preserve segment `start`, `duration`, and source-language metadata.
5. Normalize output to the schema in [references/transcript-schema.md](references/transcript-schema.md).
6. If captions are unavailable or blocked, report the exact failure and route to `$youtube-dlp-extractor` for permitted subtitle/audio fallback.
7. Save only the requested format. Prefer JSON for downstream processing and Markdown for humans.

## Run the bundled extractor

```bash
python scripts/fetch_transcript.py VIDEO_OR_URL \
  --languages en,hi \
  --format json \
  --output transcript.json
```

Use `--list` to inspect available caption tracks before fetching.

## Quality rules

- Keep timestamps attached to their original text.
- Remove repeated whitespace, not meaningful punctuation.
- Mark auto-generated captions with `is_generated: true`.
- Never invent missing words or timestamps.
- Treat translated captions as a derived artifact and record `translated_to`.
- For long videos, return the file plus a compact metadata summary instead of pasting the full transcript.

## Failure handling

Read [references/fallbacks.md](references/fallbacks.md) when captions are disabled, the video is unavailable, YouTube blocks the request, or authentication is required.

## Rights and privacy

Transcript access does not grant reuse rights. Do not bypass access controls. Do not expose cookies, proxy credentials, or private video data in outputs or logs.
