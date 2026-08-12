---
name: web-search
description: Web search
---

# DuckDuckGo Search

Web search and content extraction using DuckDuckGo. No API key required.

## Search

```bash
uv run {baseDir}/search.py "query"                         # Basic search (5 results)
uv run {baseDir}/search.py "query" -n 10                   # More results (max 20)
uv run {baseDir}/search.py "query" --timelimit d           # Results from last day
uv run {baseDir}/search.py "query" --region de-de          # Results from Germany
uv run {baseDir}/search.py "query" -n 3 --timelimit m      # Combined options
uv run {baseDir}/search.py "query" --backend brave         # Force a single specific backend
uv run {baseDir}/search.py "query" --timeout 3             # Fail slow providers faster
```

### Options

- `-n <num>` - Number of results (default: 5, max: 20)
- `--region <code>` - Region code (default: wt-wt for global). Examples: us-en, de-de, fr-fr
- `--backend <name>` - Search backend (default: auto). Options: auto, brave, google, bing, yahoo. `auto` queries all engines simultaneously with priority ordering — the most robust choice.
- `--timeout <seconds>` - Request timeout (default: 5)
- `--timelimit <period>` - Filter by time:
  - `d` - Past day
  - `w` - Past week
  - `m` - Past month
  - `y` - Past year

## Extract Page Content

Fetches a URL and extracts readable content as plain text.

```bash
uv run {baseDir}/content.py "https://example.com/article"
uv run {baseDir}/content.py "https://example.com/article" --max-chars 50000
```

Output is limited to 20,000 characters by default to avoid context bloat. Use
`--max-chars` to change the limit, or `--max-chars 0` for unlimited output.
