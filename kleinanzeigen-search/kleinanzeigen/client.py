"""HTTP client for kleinanzeigen.de search.

primp impersonates Chrome's TLS/HTTP2 fingerprint; results are server-rendered,
so no JS runtime is needed. The search form endpoint redirects to the canonical
result URL (e.g. /s-hamburg/verschenken/k0l9409); page N lives at
/s-hamburg/seite:N/verschenken/k0l9409. Out-of-range pages silently redirect to
another page, so the landed page number is checked against the requested one.
"""

import re
import time
from collections.abc import Iterator

import primp

from kleinanzeigen.models import Listing, ListingDetail, SearchPage
from kleinanzeigen.parser import BASE_URL, parse_listing_detail, parse_search_page

SEARCH_FORM_PATH = "/s-suchanfrage.html"
IMPERSONATE_BROWSER = "chrome_146"
IMPERSONATE_OS = "macos"
REQUEST_TIMEOUT_SECONDS = 20
PAGE_DELAY_SECONDS = 1.5
HTTP_OK = 200
FIRST_PAGE = 1
PAGE_SEGMENT_PATTERN = re.compile(r"/seite:(\d+)")
# Canonical path: /s-<location>/<keywords>/<id>; the page segment goes after the location.
LOCATION_SEGMENT_PATTERN = re.compile(r"^(/s-[^/]+)(/)")


class KleinanzeigenError(RuntimeError):
    pass


def page_number_of(url: str) -> int:
    match = PAGE_SEGMENT_PATTERN.search(url)
    return int(match.group(1)) if match else FIRST_PAGE


def paginated_url(canonical_url: str, page: int) -> str:
    path = canonical_url.removeprefix(BASE_URL)
    path = PAGE_SEGMENT_PATTERN.sub("", path)
    return f"{BASE_URL}{LOCATION_SEGMENT_PATTERN.sub(rf'\1/seite:{page}\2', path, count=1)}"


class KleinanzeigenClient:
    def __init__(self, page_delay_seconds: float = PAGE_DELAY_SECONDS) -> None:
        self._page_delay_seconds = page_delay_seconds
        self._http = primp.Client(
            impersonate=IMPERSONATE_BROWSER,
            impersonate_os=IMPERSONATE_OS,
            follow_redirects=True,
            cookie_store=True,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

    def _get(self, url: str, params: dict[str, str] | None = None) -> primp.Response:
        response = self._http.get(url, params=params)
        if response.status_code != HTTP_OK:
            raise KleinanzeigenError(f"GET {response.url} -> HTTP {response.status_code}")
        return response

    def _fetch_page(self, url: str, page: int) -> SearchPage:
        response = self._get(url)
        if page_number_of(response.url) != page:
            return SearchPage(page=page, listings=[], result_summary=None, next_path=None)
        return parse_search_page(response.text, page)

    def search_pages(
        self, keywords: str, location: str, start_page: int = FIRST_PAGE, max_pages: int = 1
    ) -> Iterator[SearchPage]:
        first = self._get(
            f"{BASE_URL}{SEARCH_FORM_PATH}",
            params={"keywords": keywords, "locationStr": location},
        )
        if start_page == FIRST_PAGE:
            page = parse_search_page(first.text, FIRST_PAGE)
        else:
            time.sleep(self._page_delay_seconds)
            page = self._fetch_page(paginated_url(first.url, start_page), start_page)
        yield page

        for _ in range(max_pages - 1):
            if not page.next_path:
                return
            time.sleep(self._page_delay_seconds)
            page = self._fetch_page(f"{BASE_URL}{page.next_path}", page.page + 1)
            yield page

    def search(
        self, keywords: str, location: str, start_page: int = FIRST_PAGE, max_pages: int = 1
    ) -> list[Listing]:
        return [
            listing
            for page in self.search_pages(keywords, location, start_page, max_pages)
            for listing in page.listings
        ]

    def get_listing(self, url: str) -> ListingDetail:
        response = self._get(url)
        return parse_listing_detail(response.text, str(response.url))
