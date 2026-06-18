# Normalized transcript schema

Use this JSON shape:

```json
{
  "schema_version": "1.0",
  "video_id": "dQw4w9WgXcQ",
  "source_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "language": "English",
  "language_code": "en",
  "is_generated": false,
  "translated_to": null,
  "segments": [
    {
      "text": "Example caption",
      "start": 12.4,
      "duration": 2.1,
      "end": 14.5
    }
  ]
}
```

Required invariants:

- `start`, `duration`, and `end` are seconds.
- Segments remain in source order.
- `end = start + duration`.
- Empty segments are omitted.
- Unknown metadata is `null`, not guessed.
