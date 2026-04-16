#!/usr/bin/env python3
"""Fetch and extract readable content from a URL as markdown."""
# /// script
# requires-python = ">=3.10"
# dependencies = ["ddgs"]
# ///

import sys

from ddgs import DDGS


def main():
    if len(sys.argv) < 2:
        print("Usage: content.py <url>", file=sys.stderr)
        print("\nExtracts readable content from a webpage as markdown.", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    try:
        with DDGS() as d:
            result = d.extract(url, fmt="text_markdown")
            print(result.get("content", "(Could not extract content)"))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
