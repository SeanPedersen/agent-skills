#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "primp>=2.0.1",
#     "selectolax>=0.4.12,<1",
# ]
# ///
"""CLI: search kleinanzeigen.de page by page, or view one listing in full (--detail), as a table or JSON."""

import argparse
import json
from dataclasses import asdict

from kleinanzeigen import KleinanzeigenClient
from kleinanzeigen.models import ListingDetail, SearchPage

DEFAULT_LOCATION = ""
TITLE_WIDTH = 60


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queries", nargs="*", help="one or more search keywords")
    parser.add_argument("--detail", metavar="URL", help="show one listing in full (text, all images, attributes, seller profile) instead of searching")
    parser.add_argument("--location", default=DEFAULT_LOCATION)
    parser.add_argument("--page", type=int, default=1, help="result page to start at (1-based)")
    parser.add_argument("--pages", type=int, default=1, help="number of pages to fetch from --page on")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = parser.parse_args()
    if not args.detail and not args.queries:
        parser.error("provide search keywords or --detail URL")
    return args


def page_to_dict(query: str, page: SearchPage) -> dict:
    return {
        "query": query,
        "page": page.page,
        "result_summary": page.result_summary,
        "has_next": page.has_next,
        "listings": [asdict(listing) for listing in page.listings],
    }


def print_page_table(query: str, location: str, page: SearchPage) -> None:
    print(f"\n== {query!r} in {location}, page {page.page}: {page.result_summary or 'no results'} (has_next={page.has_next}) ==")
    for l in page.listings:
        print(f"{l.posted:>15} | {l.price:>12} | {l.title[:TITLE_WIDTH]:<{TITLE_WIDTH}} | {l.location} | {l.url}")


def print_detail(detail: ListingDetail) -> None:
    for field, value in asdict(detail).items():
        print(f"{field}: {value}")


def show_detail(client: KleinanzeigenClient, url: str, as_json: bool) -> None:
    detail = client.get_listing(url)
    if as_json:
        print(json.dumps(asdict(detail), ensure_ascii=False, indent=2))
        return
    print_detail(detail)


def main() -> None:
    args = parse_args()
    client = KleinanzeigenClient()
    if args.detail:
        show_detail(client, args.detail, args.json)
        return

    results = [
        (query, page)
        for query in args.queries
        for page in client.search_pages(query, args.location, args.page, args.pages)
    ]

    if args.json:
        print(json.dumps([page_to_dict(q, p) for q, p in results], ensure_ascii=False, indent=2))
        return

    for query, page in results:
        print_page_table(query, args.location, page)


if __name__ == "__main__":
    main()
