#!/usr/bin/env python3
"""Construct and optionally execute a bounded yt-dlp command."""

from __future__ import annotations

import argparse
import json
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

DOWNLOAD_MODES = {"subtitles", "audio", "video", "thumbnail"}


def build_command(args: argparse.Namespace) -> list[str]:
    command = ["yt-dlp", "--no-progress", "--retries", str(args.retries), "--fragment-retries", str(args.retries), "--max-filesize", args.max_filesize, "--paths", str(args.output_dir), "--output", "%(title).160B [%(id)s].%(ext)s"]
    if args.mode == "metadata":
        command += ["--skip-download", "--dump-single-json"]
    elif args.mode == "formats":
        command += ["--list-formats"]
    elif args.mode == "subtitles":
        command += ["--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", args.languages, "--sub-format", "vtt/srt/best"]
    elif args.mode == "audio":
        command += ["--extract-audio", "--audio-format", args.audio_format, "--audio-quality", "0"]
    elif args.mode == "thumbnail":
        command += ["--skip-download", "--write-thumbnail"]
    elif args.mode == "video":
        command += ["--format", args.format]
    if args.playlist_end:
        command += ["--playlist-end", str(args.playlist_end)]
    else:
        command += ["--no-playlist"]
    command.append(args.url)
    return command


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--mode", choices=("metadata", "formats", "subtitles", "audio", "video", "thumbnail"), default="metadata")
    parser.add_argument("--output-dir", type=Path, default=Path("youtube-output"))
    parser.add_argument("--languages", default="en.*")
    parser.add_argument("--audio-format", choices=("m4a", "mp3", "wav", "opus"), default="m4a")
    parser.add_argument("--format", default="bv*+ba/b")
    parser.add_argument("--playlist-end", type=int)
    parser.add_argument("--max-filesize", default="2G")
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--confirm-rights", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.mode in DOWNLOAD_MODES and not args.confirm_rights:
        parser.error(f"--confirm-rights is required for {args.mode} extraction")
    if args.playlist_end is not None and not 1 <= args.playlist_end <= 500:
        parser.error("--playlist-end must be between 1 and 500")
    command = build_command(args)
    if args.dry_run:
        print(json.dumps({"argv": command, "display": shlex.join(command)}, indent=2))
        return 0
    if not shutil.which("yt-dlp"):
        print("yt-dlp is not installed or not on PATH", file=sys.stderr)
        return 2
    args.output_dir.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(command, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
