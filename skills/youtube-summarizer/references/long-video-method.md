# Long-video summarization

Use a hierarchical pass:

1. Partition into timestamp-preserving chunks.
2. Extract each chunk's thesis, claims, evidence, examples, and unresolved references.
3. Group adjacent chunks into topics.
4. Build a global outline from topic summaries.
5. Verify every global point against at least one original timestamp.
6. Run a coverage check: beginning, middle, conclusion, and any Q&A section.

For playlists, summarize each video first. Then synthesize across videos with explicit per-video provenance.
