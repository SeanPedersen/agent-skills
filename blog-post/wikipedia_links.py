#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx"]
# ///
"""
Resolve Wikipedia URLs for a list of technical terms.

Usage:
    uv run wikipedia_links.py '["Python", "machine learning", "REST API"]'

Output:
    JSON object mapping each term to its Wikipedia URL (or null if not found).
"""

import json
import sys
import httpx

WIKIPEDIA_SEARCH_API = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_PAGE_BASE = "https://en.wikipedia.org/wiki/"
USER_AGENT = "blog-post-skill/1.0 (https://github.com/anthropics/agent-skills; seanpedersen96@protonmail.com)"


def search_wikipedia(term: str, client: httpx.Client) -> str | None:
    params = {
        "action": "query",
        "list": "search",
        "srsearch": term,
        "format": "json",
        "srlimit": 1,
        "srnamespace": 0,
    }
    try:
        response = client.get(WIKIPEDIA_SEARCH_API, params=params, timeout=10)
        response.raise_for_status()
        results = response.json().get("query", {}).get("search", [])
        if not results:
            return None
        title = results[0]["title"]
        return WIKIPEDIA_PAGE_BASE + title.replace(" ", "_")
    except Exception:
        return None


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: uv run wikipedia_links.py '<json-array-of-terms>'", file=sys.stderr)
        sys.exit(1)

    terms: list[str] = json.loads(sys.argv[1])
    results: dict[str, str | None] = {}

    with httpx.Client(headers={"User-Agent": USER_AGENT}) as client:
        for term in terms:
            results[term] = search_wikipedia(term, client)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
