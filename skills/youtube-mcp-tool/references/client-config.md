# MCP client configuration

Use a local stdio server:

```json
{
  "mcpServers": {
    "youtube": {
      "command": "python",
      "args": [
        "/absolute/path/youtube-skill/skills/youtube-mcp-tool/scripts/server.py"
      ]
    }
  }
}
```

Operational checks:

1. Use an absolute script path.
2. Ensure the selected Python environment contains `mcp`, `youtube-transcript-api`, and `yt-dlp`.
3. Keep logs on stderr so stdout remains valid MCP transport.
4. Restart the MCP client after config changes.
5. Test tool discovery before testing a transcript call.

For remote HTTP transport, add authentication, request limits, timeouts, audit logging, and per-tenant secret isolation before deployment.
