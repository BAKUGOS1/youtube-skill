#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cat > "$TMP/transcript.json" <<'JSON'
{
  "video_id": "demo12345",
  "source_url": "https://www.youtube.com/watch?v=demo12345",
  "language_code": "en",
  "is_generated": false,
  "segments": [
    {"text": "The first section explains transcript extraction.", "start": 0, "duration": 5, "end": 5},
    {"text": "The second section explains grounded video question answering.", "start": 10, "duration": 6, "end": 16},
    {"text": "Research requires timestamps and source provenance.", "start": 20, "duration": 5, "end": 25}
  ]
}
JSON

python "$ROOT/skills/youtube-summarizer/scripts/chunk_transcript.py" \
  "$TMP/transcript.json" --max-chars 500 --output "$TMP/chunks.json"
python "$ROOT/skills/youtube-qa/scripts/rank_passages.py" \
  "$TMP/chunks.json" --query "grounded question answering" --top-k 2 > "$TMP/ranked.json"
python "$ROOT/skills/youtube-research/scripts/build_corpus.py" \
  "$TMP/transcript.json" --output "$TMP/corpus.json"
python "$ROOT/skills/youtube-dlp-extractor/scripts/safe_yt_dlp.py" \
  "https://www.youtube.com/watch?v=demo12345" --mode metadata --dry-run > "$TMP/command.json"

python - "$TMP" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
assert json.loads((root / "chunks.json").read_text())["chunks"]
assert json.loads((root / "ranked.json").read_text())[0]["score"] > 0
assert len(json.loads((root / "corpus.json").read_text())["passages"]) == 3
assert json.loads((root / "command.json").read_text())["argv"][0] == "yt-dlp"
print("Smoke tests passed")
PY
