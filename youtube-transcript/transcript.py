#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "youtube-transcript-api>=1.2.1",
# ]
# ///
"""Fetch a YouTube transcript (raw timestamped, or summary-ready with ad-removal prompt)."""

import argparse
import re
import sys

from youtube_transcript_api import YouTubeTranscriptApi

LANGUAGES = ["en", "de", "es", "fr", "ru"]

ADBLOCK_PROMPT = (
    "Remove any mention of sponsorships, ads, or promotional content "
    "from the following transcript:\n\n"
)

URL_PATTERN = re.compile(
    r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})"
)
ID_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{11}$")


def extract_video_id(value: str) -> str:
    if ID_PATTERN.match(value):
        return value
    match = URL_PATTERN.search(value)
    if not match:
        raise ValueError(f"Invalid YouTube URL or video ID: {value}")
    return match.group(1)


def format_timestamp(seconds: float) -> str:
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def render_raw(snippets) -> str:
    return "\n".join(f"[{format_timestamp(s.start)}] {s.text}" for s in snippets)


def render_summary(snippets) -> str:
    return ADBLOCK_PROMPT + "\n".join(s.text for s in snippets)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a YouTube transcript.")
    parser.add_argument("video", help="YouTube video ID or URL")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Output summary-ready text prefixed with an ad-removal prompt (no timestamps).",
    )
    args = parser.parse_args()

    try:
        video_id = extract_video_id(args.video)
        snippets = YouTubeTranscriptApi().fetch(video_id, languages=LANGUAGES)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(render_summary(snippets) if args.summary else render_raw(snippets))
    return 0


if __name__ == "__main__":
    sys.exit(main())
