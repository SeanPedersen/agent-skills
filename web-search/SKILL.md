---
name: web-search
description: Web search
---

# Digger Web Search

Web search and content extraction using the [Digger](https://digger.so) search API. No API key required. Requests use `primp` with a Chrome TLS/HTTP2 fingerprint to avoid bot refusals.

## Search

```bash
uv run {baseDir}/search.py "query"                         # Basic search (5 results)
uv run {baseDir}/search.py "query" -n 10                   # More results (max 20)
uv run {baseDir}/search.py "query" --region de-de          # Results from Germany
uv run {baseDir}/search.py "query" --timeout 3             # Fail slow requests faster
```

### Options

- `-n <num>` - Number of results (default: 5, max: 20)
- `--region <code>` - Region code in country-language format (default: none). Examples: us-en, de-de, fr-fr
- `--timeout <seconds>` - Request timeout (default: 10)

## Extract Page Content

Fetches a URL (Chrome-impersonated) and extracts the main readable content as markdown (navigation, footers and other boilerplate are stripped).

```bash
uv run {baseDir}/content.py "https://example.com/article"
uv run {baseDir}/content.py "https://example.com/article" --max-chars 50000
uv run {baseDir}/content.py "https://example.com/article" --full   # whole page, no boilerplate stripping
```

Output is limited to 20,000 characters by default to avoid context bloat. Use
`--max-chars` to change the limit, or `--max-chars 0` for unlimited output.
