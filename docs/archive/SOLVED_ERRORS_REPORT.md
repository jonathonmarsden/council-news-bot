# Resolved Errors Report (25 Jan 2026)

## 2026-01-25 Updates

### Barcaldine Regional Council (QLD)
*   **Error**: `Scraped 0 items`.
*   **Cause**: The scraper was looking for generic `<div class="news-item">` selectors which did not exist on their OpenCities CMS.
*   **Solution**: Updated `states/qld/councils.json` to use correct `item_selector: .list-item-container` and `title_selector: .list-item-title`.
*   **Result**: 9 articles found.

### City of Armadale (WA)
*   **Error**: `TimeoutError` in `browser_scraper` / 0 items in `curl_scraper`.
*   **Cause**: Heavy Next.js "App Router" application. The page is an empty shell that hydrates via Client-Side Rendering (CSR). Standard tools timed out or saw skeletons.
*   **Solution**:
    1.  Reverse-engineered the public API: `https://api.my.armadale.wa.gov.au/content/mediaRelease`.
    2.  Developed `JsonScraper` module.
    3.  Updated config to bypass HTML entirely and fetch 100+ items instantly via JSON.
*   **Result**: 31 articles found instantly. 

### Infrastructure: JSON Scraper
*   **Added**: `core/scrapers/json.py`.
*   **Purpose**: To handle Headless CMS sites (Next.js, Nuxt, Contentful) that are resistant to standard HTML scraping but expose public APIs.
*   **Documentation**: Updated `CONTRIBUTING.md` and `PROJECT_LEARNINGS_2026.md`.

## Previous Fixes (23 Jan 2026)

### 404 & Connection Errors
| State | Council | Issue | Resolution |
|-------|---------|-------|------------|
| NSW | Hay Shire Council | 404 (Old URL) | Updated URL to `https://www.hay.nsw.gov.au/Inside-Hay-Shire-Council/News-Council-Updates` & Fixed Selectors. |
| NSW | Gunnedah Shire Council | 404 (Report Outdated) | Verified Config `https://www.gunnedah.nsw.gov.au/index.php/council/keep-in-touch/latest-news-media`. Works. |
| NSW | MidCoast Council | SSL Error (TLSv1) | Verified Config uses `curl_scraper`. Works locally. |
| QLD | Torres Strait Island | SSL Error (TLSv1) | Verified Config uses `curl_scraper`. Works locally. |
| VIC | Buloke Shire Council | Read Timeout | Verified Config uses `curl_scraper`. Works locally. |

### WAF / "No Items" Fixes
Many councils in the "WAF" list were actually suffering from incorrect URLs (Landing Page vs Listing).

| State | Council | Issue | Resolution |
|-------|---------|-------|------------|
| VIC | Hindmarsh Shire | URL was Landing Page | Updated to `https://www.hindmarsh.vic.gov.au/Council/News-and-Media/Latest-News`. |
| VIC | Whittlesea City | URL was Landing Page | Updated to `https://www.whittlesea.vic.gov.au/About-us/News/Latest-news` and removed invalid whitespace. |
| NSW | Burwood Council | WAF (False Positive?) | Verified `curl_scraper` works correctly. |
| NSW | Hawkesbury Council | WAF (False Positive?) | Verified `curl_scraper` works correctly. |
| VIC | Moorabool Shire | WAF (False Positive?) | Verified `curl_scraper` works correctly. |

## 2026-01-26 Updates

### Bluesky API Error (URI Validation)
*   **Error**: `XrpcError(error='InvalidRequest', message='Invalid app.bsky.feed.post record: Record/facets/0/features/0/uri must be a uri')`
*   **Cause**: Pending articles from various councils contained non-ASCII characters in their URLs (e.g., Unicode curly quotes `’` or en-dashes `–`). The `BlueSkyPoster` was submitting these containing raw Unicode, which the Bluesky API rejected.
*   **Examples**: `Launch-of-PRACC’s-2026-performance-season`.
*   **Solution**: Updated `core/poster.py` (`_add_tracking_params`) to strictly ASCII-encode the URL path using `urllib.parse.quote(path, safe='/')` before submission.
*   **Result**: Articles with complex URLs are now posting successfully.

## 2026-01-28 Updates

### System-Wide Scraper Outage (Proxy Backout)
*   **Error**: All scrapers failing silently or with connectivity errors. Bot posted nothing for 4+ hours.
*   **Cause**: The rotating proxy service (Webshare) subscription had expired or was blocked, returning 000/502 errors to `curl`.
*   **Diagnosis**:
    *   Health checks showed VPS up but no new articles.
    *   Manual `curl` from VPS to proxy confirmed 000 response.
    *   User verified Webshare account status.
*   **Solution**:
    1.  User restored Webshare proxy service.
    2.  Verified connectivity via `scripts/deployment/trigger_manual_run.py` (see DEPLOYMENT.md).
    3.  Manually triggered a catch-up run for WA state, which processed 31 missing articles.
*   **Result**: System resumed regular posting.
