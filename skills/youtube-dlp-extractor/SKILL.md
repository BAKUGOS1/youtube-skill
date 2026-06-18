---
name: youtube-dlp-extractor
description: Inspect and extract permitted YouTube metadata, thumbnails, subtitles, audio, or video with yt-dlp and FFmpeg. Use when Codex needs a robust fallback for missing captions, format discovery, playlist metadata, local audio transcription input, or media download from content the user owns, licenses, or is authorized to process.
---

# YouTube yt-dlp Extractor

Default to metadata-only inspection. Require an explicit rights confirmation before downloading subtitles, audio, or video.

## Workflow

1. Confirm the URL and requested artifact.
2. Check that `yt-dlp` is installed and current.
3. Run metadata inspection first.
4. Select the least data-intensive artifact:
   - captions before audio
   - audio before video
   - one item before a playlist
5. Use `scripts/safe_yt_dlp.py` to construct or run a shell-safe command.
6. Validate output files and report source URL, format, language, duration, and size.

## Commands

Inspect without downloading:

```bash
python scripts/safe_yt_dlp.py URL --mode metadata
```

Preview a permitted subtitle extraction:

```bash
python scripts/safe_yt_dlp.py URL \
  --mode subtitles \
  --languages "en.*,hi.*" \
  --confirm-rights \
  --dry-run
```

Read [references/extraction-policy.md](references/extraction-policy.md) before media extraction and [references/recipes.md](references/recipes.md) for format recipes.

## Safety and reliability

- Never bypass DRM, paywalls, private access, age gates, or account controls.
- Never print cookie contents or secrets.
- Avoid `--no-check-certificates`, arbitrary postprocessor arguments, and shell interpolation.
- Use bounded retries, output templates, playlist limits, and size limits.
- Do not promise that a format or extractor will remain stable; YouTube changes frequently.
- Keep the original URL and metadata alongside derived files.
