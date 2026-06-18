# MCP tool contracts

## `get_youtube_transcript`

Input:

```json
{
  "video": "YouTube URL or video ID",
  "languages": ["en", "hi"],
  "translate_to": null,
  "max_segments": 5000
}
```

Output:

```json
{
  "schema_version": "1.0",
  "video_id": "string",
  "language_code": "string",
  "is_generated": false,
  "translated_to": null,
  "truncated": false,
  "segments": []
}
```

## `list_youtube_transcripts`

Return track language, language code, generated/manual status, and translation support.

## `get_youtube_metadata`

Return bounded public metadata through `yt-dlp --skip-download`. Remove cookies, headers, raw formats, and excessively large fields.

## Errors

Return a concise category and message:

- `invalid_video`
- `captions_unavailable`
- `language_unavailable`
- `request_blocked`
- `dependency_missing`
- `metadata_failed`

Never include secrets, full HTTP headers, cookies, or proxy credentials.
