---
name: youtube-transcript
description: Fetch transcripts from YouTube videos (urls)
---

# YouTube Transcript

Fetch transcripts from YouTube videos (for summarization).

## Setup

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/). Dependencies declared inline in the script and installed on first run.

## Usage

**Always quote the URL** — unquoted `?` and `&` trigger zsh glob expansion and the call fails with `no matches found`.

Raw timestamped transcript:

```bash
uv run {baseDir}/transcript.py "$URL"
```

Summary-ready text (prepends an ad-removal prompt, strips timestamps - recommended as default for better summarization):

```bash
uv run {baseDir}/transcript.py "$URL" --summary
```

Accepts video ID or full URL:
- `EBw7gsDPAYQ`
- `"https://www.youtube.com/watch?v=EBw7gsDPAYQ"`
- `"https://youtu.be/EBw7gsDPAYQ"`
- `"https://www.youtube.com/shorts/EBw7gsDPAYQ"`

## Notes

- Video must have captions (auto-generated or manual).
- Language preference: en, de, es, fr, ru.
