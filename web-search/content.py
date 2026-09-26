#!/usr/bin/env python3
"""Fetch a URL and extract its main readable content as markdown (boilerplate such as navigation is stripped)."""
# /// script
# requires-python = ">=3.10"
# dependencies = ["primp", "trafilatura"]
# ///

import argparse
import sys

import primp
import trafilatura

DEFAULT_TIMEOUT_SECONDS = 10
IMPERSONATE_BROWSER = "chrome"
IMPERSONATE_OS = "macos"
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


def extract_main_content(response):
    """Main-content extraction; falls back to full-page markdown when nothing is detected."""
    main_content = trafilatura.extract(
        response.text,
        url=str(response.url),
        output_format="markdown",
        include_links=True,
        include_tables=True,
        favor_recall=True,
    )
    return main_content or response.text_markdown


def main():
    parser = argparse.ArgumentParser(description="Extract readable webpage content as markdown")
    parser.add_argument("url", help="URL to extract")
    parser.add_argument(
        "--max-chars",
        type=nonnegative_int,
        default=DEFAULT_MAX_CHARS,
        help="Maximum output characters; use 0 for unlimited (default: 20000)",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Skip main-content extraction and return the whole page as markdown",
    )
    args = parser.parse_args()

    try:
        client = primp.Client(
            impersonate=IMPERSONATE_BROWSER,
            impersonate_os=IMPERSONATE_OS,
            follow_redirects=True,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
        response = client.get(args.url)
        response.raise_for_status()
        content = (response.text_markdown if args.full else extract_main_content(response)) or "(Could not extract content)"
        print(limit_content(content, args.max_chars))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
