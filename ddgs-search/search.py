#!/usr/bin/env python3
"""Web search via DuckDuckGo (ddgs). Run with: uv run search.py"""
# /// script
# requires-python = ">=3.10"
# dependencies = ["ddgs"]
# ///

import argparse
import sys

from ddgs import DDGS


def main():
    parser = argparse.ArgumentParser(description="Search the web via DuckDuckGo")
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument("-n", "--num", type=int, default=5, help="Number of results (default: 5, max: 20)")
    parser.add_argument("--region", default="wt-wt", help="Region code (default: wt-wt for no region)")
    parser.add_argument("--timelimit", choices=["d", "w", "m", "y"], help="Time filter: d=day, w=week, m=month, y=year")
    args = parser.parse_args()

    query = " ".join(args.query)
    num = min(args.num, 20)

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(
                query,
                region=args.region,
                timelimit=args.timelimit,
                max_results=num,
            ))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print("No results found.", file=sys.stderr)
        sys.exit(0)

    for i, r in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(f"Title: {r.get('title', '')}")
        print(f"Link: {r.get('href', '')}")
        print(f"Snippet: {r.get('body', '')}")
        print()


if __name__ == "__main__":
    main()
