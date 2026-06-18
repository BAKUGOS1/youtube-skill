#!/usr/bin/env python3
"""Fetch and normalize a YouTube transcript."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{6,20}$")


def video_id_from(value: str) -> str:
    value = value.strip()
    if VIDEO_ID_RE.fullmatch(value):
        return value
    parsed = urlparse(value if "://" in value else f"https://{value}")
    host = parsed.netloc.lower().split(":")[0]
    if host in {"youtu.be", "www.youtu.be"}:
        candidate = parsed.path.strip("/").split("/")[0]
    elif host.endswith("youtube.com") or host.endswith("youtube-nocookie.com"):
        if parsed.path == "/watch":
            candidate = parse_qs(parsed.query).get("v", [""])[0]
        else:
            parts = [part for part in parsed.path.split("/") if part]
            candidate = parts[1] if len(parts) > 1 and parts[0] in {"shorts", "embed", "live"} else ""
    else:
        candidate = ""
    if not VIDEO_ID_RE.fullmatch(candidate):
        raise ValueError(f"Could not parse a YouTube video ID from: {value}")
    return candidate


def normalize(video_id: str, transcript: object, translated_to: str | None = None) -> dict:
    snippets = transcript.to_raw_data()
    segments = []
    for item in snippets:
        text = " ".join(str(item.get("text", "")).split())
        if not text:
            continue
        start = round(float(item.get("start", 0)), 3)
        duration = round(float(item.get("duration", 0)), 3)
        segments.append({"text": text, "start": start, "duration": duration, "end": round(start + duration, 3)})
    return {
        "schema_version": "1.0",
        "video_id": video_id,
        "source_url": f"https://www.youtube.com/watch?v={video_id}",
        "language": getattr(transcript, "language", None),
        "language_code": getattr(transcript, "language_code", None),
        "is_generated": getattr(transcript, "is_generated", None),
        "translated_to": translated_to,
        "segments": segments,
    }


def as_markdown(data: dict) -> str:
    lines = [f"# YouTube transcript: {data['video_id']}", "", f"- Language: {data.get('language') or data.get('language_code') or 'unknown'}", f"- Generated captions: {data.get('is_generated')}", ""]
    for segment in data["segments"]:
        minutes, seconds = divmod(int(segment["start"]), 60)
        hours, minutes = divmod(minutes, 60)
        lines.append(f"- **[{hours:02d}:{minutes:02d}:{seconds:02d}]** {segment['text']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--languages", default="en")
    parser.add_argument("--translate")
    parser.add_argument("--list", action="store_true", dest="list_tracks")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("Install dependency: pip install youtube-transcript-api", file=sys.stderr)
        return 2
    try:
        video_id = video_id_from(args.video)
        api = YouTubeTranscriptApi()
        if args.list_tracks:
            rows = [{"language": track.language, "language_code": track.language_code, "is_generated": track.is_generated, "is_translatable": track.is_translatable} for track in api.list(video_id)]
            rendered = json.dumps(rows, ensure_ascii=False, indent=2)
        else:
            languages = [part.strip() for part in args.languages.split(",") if part.strip()]
            track = api.list(video_id).find_transcript(languages)
            if args.translate:
                track = track.translate(args.translate)
            data = normalize(video_id, track.fetch(), args.translate)
            rendered = json.dumps(data, ensure_ascii=False, indent=2) if args.format == "json" else as_markdown(data)
    except Exception as exc:
        print(f"Transcript retrieval failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    if args.output:
        args.output.write_text(rendered + ("" if rendered.endswith("\n") else "\n"), encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
