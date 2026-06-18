#!/usr/bin/env python3
"""Create timestamp-preserving chunks from normalized transcript JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def chunk_segments(segments: list[dict], max_chars: int, overlap_seconds: float) -> list[dict]:
    chunks: list[dict] = []
    current: list[dict] = []
    size = 0
    for segment in segments:
        text = str(segment.get("text", "")).strip()
        if current and size + len(text) + 1 > max_chars:
            chunks.append(make_chunk(len(chunks), current))
            cutoff = float(current[-1].get("end", current[-1].get("start", 0))) - overlap_seconds
            current = [item for item in current if float(item.get("end", 0)) >= cutoff]
            size = sum(len(str(item.get("text", ""))) + 1 for item in current)
        current.append(segment)
        size += len(text) + 1
    if current:
        chunks.append(make_chunk(len(chunks), current))
    return chunks


def make_chunk(index: int, segments: list[dict]) -> dict:
    return {
        "chunk_id": index,
        "start": segments[0].get("start", 0),
        "end": segments[-1].get("end", segments[-1].get("start", 0)),
        "text": " ".join(str(item.get("text", "")).strip() for item in segments).strip(),
        "segments": segments,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--max-chars", type=int, default=12000)
    parser.add_argument("--overlap-seconds", type=float, default=15)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.max_chars < 500:
        parser.error("--max-chars must be at least 500")
    data = json.loads(args.input.read_text(encoding="utf-8"))
    result = {"schema_version": "1.0", "video_id": data.get("video_id"), "chunks": chunk_segments(data.get("segments", []), args.max_chars, args.overlap_seconds)}
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
