#!/usr/bin/env python3
"""Rank transcript chunks with a deterministic lexical scorer."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path

TOKEN_RE = re.compile(r"[\w'-]+", re.UNICODE)


def tokens(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text) if len(token) > 1]


def rank(chunks: list[dict], query: str, top_k: int) -> list[dict]:
    query_terms = Counter(tokens(query))
    docs = [Counter(tokens(str(chunk.get("text", "")))) for chunk in chunks]
    doc_freq = Counter(term for doc in docs for term in doc)
    total = max(len(docs), 1)
    scored = []
    for chunk, doc in zip(chunks, docs):
        score = 0.0
        for term, q_count in query_terms.items():
            if term not in doc:
                continue
            idf = math.log((total + 1) / (doc_freq[term] + 1)) + 1
            score += (1 + math.log(doc[term])) * idf * q_count
        if score:
            scored.append({"score": round(score, 4), "chunk_id": chunk.get("chunk_id"), "start": chunk.get("start"), "end": chunk.get("end"), "text": chunk.get("text")})
    return sorted(scored, key=lambda item: item["score"], reverse=True)[:top_k]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=6)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    result = rank(data.get("chunks", []), args.query, max(args.top_k, 1))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
