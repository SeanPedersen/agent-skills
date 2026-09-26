#!/usr/bin/env python3
"""Web search via the Digger search API (https://digger.so). Run with: uv run search.py"""
# /// script
# requires-python = ">=3.10"
# dependencies = ["primp"]
# ///

import argparse
import os
import sys
from pathlib import Path

import primp

API_URL = "https://digger.so/api/v1/search"
DEFAULT_NUM_RESULTS = 5
DEFAULT_TIMEOUT_SECONDS = 10
MAX_RESULTS = 20
IMPERSONATE_BROWSER = "chrome"
IMPERSONATE_OS = "macos"
API_KEY_ENV_VAR = "DIGGER_API_KEY"
ENV_FILE = Path(__file__).parent / ".env"


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


def load_api_key():
    """Read the key from the environment, falling back to the skill's .env file."""
    if key := os.environ.get(API_KEY_ENV_VAR):
        return key
    if not ENV_FILE.is_file():
        return None
    for line in ENV_FILE.read_text().splitlines():
        name, _, value = line.strip().partition("=")
        if name == API_KEY_ENV_VAR:
            return value.strip().strip("\"'") or None
    return None


def fetch_results(query, num, region, timeout):
    params = {"q": query, "max_results": str(num)}
    if region:
        params["region"] = region
    api_key = load_api_key()
    client = primp.Client(
        impersonate=IMPERSONATE_BROWSER,
        impersonate_os=IMPERSONATE_OS,
        headers={"Authorization": f"Bearer {api_key}"} if api_key else None,
        timeout=timeout,
    )
    response = client.get(API_URL, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"HTTP {response.status_code}: {response.text}")
    return response.json().get("results", [])


def main():
    parser = argparse.ArgumentParser(description="Search the web via Digger")
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument("-n", "--num", type=positive_int, default=DEFAULT_NUM_RESULTS, help="Number of results (default: 5, max: 20)")
    parser.add_argument("--region", help="Region code in country-language format, e.g. us-en, de-de (default: none)")
    parser.add_argument("--timeout", type=positive_float, default=DEFAULT_TIMEOUT_SECONDS, help="Request timeout in seconds (default: 10)")
    args = parser.parse_args()

    query = " ".join(args.query)
    num = min(args.num, MAX_RESULTS)

    try:
        results = fetch_results(query, num, args.region, args.timeout)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print("No results found.", file=sys.stderr)
        sys.exit(1)

    for i, r in enumerate(results, 1):
        print(f"--- Result {i} ---")
        print(f"Title: {r.get('title', '')}")
        print(f"Link: {r.get('url', '')}")
        print(f"Snippet: {r.get('snippet', '')}")
        print()


if __name__ == "__main__":
    main()
