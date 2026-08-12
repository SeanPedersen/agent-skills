#!/usr/bin/env python3
"""Fetch and extract readable content from a URL as markdown."""
# /// script
# requires-python = ">=3.10"
# dependencies = ["ddgs"]
# ///

import argparse
import sys

from ddgs import DDGS

DEFAULT_TIMEOUT_SECONDS = 5
DEFAULT_MAX_CHARS = 20_000
TRUNCATION_MARKER = "\n\n[Content truncated at the maximum character limit.]"


def nonnegative_int(value):
    parsed_value = int(value)
    if parsed_value < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return parsed_value


def limit_content(content, max_chars):
    if max_chars == 0 or len(content) <= max_chars:
        return content
    if max_chars <= len(TRUNCATION_MARKER):
        return TRUNCATION_MARKER[:max_chars]
    return content[:max_chars - len(TRUNCATION_MARKER)] + TRUNCATION_MARKER


def main():
    parser = argparse.ArgumentParser(description="Extract readable webpage content as markdown")
    parser.add_argument("url", help="URL to extract")
    parser.add_argument(
        "--max-chars",
        type=nonnegative_int,
        default=DEFAULT_MAX_CHARS,
        help="Maximum output characters; use 0 for unlimited (default: 20000)",
    )
    args = parser.parse_args()

    try:
        with DDGS(timeout=DEFAULT_TIMEOUT_SECONDS) as d:
            result = d.extract(args.url, fmt="text_markdown")
            content = result.get("content", "(Could not extract content)")
            print(limit_content(content, args.max_chars))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
