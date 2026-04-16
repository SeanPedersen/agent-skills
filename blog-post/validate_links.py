#!/usr/bin/env python3
"""Validate that URLs exist and page content matches the expected anchor text."""
# /// script
# requires-python = ">=3.10"
# dependencies = ["niquests", "readability-lxml", "lxml[html_clean]"]
# ///

import json
import sys

import niquests
from readability import Document


def validate_link(url: str, anchor_text: str) -> dict:
    """Check that a URL is reachable and its content relates to the anchor text."""
    result = {"url": url, "anchor": anchor_text, "exists": False, "relevant": False, "error": None}

    try:
        resp = niquests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
            timeout=10,
            allow_redirects=True,
        )
        if resp.status_code >= 400:
            result["error"] = f"HTTP {resp.status_code}"
            return result
        result["exists"] = True

        doc = Document(resp.text)
        title = (doc.title() or "").lower()
        from lxml import html as lxml_html

        tree = lxml_html.fromstring(doc.summary())
        body_text = tree.text_content().lower()[:5000]

        anchor_words = [w for w in anchor_text.lower().split() if len(w) > 3]
        if not anchor_words:
            result["relevant"] = True
            return result

        matches = sum(1 for w in anchor_words if w in title or w in body_text)
        result["relevant"] = matches >= len(anchor_words) * 0.4

    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_links.py '<json_array>'", file=sys.stderr)
        print('  JSON format: [{"url": "https://...", "anchor": "link text"}, ...]', file=sys.stderr)
        sys.exit(1)

    try:
        links = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    all_valid = True
    for link in links:
        result = validate_link(link["url"], link.get("anchor", ""))
        status = "OK" if result["exists"] and result["relevant"] else "FAIL"
        if status == "FAIL":
            all_valid = False
        print(f"[{status}] {result['url']}")
        if not result["exists"]:
            print(f"  -> Not reachable: {result['error'] or 'unknown'}")
        elif not result["relevant"]:
            print(f"  -> Content does not match anchor: \"{result['anchor']}\"")

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
