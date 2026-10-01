---
name: web-search
description: Digger web search, page content extraction, and searchable Instagram and GitHub repository collections with an optional API key.
---

# Digger Web Search

Web search and content extraction using the [Digger](https://digger.so) search API. The API works without a key at the anonymous search allowance; an optional bearer API key applies your plan's higher limit. Requests use `primp` with a Chrome TLS/HTTP2 fingerprint to avoid bot refusals.

## Optional API key

Set `DIGGER_API_KEY=dgr_...` in `.env` in your working directory or this skill's
directory. The search client reads the environment first, then the working
directory's `.env`, then the skill's `.env`; blank keys fall back to the next source.
Quoted values and dotenv comments are supported. Never print or commit the key.
Without a key the client omits Authorization and uses anonymous search.

## Search

```bash
uv run {baseDir}/search.py "query"                         # Basic search (5 results)
uv run {baseDir}/search.py "query" -n 10                   # More results (max 20)
uv run {baseDir}/search.py "query" --region de-de          # Results from Germany
uv run {baseDir}/search.py "query" --timeout 3             # Fail slow requests faster
uv run {baseDir}/search.py "local LLM" --collection code_repos --min-stars 0 --language Rust
uv run {baseDir}/search.py "Wurst" --collection instagram --mode profiles --language de --location Germany
uv run {baseDir}/search.py "Wurst" --collection instagram --mode posts --search-type keyword --language de --published-after 2026-09-01
```

### Options

- `-n <num>` - Number of results (default: 5, max: 20)
- `--region <code>` - Region code in country-language format (default: none). Examples: us-en, de-de, fr-fr
- `--timeout <seconds>` - Request timeout (default: 10)
- `--collection web|instagram|code_repos` - Select the Digger collection (default: `web`)
- `--mode profiles|posts` - Required for Instagram searches
- `--search-type semantic|keyword` - Instagram post search type; profiles are semantic only
- Instagram profile filters: `--language`, `--location`, `--verified`/`--no-verified`, `--profile-type`, `--min-followers`, `--max-followers`
- Instagram post filters: `--language`, `--published-after`, `--published-before`
- Code repository filters: `--language`, `--license`, `--min-stars`, `--include-forks`, `--include-archived`, `--created-after`, `--created-before`, `--page`

Collection searches use the same authenticated Digger client and API key lookup as web search. Results are printed as JSON objects so collection-specific fields remain available.

## Extract Page Content

Fetches a URL (Chrome-impersonated) and extracts the main readable content as markdown (navigation, footers and other boilerplate are stripped).

```bash
uv run {baseDir}/content.py "https://example.com/article"
uv run {baseDir}/content.py "https://example.com/article" --max-chars 50000
uv run {baseDir}/content.py "https://example.com/article" --full   # whole page, no boilerplate stripping
```

Output is limited to 20,000 characters by default to avoid context bloat. Use
`--max-chars` to change the limit, or `--max-chars 0` for unlimited output.

## Collections

Search the web, Instagram profiles and posts, or GitHub code repositories with the
same optional bearer key and your plan's search allowances. Without a key, the
anonymous search allowance applies. Discover endpoints and capabilities at
`GET https://digger.so/api/v1/collections`; consult
`https://digger.so/openapi.json` for all filters and response fields.

All search endpoints require `q` and accept `max_results` (1–20, default 10).
Collection responses identify the dataset with `collection`; their result fields
vary by collection, so consult the schema rather than assuming web result fields.

### Instagram — GET /api/v1/search/instagram

- `mode=profiles` (default): semantic profile search. Filters: `min_followers`,
  `max_followers`, `verified`, `profile_type` (`all`, `creator`, `business`),
  `language`, and `location`. Profiles support only `search_type=semantic`.
- `mode=posts`: search captions with `search_type=semantic` (default) or `keyword`.
  Supports `language`, `published_after`, and `published_before`.
- Follower, verification, profile type, and location filters apply only to profiles.
  Publication date filters apply only to posts. Instagram has no pagination.

### Code repositories — GET /api/v1/search/code_repos

Keyword search over GitHub repository names, descriptions, topics, and READMEs.
Filters: `language`, `license`, `min_stars`, `include_forks`, `include_archived`,
`created_after`, and `created_before`. The default star minimum is **1000**;
use `min_stars=0` to disable it. Forks and archived repositories are excluded by
default. Results include `created_at`.

Use `page` (starting at 1) for pagination; keep the query, filters, and `max_results`
unchanged across pages. Date filters use inclusive UTC dates in `YYYY-MM-DD` format.

```bash
curl --get -H "Authorization: Bearer $DIGGER_API_KEY" \
  --data-urlencode "q=rust async runtime" --data "language=Rust" \
  --data "min_stars=0" "https://digger.so/api/v1/search/code_repos"
```

Omit the Authorization header when no key is configured.

## Holon Trees (Digger Pro)

The same bearer key manages your Holon Trees. GET and PUT
`https://digger.so/api/holon-trees/{id}/document` read and replace a tree document,
so an agent can restructure it or file items in several folders. A rebuild replaces
hand edits.
