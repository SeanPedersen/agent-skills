#!/usr/bin/env python3
"""Web search via DuckDuckGo (ddgs). Run with: uv run search.py"""
# /// script
# requires-python = ">=3.10"
# dependencies = ["ddgs"]
# ///

import argparse
import sys

from ddgs import DDGS

DEFAULT_BACKEND = "auto"
DEFAULT_NUM_RESULTS = 5
DEFAULT_REGION = "wt-wt"
DEFAULT_TIMEOUT_SECONDS = 5
MAX_RESULTS = 20
SEARCH_BACKENDS = ("auto", "brave", "google", "bing", "yahoo")


def positive_int(value):
    parsed_value = int(value)
    if parsed_value < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return parsed_value


def positive_float(value):
    parsed_value = float(value)
    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return parsed_value


def main():
    parser = argparse.ArgumentParser(description="Search the web via DuckDuckGo")
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument("-n", "--num", type=positive_int, default=DEFAULT_NUM_RESULTS, help="Number of results (default: 5, max: 20)")
    parser.add_argument("--region", default=DEFAULT_REGION, help="Region code (default: wt-wt for no region)")
    parser.add_argument("--timelimit", choices=["d", "w", "m", "y"], help="Time filter: d=day, w=week, m=month, y=year")
    parser.add_argument("--backend", choices=SEARCH_BACKENDS, default=DEFAULT_BACKEND, help="Search backend (default: auto). auto queries all engines simultaneously for best coverage.")
    parser.add_argument("--timeout", type=positive_float, default=DEFAULT_TIMEOUT_SECONDS, help="Request timeout in seconds (default: 5)")
    args = parser.parse_args()

    query = " ".join(args.query)
    num = min(args.num, MAX_RESULTS)

    try:
        with DDGS(timeout=args.timeout) as ddgs:
            results = list(ddgs.text(
                query,
                region=args.region,
                timelimit=args.timelimit,
                max_results=num,
                backend=args.backend,
            ))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print("No results found.", file=sys.stderr)
        sys.exit(1)

    for i, r in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(f"Title: {r.get('title', '')}")
        print(f"Link: {r.get('href', '')}")
        print(f"Snippet: {r.get('body', '')}")
        print()


if __name__ == "__main__":
    main()
