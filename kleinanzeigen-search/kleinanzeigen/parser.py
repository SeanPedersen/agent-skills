"""Pure HTML parsing of kleinanzeigen.de search result pages.

Only ads in `#srchrslt-adtable` are returned; `#srchrslt-adtable-altads` holds
suggestions from outside the requested location and is skipped on purpose.
"""

import json
import re

from selectolax.parser import HTMLParser, Node

from kleinanzeigen.models import Listing, ListingDetail, SearchPage

BASE_URL = "https://www.kleinanzeigen.de"
SELLER_ID_PATTERN = re.compile(r"sellerId: [\"`'](\d+)")
SHIPPING_PATTERN = re.compile(r'"Versand":"(\w+)"')
ACTIVE_SINCE_PATTERN = re.compile(r"Aktiv seit (\S+)")
ADS_ONLINE_PATTERN = re.compile(r"\d+ Anzeigen online")
SHIPPING_OFFERED = "ja"
RESULT_SUMMARY_PATTERN = re.compile(r"[\d.]+ - [\d.]+ von [\d.]+ Ergebnissen[^<]*")


def _text(node: Node | None) -> str:
    return node.text(strip=True) if node else ""


def _multiline_text(node: Node | None) -> str:
    return node.text(strip=True, separator="\n") if node else ""


def _icon_label(article: Node, icon: str) -> str:
    return _text(article.css_first(f'svg[data-title="{icon}"] + span'))


def _json_ld(article: Node) -> dict:
    script = article.css_first('script[type="application/ld+json"]')
    if not script:
        return {}
    try:
        return json.loads(script.text())
    except json.JSONDecodeError:
        return {}


def parse_listing(article: Node) -> Listing:
    href = article.attributes.get("data-href") or ""
    metadata = _json_ld(article)
    return Listing(
        ad_id=article.attributes.get("data-adid") or "",
        title=_text(article.css_first("h3 a")) or metadata.get("title", ""),
        url=f"{BASE_URL}{href}",
        # The first <p> is the current price; a second one is the struck-through old price.
        price=_text(article.css_first("h3 ~ div p")),
        location=_icon_label(article, "locationOutline"),
        posted=_icon_label(article, "calendarOutline"),
        description=metadata.get("description") or _text(article.css_first("h3 + p")),
        image_url=metadata.get("contentUrl"),
    )


def parse_search_page(html: str, page: int) -> SearchPage:
    doc = HTMLParser(html)
    summary = RESULT_SUMMARY_PATTERN.search(html)
    # Usually <a href>, but near the last page the site renders a <span data-url> instead.
    next_link = doc.css_first('[title="Nächste"]')
    return SearchPage(
        page=page,
        listings=[parse_listing(a) for a in doc.css("#srchrslt-adtable article[data-adid]")],
        result_summary=summary.group(0).strip() if summary else None,
        next_path=(next_link.attributes.get("href") or next_link.attributes.get("data-url")) if next_link else None,
    )


def _first_match(pattern: re.Pattern[str], text: str, group: int = 0) -> str | None:
    match = pattern.search(text)
    return match.group(group) if match else None


def _attributes(doc: HTMLParser) -> dict[str, str]:
    attributes = {}
    for item in doc.css("#viewad-details li"):
        value_node = item.css_first(".addetailslist--detail--value")
        value = _text(value_node)
        # The label is a bare text node before the value <span>.
        label = item.text(strip=True).removesuffix(value).strip() if value_node else ""
        if label and value:
            attributes[label] = value
    return attributes


def parse_listing_detail(html: str, url: str) -> ListingDetail:
    """Parse an ad page (/s-anzeige/...): full text, gallery, attributes and seller profile."""
    doc = HTMLParser(html)
    contact = doc.css_first("#viewad-contact")
    contact_text = contact.text(strip=True, separator=" ") if contact else ""
    profile_link = doc.css_first('#viewad-contact a[href*="userId"]')
    return ListingDetail(
        ad_id=_first_match(re.compile(r"adId:\s*'(\d+)'"), html, 1) or "",
        url=url,
        title=_text(doc.css_first("#viewad-title")),
        price=_text(doc.css_first("#viewad-price")),
        location=_text(doc.css_first("#viewad-locality")),
        posted=_text(doc.css_first("#viewad-extra-info")),
        description=_multiline_text(doc.css_first("#viewad-description-text")),
        image_urls=[img.attributes["src"] for img in doc.css(".galleryimage-element img") if img.attributes.get("src")],
        attributes=_attributes(doc),
        shipping=_first_match(SHIPPING_PATTERN, html, 1) == SHIPPING_OFFERED,
        seller_id=_first_match(SELLER_ID_PATTERN, html, 1),
        seller_name=_text(doc.css_first("#viewad-contact .text-body-regular-strong")),
        seller_type=_text(doc.css_first(".userprofile-vip-details-text")),
        seller_active_since=_first_match(ACTIVE_SINCE_PATTERN, contact_text, 1),
        seller_rating=_text(doc.css_first(".userbadges-profile-rating")) or None,
        seller_ads_online=_first_match(ADS_ONLINE_PATTERN, contact_text),
        seller_profile_url=f"{BASE_URL}{profile_link.attributes['href']}" if profile_link else None,
    )
