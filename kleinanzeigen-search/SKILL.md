---
name: kleinanzeigen-search
description: Search kleinanzeigen.de listings (keywords + city) page by page, or view one listing in full (all images, full text, seller profile)
---

# Kleinanzeigen Search

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/); dependencies install on first run.

```bash
uv run {baseDir}/search.py "v100 32gb" --json                       # page 1, no location = all of Germany (default)
uv run {baseDir}/search.py verschenken --location berlin --json     # any city name
uv run {baseDir}/search.py verschenken --page 3 --pages 2 --json    # pages 3-4; multiple quoted queries allowed
uv run {baseDir}/search.py --detail <listing url> --json            # one listing in full
```

`--json` emits one object per fetched page:

```json
[{"query": "verschenken", "page": 3, "result_summary": "51 - 75 von 5.409 Ergebnissen …",
  "has_next": true, "listings": [{"ad_id", "title", "url", "price", "location", "posted", "description", "image_url"}]}]
```

`--detail` fetches one listing page (search results truncate the description and show a single thumbnail) and returns:

```json
{"ad_id", "url", "title", "price", "location", "posted", "description" /* full text */, "image_urls" /* full gallery */,
 "attributes" /* e.g. {"Zustand": "Sehr Gut"} */, "shipping" /* bool */, "seller_id", "seller_name",
 "seller_type" /* "Privater Nutzer" | commercial */, "seller_active_since", "seller_rating", "seller_ads_online",
 "seller_profile_url" /* private: s-bestandsliste.html?userId=…, business: /pro/<shop> */}
```

## Notes

- Use search to shortlist, then `--detail` on promising listings to inspect text, photos and seller before recommending.
- Paginate with `--page 1, 2, …` until `has_next` is false. 25 listings per page, max 50 pages: narrow the query instead of paging deep.
- `posted` is raw site text ("Heute, 01:18", "14.09.2026").
- Poll moderately to avoid rate limits.
- Always include the listing `url` when reporting listings.
- Flag shady listings for review (no Käuferschutz accepted by seller, suspicious pricing or incomplete  / bad reviewed seller profiles)
