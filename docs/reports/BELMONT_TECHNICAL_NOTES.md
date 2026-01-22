# City of Belmont Scraper Technical Notes

**Date:** 2026-01-21
**Status:** FIXED
**Scraper:** `BelmontScraper` (in `core/scrapers/wa_custom.py`)

## The Problem
The City of Belmont website (`https://www.belmont.wa.gov.au/discover/what-s-happening/latest-news`) uses Client-Side Rendering (CSR). 
- The initial HTML response contains no news items.
- A JavaScript function `ITGAsyncSearch` (from `itg.search.js`) fetches content dynamically.
- Previous attempts yielded 404s or stale data (2020) because the default API behavior is to sort by `menuitemname` or relevance, not date, and the "future dated" items were hidden without specific parameters.

## The Solution
We reverse-engineered the internal API endpoint used by the frontend.

### Endpoint
`GET https://www.belmont.wa.gov.au/api/search/search`

### Critical Parameters
The API is extremely sensitive to the following parameters. Missing any of them (especially `userguid`) can result in errors or incorrect data.

| Parameter | Value | Notes |
| :--- | :--- | :--- |
| `sort` | `DATE_DSC` | **Crucial**. Without this, you get data from 2020. |
| `searchindex` | `BelmontNewsIndex` | Selects the correct search index. |
| `transformationname` | `Belmont.Transformations.NewsSearchResults` | Formats response as HTML. |
| `userguid` | `3758B9B5-045C-4B7D-B020-80F9B068D990` | Acts as an auth/session token for the search context. |
| `pagenum` | `1` | Pagination. |
| `pagesize` | `12` | Batch size. |

### Response Format
The API returns a JSON object. The actual HTML for the news cards is inside the `PartialHTML` key.

```json
{
  "Count": 135,
  "PartialHTML": "<div class=\"news-item\">...</div>",
  "DidYouMean": ""
}
```

### Parsing Logic
We use `BeautifulSoup` to parse `PartialHTML`.
- **Title**: Inside `.title` (sometimes nested in `<strong>`).
- **Date**: Inside `.release-date`. **Note**: The API currently returns future dates (e.g., Jan 2026) for recent items. This might be a timezone or CMS configuration quirk, but the data is the "latest".
- **Link**: In `a` tag or `.read-more`. needs to be prepended with `https://www.belmont.wa.gov.au`.

## Reusability
This pattern (Kentico/Jadu style search API) might be present in other "Alyka" built sites in WA (e.g., Swan, Rockingham). If those sites fail with `AlykaScraper`, check for `/api/search/search` or similar endpoints and look for `ITGAsyncSearch` in the source code.
