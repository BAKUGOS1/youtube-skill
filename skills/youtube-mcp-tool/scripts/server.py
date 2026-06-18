#!/usr/bin/env python3
"""Minimal read-oriented YouTube MCP server."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from urllib.parse import parse_qs, urlparse

from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi

mcp = FastMCP("youtube-tools")
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{6,20}$")


def parse_video_id(value: str) -> str:
    value = value.strip()
    if VIDEO_ID_RE.fullmatch(value):
        return value
    parsed = urlparse(value if "://" in value else f"https://{value}")
    host = parsed.netloc.lower().split(":")[0]
    candidate = ""
    if host in {"youtu.be", "www.youtu.be"}:
        candidate = parsed.path.strip("/").split("/")[0]
    elif host.endswith("youtube.com") or host.endswith("youtube-nocookie.com"):
        if parsed.path == "/watch":
            candidate = parse_qs(parsed.query).get("v", [""])[0]
        else:
            parts = [part for part in parsed.path.split("/") if part]
            if len(parts) > 1 and parts[0] in {"shorts", "embed", "live"}:
                candidate = parts[1]
    if not VIDEO_ID_RE.fullmatch(candidate):
        raise ValueError("invalid_video: could not parse a YouTube video ID")
    return candidate


@mcp.tool()
def list_youtube_transcripts(video: str) -> dict:
    """List public caption tracks for a YouTube video."""
    video_id = parse_video_id(video)
    tracks = []
    for track in YouTubeTranscriptApi().list(video_id):
        tracks.append({"language": track.language, "language_code": track.language_code, "is_generated": track.is_generated, "is_translatable": track.is_translatable})
    return {"schema_version": "1.0", "video_id": video_id, "tracks": tracks}


@mcp.tool()
def get_youtube_transcript(video: str, languages: list[str] | None = None, translate_to: str | None = None, max_segments: int = 5000) -> dict:
    """Retrieve a normalized, timestamped public YouTube transcript."""
    video_id = parse_video_id(video)
    max_segments = min(max(max_segments, 1), 10000)
    track = YouTubeTranscriptApi().list(video_id).find_transcript(languages or ["en"])
    if translate_to:
        track = track.translate(translate_to)
    fetched = track.fetch()
    rows = []
    for item in fetched.to_raw_data()[:max_segments]:
        text = " ".join(str(item.get("text", "")).split())
        if not text:
            continue
        start = round(float(item.get("start", 0)), 3)
        duration = round(float(item.get("duration", 0)), 3)
        rows.append({"text": text, "start": start, "duration": duration, "end": round(start + duration, 3)})
    return {
        "schema_version": "1.0",
        "video_id": video_id,
        "source_url": f"https://www.youtube.com/watch?v={video_id}",
        "language": fetched.language,
        "language_code": fetched.language_code,
        "is_generated": fetched.is_generated,
        "translated_to": translate_to,
        "truncated": len(fetched) > max_segments,
        "segments": rows,
    }


@mcp.tool()
def get_youtube_metadata(video: str) -> dict:
    """Inspect bounded public YouTube metadata without downloading media."""
    if not shutil.which("yt-dlp"):
        raise RuntimeError("dependency_missing: yt-dlp is not installed")
    completed = subprocess.run(["yt-dlp", "--skip-download", "--dump-single-json", "--no-playlist", video], check=False, capture_output=True, text=True, timeout=90)
    if completed.returncode:
        raise RuntimeError(f"metadata_failed: {completed.stderr.strip()[:500]}")
    raw = json.loads(completed.stdout)
    allowed = ("id", "title", "description", "channel", "channel_id", "uploader", "upload_date", "duration", "live_status", "webpage_url", "thumbnail", "view_count", "like_count", "categories", "tags")
    return {"schema_version": "1.0", **{key: raw.get(key) for key in allowed}}


if __name__ == "__main__":
    mcp.run(transport="stdio")
