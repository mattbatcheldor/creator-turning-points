# Creator Turning Points release audit

16 November 2026. Editions 01 and 02: 15 cases each, 30 total. The Index remains disabled. Built with python3 src/build.py and checked with python3 src/audit.py. All internal links, anchors, case counts, required fields, credited 800 by 450 WebP images and image fingerprints pass. No em or en dash characters occur in repository text.

All 15 Edition 02 thumbnails were visually inspected. Four screening selections use creator-owned YouTube channels. YouTube metadata availability is checked with oEmbed, separately from regional playback or embedding permission.

## External checks

105 distinct external URLs checked in this release. YouTube watch URLs were checked through oEmbed. 100 checks returned HTTP 200. The complete log is verification/urls.json. Bare Google Fonts preconnect origins are connection hints, not reader destinations; they can return errors while the actual font stylesheet works.

## Failed or blocked reader URLs

- https://www.charlotteobserver.com/charlottefive/c5-food-drink/article249182880.html : HTTP Error 503: Service Unavailable
- https://www.foodnetwork.com/fn-dish/news/instacart-sales-increase-emily-mariko-salmon-bowl-tiktok : HTTP Error 404: Not Found
- https://www.thebookseller.com/news/pinch-packs-punch-slimming-cookbook-breaks-scales-become-fastest-selling-non-fiction-title-all : HTTP Error 429: Too Many Requests

Food Network’s article was readable through web retrieval and supplied the Instacart attribution, but that does not turn a failed direct GET into a pass. The Bookseller’s launch figure was corroborated in The Irish Times and on its searchable article. No failed endpoint is marked checked successfully.

## Limits

No controlled estimate of creator sales lift was established. Self-reported sales, platform-limited data and company-wide totals are labelled in the cases. Substituted and later media, location limits, regional playback and any browser checks not performed are listed in NOT_VERIFIED.md.
