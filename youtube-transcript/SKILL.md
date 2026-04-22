---
name: youtube-transcript
description: Fetch transcripts from YouTube videos for summarization and analysis. Raw timestamped output, or summary-ready text with an ad-removal prompt.
---

# YouTube Transcript

Fetch transcripts from YouTube videos. Python script that runs via `uv` with inline dependencies (no venv management needed).

Based on https://github.com/SeanPedersen/youtube-transcript-mcp.

## Setup

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/). Dependencies declared inline in the script and installed on first run.

## Usage

**Always quote the URL** — unquoted `?` and `&` trigger zsh glob expansion and the call fails with `no matches found`.

Raw timestamped transcript:

```bash
{baseDir}/transcript.py "$URL"
```

Summary-ready text (prepends an ad-removal prompt, strips timestamps):

```bash
{baseDir}/transcript.py "$URL" --summary
```

Accepts video ID or full URL:
- `EBw7gsDPAYQ`
- `"https://www.youtube.com/watch?v=EBw7gsDPAYQ"`
- `"https://youtu.be/EBw7gsDPAYQ"`
- `"https://www.youtube.com/shorts/EBw7gsDPAYQ"`

## Output

### Raw (default)

```
[0:00] All right. So, I got this UniFi Theta
[0:15] I took the camera out, painted it
[1:23] And here's the final result
```

### Summary mode

```
Remove any mention of sponsorships, ads, or promotional content from the following transcript:

All right. So, I got this UniFi Theta
I took the camera out, painted it
...
```

Pipe `--summary` output to an LLM to produce an ad-free summary.

## Notes

- Video must have captions (auto-generated or manual).
- Language preference: en, de, es, fr, ru.
