#!/usr/bin/env python3
"""Combine normalized transcript files into a provenance-preserving corpus."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    sources = []
    passages = []
    for path in args.inputs:
        data = json.loads(path.read_text(encoding="utf-8"))
        video_id = data.get("video_id")
        sources.append({"video_id": video_id, "source_url": data.get("source_url"), "language_code": data.get("language_code"), "is_generated": data.get("is_generated"), "file": path.name})
        for index, segment in enumerate(data.get("segments", [])):
            passages.append({"passage_id": f"{video_id}:{index}", "video_id": video_id, "start": segment.get("start"), "end": segment.get("end"), "text": segment.get("text")})
    corpus = {"schema_version": "1.0", "sources": sources, "passages": passages}
    rendered = json.dumps(corpus, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
