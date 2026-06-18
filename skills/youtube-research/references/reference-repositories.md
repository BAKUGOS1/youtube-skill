# Reference repositories

Review licenses and current maintenance before reusing code. These repositories are design and implementation references, not automatic dependencies.

## Recommended foundation

| Repository | Use in this skill pack |
|---|---|
| `github.com/jdepoix/youtube-transcript-api` | Primary caption retrieval, language selection, translation, and timestamp schema |
| `github.com/yt-dlp/yt-dlp` | Metadata, subtitle, audio, playlist, and permitted media fallback |
| `github.com/kimtaeyoon83/mcp-server-youtube-transcript` | Minimal transcript MCP server pattern |
| `github.com/hancengiz/youtube-transcript-mcp` | MCP analysis workflow and sub-agent patterns |
| `github.com/vercel-labs/agent-skills` | Concise skill packaging and reusable instruction patterns |
| `github.com/Leonxlnx/taste-skill` | Opinionated quality constraints and non-generic output guidance |

## Transcript and caption implementations

- `github.com/jdepoix/youtube-transcript-api`
- `github.com/Kakulukian/youtube-transcript`
- `github.com/kimtaeyoon83/mcp-server-youtube-transcript`
- `github.com/jkawamoto/mcp-youtube-transcript`
- `github.com/hancengiz/youtube-transcript-mcp`
- `github.com/haron/yt-dlp-transcript`
- `github.com/BayramAnnakov/youtube-playlist-to-markdown`
- `github.com/forrestchang/youtube-reader`

## YouTube MCP and agent tools

- `github.com/ZubeidHendricks/youtube-mcp-server`
- `github.com/anaisbetts/mcp-youtube`
- `github.com/icraft2170/youtube-data-mcp-server`
- `github.com/ShawhinT/yt-mcp-agent`
- `github.com/0GiS0/youtube-mcp-server`
- `github.com/pauling-ai/youtube-mcp-server`
- `github.com/toorop/youtube-transcript-mcp`
- `github.com/arrrggghhh/youtube-transcript-mcp`
- `github.com/ergut/youtube-transcript-mcp`

## Research, summarization, and Q&A patterns

- `github.com/meguta12/youtube-research-tool`
- `github.com/taira-dev/youtube-research-tool`
- `github.com/OhidaAkter/youtube-summarizer-agent`
- `github.com/SatyamDevX/Youtube-Summarizer-Gen-AI-Agent`
- `github.com/print-ashish/Youtube_Summarizer_Q-A_Agent`
- `github.com/abdurrahimcs50/youtube_transcript_ai_agent`
- `github.com/ShubhSarin/youtube-study-helper`
- `github.com/Sandesh-Huli/rag-yt-chatbot`
- `github.com/Maria-Antony/uTube-Gist`
- `github.com/Chinwike1/chat-with-transcripts`
- `github.com/rmccorkl/tubesage`
- `github.com/svpino/youtube-rag`

## Selection guidance

- Use `youtube-transcript-api` for lightweight public-caption retrieval.
- Use `yt-dlp` when metadata, subtitles, playlists, audio, or extractor resilience is required.
- Use a small transcript-only MCP server as the baseline; add metadata deliberately.
- Use RAG repositories for chunking and retrieval ideas, not as proof that their answers are grounded.
- Keep summarization and Q&A separate so each has a clear output contract.
- Treat playlist and Whisper fallbacks as optional, more expensive paths.
- Avoid copying broad all-in-one agents that mix extraction, generation, storage, and UI without testable boundaries.
