# Transcript fallback matrix

| Failure | Action |
|---|---|
| Requested language missing | List tracks and ask or use the next requested language |
| Manual captions missing | Use generated captions and mark them generated |
| Captions disabled | Use permitted audio transcription only if the user has rights |
| `RequestBlocked` / `IpBlocked` | Retry conservatively; use an approved proxy only when configured by the user |
| Age/private/member restriction | Request authorized access; never bypass the restriction |
| Empty or malformed captions | Try `yt-dlp` subtitle metadata, then validate the resulting VTT/SRT |
| Live stream still running | Explain that the final transcript may not yet exist |

Do not claim transcript completeness when the source is partial.
