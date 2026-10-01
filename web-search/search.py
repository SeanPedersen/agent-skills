#!/usr/bin/env python3
"""Search Digger web, Instagram, and GitHub repository collections."""
# /// script
# requires-python = ">=3.12"
# dependencies = ["primp", "python-dotenv"]
# ///

import argparse
import json
import os
import sys
from pathlib import Path

import primp
from dotenv import dotenv_values

API_URL = "https://digger.so/api/v1/search"
COLLECTION_URLS = {
    "instagram": "https://digger.so/api/v1/search/instagram",
    "code_repos": "https://digger.so/api/v1/search/code_repos",
}
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


def nonnegative_int(value):
    parsed_value = int(value)
    if parsed_value < 0:
        raise argparse.ArgumentTypeError("must be at least 0")
    return parsed_value


def positive_float(value):
    parsed_value = float(value)
    if parsed_value <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    return parsed_value


def load_api_key():
    """Prefer the environment, then the working directory and skill .env files."""
    if key := os.environ.get(API_KEY_ENV_VAR, "").strip():
        return key
    for env_file in (Path.cwd() / ".env", ENV_FILE):
        key = dotenv_values(env_file, interpolate=False).get(API_KEY_ENV_VAR)
        if key and key.strip():
            return key.strip()
    return None


def build_client(timeout):
    api_key = load_api_key()
    return primp.Client(
        impersonate=IMPERSONATE_BROWSER,
        impersonate_os=IMPERSONATE_OS,
        headers={"Authorization": f"Bearer {api_key}"} if api_key else None,
        timeout=timeout,
    )


def fetch_results(query, num, region, timeout):
    params = {"q": query, "max_results": str(num)}
    if region:
        params["region"] = region
    response = build_client(timeout).get(API_URL, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"HTTP {response.status_code}: {response.text}")
    return response.json().get("results", [])


def fetch_collection(collection, query, num, timeout, options):
    params = {"q": query, "max_results": str(num)}
    params.update({key: str(value).lower() if isinstance(value, bool) else str(value) for key, value in options.items()})
    response = build_client(timeout).get(COLLECTION_URLS[collection], params=params)
    if response.status_code != 200:
        raise RuntimeError(f"HTTP {response.status_code}: {response.text}")
    return response.json().get("results", [])


def add_collection_arguments(parser):
    parser.add_argument("--collection", choices=("web", "instagram", "code_repos"), default="web", help="Digger collection to search")
    parser.add_argument("--mode", choices=("profiles", "posts"), help="Instagram search mode")
    parser.add_argument("--search-type", choices=("semantic", "keyword"), help="Instagram post search type")
    parser.add_argument("--language", help="Language filter for Instagram")
    parser.add_argument("--location", help="Location filter for Instagram profiles")
    parser.add_argument("--verified", action=argparse.BooleanOptionalAction, default=None, help="Filter Instagram profiles by verification")
    parser.add_argument("--profile-type", choices=("all", "creator", "business"), help="Instagram profile type")
    parser.add_argument("--min-followers", type=nonnegative_int, help="Minimum Instagram profile followers")
    parser.add_argument("--max-followers", type=nonnegative_int, help="Maximum Instagram profile followers")
    parser.add_argument("--min-stars", type=nonnegative_int, help="Minimum GitHub repository stars; set 0 to disable the default")
    parser.add_argument("--license", dest="repo_license", help="GitHub repository license filter")
    parser.add_argument("--include-forks", action="store_true", help="Include GitHub forks")
    parser.add_argument("--include-archived", action="store_true", help="Include archived GitHub repositories")
    parser.add_argument("--created-after", help="Inclusive repository creation date (YYYY-MM-DD)")
    parser.add_argument("--created-before", help="Inclusive repository creation date (YYYY-MM-DD)")
    parser.add_argument("--published-after", help="Instagram post publication date (YYYY-MM-DD)")
    parser.add_argument("--published-before", help="Instagram post publication date (YYYY-MM-DD)")
    parser.add_argument("--page", type=positive_int, default=1, help="Code repository results page")


def collection_options(args):
    if args.collection == "instagram":
        if args.min_stars is not None or args.repo_license or args.include_forks or args.include_archived or args.created_after or args.created_before or args.page != 1:
            raise ValueError("Repository-only filters cannot be used with Instagram")
        if args.mode is None:
            raise ValueError("Instagram searches require --mode profiles or --mode posts")
        if args.mode == "profiles" and args.search_type:
            raise ValueError("Instagram profile searches use semantic search and do not accept --search-type")
        if args.mode == "profiles" and (args.published_after or args.published_before):
            raise ValueError("Publication date filters apply only to Instagram posts")
        if args.mode == "posts" and any((args.location, args.verified is not None, args.profile_type, args.min_followers, args.max_followers)):
            raise ValueError("Profile-only filters cannot be used with Instagram posts")
        options = {"mode": args.mode}
        if args.search_type:
            options["search_type"] = args.search_type
        for arg_name, api_name in (("language", "language"), ("location", "location"), ("profile_type", "profile_type"), ("min_followers", "min_followers"), ("max_followers", "max_followers"), ("published_after", "published_after"), ("published_before", "published_before")):
            value = getattr(args, arg_name)
            if value is not None:
                options[api_name] = value
        if args.verified is not None:
            options["verified"] = str(args.verified).lower()
        return options

    if args.collection == "code_repos":
        if args.mode or args.search_type or args.location or args.verified is not None or args.profile_type or args.min_followers or args.max_followers or args.published_after or args.published_before:
            raise ValueError("Instagram-only options cannot be used with code_repos")
        options = {"page": args.page}
        for arg_name, api_name in (("language", "language"), ("repo_license", "license"), ("created_after", "created_after"), ("created_before", "created_before")):
            value = getattr(args, arg_name)
            if value is not None:
                options[api_name] = value
        if args.min_stars is not None:
            options["min_stars"] = args.min_stars
        if args.include_forks:
            options["include_forks"] = "true"
        if args.include_archived:
            options["include_archived"] = "true"
        return options

    return {}


def main():
    parser = argparse.ArgumentParser(description="Search Digger web, Instagram, and GitHub repository collections")
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument("-n", "--num", type=positive_int, default=DEFAULT_NUM_RESULTS, help="Number of results (default: 5, max: 20)")
    parser.add_argument("--region", help="Region code in country-language format, e.g. us-en, de-de (default: none)")
    parser.add_argument("--timeout", type=positive_float, default=DEFAULT_TIMEOUT_SECONDS, help="Request timeout in seconds (default: 10)")
    add_collection_arguments(parser)
    args = parser.parse_args()

    query = " ".join(args.query)
    num = min(args.num, MAX_RESULTS)

    try:
        if args.collection == "web":
            if args.mode or args.search_type or any((args.language, args.location, args.verified is not None, args.profile_type, args.min_followers, args.max_followers, args.min_stars, args.repo_license, args.include_forks, args.include_archived, args.created_after, args.created_before, args.published_after, args.published_before)) or args.page != 1:
                raise ValueError("Collection-specific options require --collection instagram or --collection code_repos")
            results = fetch_results(query, num, args.region, args.timeout)
        else:
            if args.region:
                raise ValueError("--region is only supported with --collection web")
            results = fetch_collection(args.collection, query, num, args.timeout, collection_options(args))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print("No results found.", file=sys.stderr)
        sys.exit(1)

    for i, r in enumerate(results, 1):
        print(f"--- Result {i} ---")
        if args.collection == "web":
            print(f"Title: {r.get('title', '')}")
            print(f"Link: {r.get('url', '')}")
            print(f"Snippet: {r.get('snippet', '')}")
        else:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        print()


if __name__ == "__main__":
    main()
