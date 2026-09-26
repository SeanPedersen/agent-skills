"""Scraper for kleinanzeigen.de search results using plain HTTP with a Chrome TLS fingerprint."""

from kleinanzeigen.client import KleinanzeigenClient
from kleinanzeigen.models import Listing, ListingDetail

__all__ = ["KleinanzeigenClient", "Listing", "ListingDetail"]
