---
name: ddgs-search
description: Web search and content extraction via DuckDuckGo. Free, no API key required. Use for searching documentation, facts, or any web content.
---

# DuckDuckGo Search

Web search and content extraction using DuckDuckGo. No API key required.

## Setup

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

No additional setup needed. Dependencies are managed inline via uv script headers.

## Search

```bash
uv run {baseDir}/search.py "query"                         # Basic search (5 results)
uv run {baseDir}/search.py "query" -n 10                   # More results (max 20)
uv run {baseDir}/search.py "query" --timelimit d           # Results from last day
uv run {baseDir}/search.py "query" --timelimit w           # Results from last week
uv run {baseDir}/search.py "query" --region de-de          # Results from Germany
uv run {baseDir}/search.py "query" -n 3 --timelimit m      # Combined options
```

### Options

- `-n <num>` - Number of results (default: 5, max: 20)
- `--region <code>` - Region code (default: wt-wt for global). Examples: us-en, de-de, fr-fr
- `--timelimit <period>` - Filter by time:
  - `d` - Past day
  - `w` - Past week
  - `m` - Past month
  - `y` - Past year

## Extract Page Content

```bash
uv run {baseDir}/content.py https://example.com/article
```

Fetches a URL and extracts readable content as plain text.

## Output Format

```
--- Result 1 ---
Title: Page Title
Link: https://example.com/page
Snippet: Description from search results

--- Result 2 ---
...
```

## When to Use

- Searching for documentation or API references
- Looking up facts or current information
- Fetching content from specific URLs
- Any task requiring web search without an API key
