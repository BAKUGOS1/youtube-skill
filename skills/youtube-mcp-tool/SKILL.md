---
name: youtube-mcp-tool
description: Design, configure, test, and operate MCP tools for YouTube transcript retrieval, caption discovery, metadata inspection, and safe downstream analysis. Use when Codex must expose YouTube capabilities to an MCP-compatible agent, connect an existing YouTube MCP server, define tool schemas, troubleshoot transport or dependency issues, or scaffold a local stdio server.
---

# YouTube MCP Tool

Prefer a small, read-oriented MCP surface. Keep transcript retrieval, metadata inspection, summarization, and media extraction as distinct capabilities.

## Workflow

1. Decide whether to connect an existing MCP server or run the bundled server.
2. Inspect tool names and schemas before invoking them.
3. Pass video IDs/URLs and language preferences as structured arguments.
4. Return normalized transcript JSON rather than an unbounded text blob.
5. Add pagination or segment limits for long videos and playlists.
6. Keep media download outside the default MCP surface.
7. Test with an MCP inspector and one known public captioned video.

## Bundled server

Install dependencies from the repository root, then run:

```bash
python skills/youtube-mcp-tool/scripts/server.py
```

The server exposes:

- `get_youtube_transcript`
- `list_youtube_transcripts`
- `get_youtube_metadata`

Read [references/tool-contracts.md](references/tool-contracts.md) before changing schemas. Read [references/client-config.md](references/client-config.md) for stdio configuration.

## Design rules

- Use stable, verb-led tool names.
- Return typed objects with `schema_version`.
- Bound transcript segments and metadata output.
- Produce actionable errors without secrets or cookie values.
- Avoid hidden network calls beyond the invoked tool.
- Never add DRM, authentication bypass, or unrestricted download tools.
- Record whether captions are generated or translated.

## Existing-server evaluation

Compare servers on:

- supported languages and translation;
- manual/generated track selection;
- timestamp fidelity;
- playlist and metadata support;
- proxy/cookie handling;
- output bounds;
- maintenance and license;
- transport and client compatibility.
