"""Data models for kleinanzeigen.de search results."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Listing:
    ad_id: str
    title: str
    url: str
    price: str
    location: str
    posted: str
    description: str
    image_url: str | None


@dataclass(frozen=True, slots=True)
class SearchPage:
    page: int
    listings: list[Listing]
    result_summary: str | None
    next_path: str | None

    @property
    def has_next(self) -> bool:
        return self.next_path is not None


@dataclass(frozen=True, slots=True)
class ListingDetail:
    ad_id: str
    url: str
    title: str
    price: str
    location: str
    posted: str
    description: str
    image_urls: list[str]
    attributes: dict[str, str]
    shipping: bool
    seller_id: str | None
    seller_name: str
    seller_type: str
    seller_active_since: str | None
    seller_rating: str | None
    seller_ads_online: str | None
    seller_profile_url: str | None
