# YouTube Skills

Six composable agent skills for transcript retrieval, grounded summarization, transcript Q&A, multi-video research, safe `yt-dlp` extraction, and MCP integration.

## Skills

- `youtube-transcript`
- `youtube-summarizer`
- `youtube-qa`
- `youtube-research`
- `youtube-dlp-extractor`
- `youtube-mcp-tool`

Each skill follows the `SKILL.md` format and includes only the scripts and references needed for its workflow.

## Install dependencies

```bash
python -m pip install -r requirements.txt
```

FFmpeg is required only for audio/video post-processing. Media extraction must be limited to content the user owns, licenses, or is authorized to process.

## Validate

```bash
./scripts/validate_all.sh
./scripts/smoke_test.sh
```
