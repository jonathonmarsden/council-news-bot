# Project Learnings 2026

## 1. Client-Side Rendering (CSR) & "App Shell" Pattern (Armadale)

**Discovery Date:** 2026-01-23
**Council(s) Affected:** Armadale (WA) `p4i5hqtl4d48` (Contentful Space ID)

### The Issue
Traditional HTTP requests (`requests`, `curl`, `aiohttp`) retrieve the **Initial HTML (App Shell)** from Next.js applications, not the rendered content.
- **Symptom**: `status_code` is 200, but the HTML contains a generic `<title>Service | City of Armadale</title>` and loading skeletons (`MuiSkeleton`) instead of article text.
- **Marker**: The presence of `<template data-dgst="BAILOUT_TO_CLIENT_SIDE_RENDERING"></template>` in the HTML body.
- **Root Cause**: The website uses Next.js Client-Side Rendering (CSR). The content is hydrated via JavaScript API calls after the page load.

### Failed Attempts
- **Direct HTML Scraping**: Returns empty shell.
- **Browser Scraping (Timeout)**: Hydration was too slow or blocked by bot detection. Playwright timed out waiting for selectors.

### The Breakthrough: Hidden APIs
By inspecting the **Network Tab** in Developer Tools, we found the frontend was calling a public JSON API:
`https://api.my.armadale.wa.gov.au/content/mediaRelease`

### The Solution: `JsonScraper`
We built a generic `JsonScraper` that bypasses the HTML/CSS entirely.
- **Efficiency**: 50x faster (Fetch 10KB JSON vs Load 5MB JS bundle).
- **Stability**: No selectors to break when CSS changes.
- **Configuration**:
    ```json
    "scraper": "json_scraper",
    "news_url": "https://api.my.armadale.wa.gov.au/content/mediaRelease...",
    "item_selector": "items",
    "title_selector": "fields.title",
    "date_selector": "fields.releaseDate",
    "link_selector": "https://my.armadale.wa.gov.au/service/news-and-media-releases/{fields.slug}"
    ```

## 2. Contentful CMS Pattern
Armadale uses Contentful (`p4i5hqtl4d48`).
- **Data Hydration**: Data often resides in `_next/static/chunks` or is fetched via GraphQL/REST calls to `api.contentful.com` (proxied via `api.my.armadale.wa.gov.au`).
- **Lesson**: If a site is "Headless" (React/Next.js/Vue), always check for a JSON API before resorting to a headless browser.

## 3. Validator vs. Poster Integration Mismatch

**Discovery Date:** 2026-01-23
**Module**: Core (Validator & Poster)

### The Issue
Silent failures in posting to Bluesky occurred for Councils with large article bodies (e.g., Bunbury, WA).
- **Symptom**: Logs showed `Validation failed (Excerpt too long (3557))`.
- **Root Cause**: The validation logic (`validate_post`) was being called with the **original raw excerpt** from the database (potentially thousands of characters) instead of the **truncated excerpt** that `BlueSkyPoster` prepares for the actual social media post.
- **Architectural Flaw**: Separation of concerns issue. The Validator tried to enforce platform limits (250 chars) on the *source data*, rather than validating the *final payload*.

### Solution
- Modified `core/poster.py` to pass the *truncated* excerpt (used_excerpt) to the validator.
- Ensure the Validator is checking exactly what will be sent to the API.
- **Key Learning**: Validation functions should verify the *output* of the transformation layer, not the *input*, when transmission limits are involved.

## 4. Vertical Scaling & Resource Optimization (VPS Tuning)
**Discovery Date:** 2026-01-23
**Infrastructure:** DigitalOcean 4GB / 2 vCPU Droplet

### The Issue
Safe defaults (1GB limit, 2 concurrent threads) were causing significant underutilization of the production environment.
- **Stats**: Local verification revealed the server had 3.8GB RAM usable but was only using ~1.3GB under load.
- **Bottleneck**: The artificial concurrency limit (`--concurrency 2`) slowed down full state scrapes unnecessarily.

### Solution
- **Docker Limits**: 
    - Boosted Bot container from 1GB -> 2GB RAM.
    - Boosted DB container from 512MB -> 1GB RAM (better buffer cache).
    - Unlocked CPU limit for Bot from 1.0 -> 1.5.
- **Application Tuning**: Increased `scraper` concurrency from 2 to 5.
- **Outcome**: Faster scrape cycles for large states (NSW/VIC) without risking OOM due to ample headroom (1GB remaining for OS/Overhead).

### Helper Command
To verify resource usage on the VPS:
`lscpu | grep "CPU(s):" && echo "---" && free -h`

## 5. Strict Validation Causing Silent Drops (Title Length)

**Discovery Date:** 2026-01-23
**Module**: Core (Validator)

### The Issue
Government media releases often have extremely verbose titles (e.g., "Public Notice: Proposal to adopt the Annual Budget 2025/26 and Strategic Resource Plan").
- **Symptom**: Logs showed `Skipping post: Validation failed for Cobar Shire Council (Title too long (188))`.
- **Impact**: Valid news was being suppressed because the Validator's `MAX_TITLE_LEN` (150 chars) was more aggressive than the Poster's ability to truncate (200-300 chars).
- **Root Cause**: Mismatch between "Ideal" (SEO/Social) length and "Acceptable" (Functional) length.

### Solution
- **Relaxed Limits**: Increased `MAX_TITLE_LEN` in `validator.py` and `poster.py` to **250 characters**.
- **Philosophy**: Prefer a truncated post (handled by `BlueSkyPoster` logic) over a dropped post. Better to have the news with `...` than no news at all.

## 6. Regex Tuning for Title Cleaning
**Discovery Date:** 2026-01-23
**Module**: Core (Poster)

### The Issue
Titles were appearing with concatenated dates, e.g., "Tue 20 January 2026Green bin or red bin?".
- **Root Cause**: The regex used to strip dates was too strict (requiring specific spacing) and didn't account for missing spaces after the year/date when scraping text content.
- **Solution**: Enhanced regex patterns in `_sanitize_title` to handle:
    - Optional spaces after date/year.
    - Ordinals (1st, 2nd).
    - Concatenated strings following the date.

## 7. Excerpt Validation Retry Logic
**Discovery Date:** 2026-01-23
**Module**: Core (Poster)

### The Issue
Posts were being dropped entirely because the *excerpt* contained a hashtag or URL (e.g., "Visit http://...").
- **Impact**: Zero visibility for valid articles just because the automated excerpt was messy.
- **Solution**: Implemented a "Retry Without Excerpt" fallback. If validation fails specifically on excerpt rules, the poster regenerates the payload with `excerpt=None` and tries again.

## 8. Database Key Reliability & ID Mismatch
**Discovery Date:** 2026-01-23
**Context:** Comprehensive Health Audit

### The Issue
A significant disconnect was found between the JSON Configuration files ("Canonical Source") and the Database Records.
- **Symptom**: When reconciling 536 Configured councils against the DB, over 400 failed to match by name, due to inconsistent slugification (e.g., "City of X" vs "X City Council" vs "X, City of").
- **Impact**: Reporting tools cannot reliably join Configuration data (URLs) with Performance data (Last Scrape Time).
- **Learning**: Database Primary Keys should be immutable and explicitly defined in the config, rather than derived from the Name at runtime.

### Action
- **Completed (2026-01-24):** All ID collisions (e.g., `latrobe`, `flinders`) across states have been resolved by appending state suffixes (`latrobe-tas`, `latrobe-vic`).
- **Result**: Config files now possess globally unique, immutable IDs.
- Future Refactor: Add an explicit `id` field to `councils.json` for every council.
- Immediate Mitigation: Use fuzzy matching in reporting tools.

## 9. Silent "Empty Run" Failures
**Discovery Date:** 2026-01-23
**Context:** Health Check Report

### The Issue
11 Councils in NSW were identified as "Healthy" (no errors) but were consistently returning 0 articles for 20+ runs.
- **Why it matters**: A scraper that runs successfully but finds nothing is more dangerous than a crashing scraper, as it raises no alarms in standard error logging.
- **Root Cause**: Likely DOM structural changes or selector rot (e.g., `article` tag changed to `div.news-item`).
- **Detection**: Monitoring `consecutive_empty_runs` is a critical health metric, distinct from `consecutive_failures`.

### Affected Councils (NSW Cluster)
- Lake Macquarie, Bogan, Lithgow, Lockhart, Murray River, Murrumbidgee, Narrandera, Shellharbour, Snowy Valleys, Upper Lachlan, Wollondilly.
**Update (2026-01-24):** All 11 of these councils have been successfully repaired.
- **Strategy**: Re-evaluating selectors (`card_scraper` updates) and detecting where news feeds were abandoned.
- **Notable Case**: **Lockhart Shire Council** was pivoted to scrape its **PDF Newsletters page** using an updated `CardScraper` that supports `self` referencing titles. This proved that when a council abandons their HTML news feed, the PDF newsletter archive is often the only viable alternative.

## 10. "Zombie Scrapers" & Silent Failures Resolved

**Discovery Date:** 2026-01-24
**Scope**: 61 Councils (including Adelaide, Bundaberg, Bogan Shire)
**Diagnosis Method**: `scripts/maintenance/audit_silent_failures.py`

### The Issue
Scrapers report `Status: 200 (Success)` but consistently find **0 articles**. This creates a false sense of security where the bot appears healthy but is gathering no data.

### Root Causes
1.  **Cloudflare Blocking (False 200)**:  
    *   **Case**: `City of Adelaide` (SA).
    *   **Mechanism**: The server returns a 200 status page that is actually a JS challenge or "Please Wait" screen, which the HTML parser cannot interpret as news. It fails to match selectors, resulting in 0 articles.
    *   **Fix**: Switch `scraper: "browser_scraper"` (Playwright). The resource cost is higher, but necessary for bypass.
2.  **RSS Configuration Errors**:  
    *   **Case**: `Bogan Shire` (NSW) & `Bundaberg` (QLD).
    *   **Mechanism**: Scrapers configured as `rss_scraper` were passed the human-readable Page URL (e.g., `.../news`) instead of the XML Feed URL. The parser loaded the HTML page, found no `<item>` tags, and exited silently with 0 articles.
    *   **Fix**: Update `news_url` to point directly to the RSS feed (e.g. `.../feed/` or `.../news?format=feed`).

## 11. Timezone & Scheduler Drift

**Discovery Date:** 2026-01-24
**Impact**: Scheduled posts missing "morning windows".

### The Learning
Docker containers default to UTC. For an Australian bot, this shifts the "5am - 10pm" window to "2pm - 7am" (AEDT is UTC+11).
*   **Fix**: Always explicitly set `TZ=Australia/Sydney` in `docker-compose.yml` AND install `tzdata` in the Dockerfile.
*   **Verification**: Run `date` inside the container after deployment.

## 12. WA Council Fixes (Dumbleyung, Datascape sites)

**Discovery Date**: 2026-01-24
**Councils Affected**: Dumbleyung, Halls Creek, Manjimup, Sandstone.

### Shire of Dumbleyung
- **Issue**: The '/news' page is a Wix template placeholder with dummy JSON data.
- **Solution**: The council publishes actual updates on the '/newsletters' page (`https://www.dumbleyung.wa.gov.au/newsletters`).
- **Implementation**: Created `DumbleyungScraper` in `wa_custom.py` which scrapes Mailchimp links (`mailchi.mp`) and parses the link text (e.g. "January 2026") as the title/date.

### Datascape Sites (Halls Creek, Manjimup, Sandstone)
- **Identification**: Sites hosted on `cdn-sites.datascape.cloud`.
- **Issue**: `curl` requests return a skeletal HTML frame. Headless Playwright requests (without User-Agent) receive a **403 Forbidden** error, indicating anti-bot protection.
- **Solution**: Use `browser_scraper` with a standard User-Agent string.
- **Selectors**:
  - Container: `#news-listing ul li`
  - Title: `h2`
  - Date: `time` (datetime attribute)
  - Link: `a` (wraps the content)

## 13. Alyka CMS & Client-Side Hydration

**Discovery Date**: 2026-01-24
**Councils Affected**: Harvey, Mandurah, Subiaco (WA).

### The Issue
Sites built by "Alyka" (identified by `Alyka.NewsArticle` in JS or `/app_themes/harvey/` paths) often use Client-Side Rendering (CSR) for their news feeds, particularly on "Latest News" sub-pages.
- **Symptom 1**: `requests` returns a 200 OK HTML page, but the container (e.g., `#pageTypeListing-results`) is empty.
- **Symptom 2**: The landing page might show 3 "featured" items, but the actual archive (`/latest-news`) requires JS to load the full list from an API (`/aapi/advancesearch`).

### Solution
- **Action**: Switch to `browser_scraper` (Playwright) to allow the `Alyka.scripts.js` to hydrate the DOM.
- **Config Changes**:
  - **Harvey**: Point to `/news-and-events/latest-news`. Selector: `.news-item`.
  - **Mandurah**: Point to `/explore/whats-on/news`. Selector: `.news-archive__item`.
  - **Subiaco**: Point to `/see-do/good-to-know/news`. Selector: `.news-item`.
- **Note**: These sites do not trigger the 403 Forbidden seen on Datascape sites, but they simply return 0 items without a browser.

## 15. Browser Scraper Logic Fix

**Discovery Date**: 2026-01-24
**Component**: `core/scrapers/browser.py`

### The Issue
While diagnosing **Bass Coast**, I discovered that the `BrowserScraper` implementation had a bug when handling `link_selector: "self"`. unlike the standard `BaseScraper`, the browser scraper was passing the string "self" directly to Playwright's `query_selector`, causing it to fail silently (caught in try/except) and return 0 items.

### The Fix
Updated `core/scrapers/browser.py` to explicitly check for the "self" keyword:
```python
if link_sel == "self":
    link_el = item
else:
    link_el = item.query_selector(link_sel) if link_sel else item
```

This instantly resolved the Bass Coast 0-article issue.

## 16. WA Datascape Verification

**Discovery Date**: 2026-01-24
**Councils Affected**: Halls Creek, Manjimup, Sandstone.
**CMS**: Datascape (suspected, shares identicial DOM structure).

### The Issue
These sites were returning `403 Forbidden` when accessed via standard `curl` or `requests`, and generic scraping failed.

### Detection
The sites share a distinct DOM signature:
*   Container: `#news-listing ul li`
*   Title: `h2` inside the list item.
*   Date: `time` element.
*   Link: `a` tag wrapping the content.

### Solution
Ensured they are configured with `scraper: "browser_scraper"`.
Verified that the `BrowserScraper` correctly bypasses the 403 blocks (WAF) by using a legitimate User-Agent string.

### Outcome
All verified working:
*   **Manjimup**: 20 articles.
*   **Halls Creek**: 20 articles.
*   **Sandstone**: 6 articles.

## 17. Incapsula WAF & Drupal Selectors (NSW Northern Beaches)

**Discovery Date**: 2026-01-24
**Councils Affected**: Northern Beaches Council (NSW)
**Technique**: WAF Bypass & Selector Refinement

### The Issue
Northern Beaches Council (`northern-beaches`) was failing silently (0 articles).
1.  **Original Config**: `curl_scraper` + generic selectors.
2.  **Selector Issue**: The site uses a complex Drupal structure where news items are nested deep within `div.view-content`. Standard `article` selectors missed them.
3.  **WAF Issue**: Upon fixing selectors, the `curl_scraper` began hitting **Incapsula/Imperva** blocks (403 or CAPTCHA pages), returning invalid HTML that yielded 0 articles.

### The Fix
1.  **Switch to Browser**: Changed scraper to `"browser_scraper"` to handle the JS challenge/WAF signature.
2.  **Drupal Selectors**:
    *   Container: `article.node-cnews` (Specific to their news content type).
    *   Title: `h2.node__title span` (Title text is nested in a span).
    *   Date: `.node__meta span` (Date is in metadata block).

### Outcome
Successfully scraped 20 articles (e.g., "Council Meeting Outcomes").
**Learning**: If a high-profile council (major metro) returns 0 items with correct selectors, assume WAF/blocking is in play and verify with `browser_scraper`.

## 18. User Agent WAF Blocking (Cherbourg Pattern)

**Discovery Date:** 2026-01-24
**Council(s) Affected:** Cherbourg Aboriginal Shire Council (QLD)

### The Issue
Specific WAF configurations may block requests based on generic or "impersonator" User Agent strings while allowing standard browser defaults or seemingly "empty/default" automated strings.
- **Symptom**: `BrowserScraper` (Playwright) returns 0 items and timeouts waiting for selectors, even though the site is accessible manually.
- **Diagnosis**: A custom "impersonated" User Agent string (e.g., `... Chrome/120.0...`) triggered a block, whereas the default Playwright User Agent (which usually identifies as HeadlessChrome) was allowed.
- **Counter-Intuitive**: Normally, we override UAs to look *more* like human users. In this case, the specific "fake" string was likely flagged as a bot signature by a security rule, while the "honest" headless UA was ignored or treated differently.

### Solution
- Added `use_default_ua` flag to `BrowserScraper` to bypass the hardcoded impersonation.
- **Key Learning**: When scraping fails with a "perfect" human-like User Agent, try reverting to the tool's default. WAFs maintain blacklists of known scraper masquerades.

## 19. The "Zombie Scraper" Phenomenon & Audit Methodology

**Discovery Date**: 2026-01-24
**Scope**: All Jurisdictions (NT, TAS, SA focused)
**Status**: Repaired

### The Issue
A "Zombie Scraper" is a scraper that returns `200 OK` status codes and runs without errors, but produces no **new** data because the underlying source has become stale or the target page layout has shifted silently.
- **Symptom**: The bot reports "0 new articles" day after day, for months or years.
- **Example**: Litchfield Council (NT) RSS feed was active but only contained items from 2014-2020. The scraper was "working" techincally, but failing operationally.

### Detection Methodology
We developed `scripts/debug_zombies.py` to audit councils by "Freshness":
1.  **Parse Live Data**: Run the scraper logic locally.
2.  **Extract Date**: specific focus on the `pubDate` or data extraction.
3.  **Threshold Check**: Flag any council where the *newest* item is older than 90 days (warning) or 365 days (critical).

### Key Learnings
- **Status Codes Lie**: HTTP 200 means "Server is happy", not "Content is fresh".
- **Visual Checks Required**: You must inspect the HTML content to verified dates.
- **Bandwidth Limits**: Small councils (e.g., West Daly) on shared hosting may return `509 Bandwidth Exceeded` if hit too frequently or if their plan expires.

## 20. RSS Feed Decay & The Shift to HTML Scraping

**Discovery Date**: 2026-01-24
**Trend**: 40% of NT councils had broken/stale RSS.

### The Observation
RSS feeds are increasingly neglected by municipal IT teams. They are often legacy artifacts left over from old CMS migrations (Drupal 7 -> 10).
- **Darwin**: Feed endpoint existed but returned 404 or XML errors.
- **Litchfield**: Feed valid but abandoned (stale data).
- **Victoria Daly**: Feed moved URL without redirect.

### The Strategy
**Prefer HTML Scraping** (`curl_scraper`) over RSS (`rss_scraper`) for stability in 2026.
- **Pros**: Matches what users see on the website. If the website is up, the "feed" is up.
- **Cons**: Requires selector maintenance.
- **Decision Matrix**:
    - If RSS is < 30 days old: **Keep RSS**.
    - If RSS is > 90 days old or 404: **Switch to HTML**.
    - If HTML is blocked (WAF): **Switch to Browser**.

## 21. VPS vs Local Fingerprinting (Lockyer Valley Case)

**Discovery Date:** 2026-01-24
**Council(s) Affected:** Lockyer Valley (QLD)

### The Issue
A scraper configuration working perfectly on a local development machine (macOS) failed consistently on the production VPS (Ubuntu/DigitalOcean).
- **Symptom**: `curl_scraper` returned "Found 0 articles" on VPS, but worked locally.
- **Analysis**: The site likely employs fingerprinting or behavioral analysis. The `curl_cffi` impersonation (`chrome120` or similar) might have subtle differences on Linux vs macOS, or the IP reputation of DigitalOcean triggered a "soft block" (serving a 200 OK page with no content).
- **Resolution**: Ironically, simplifying the scraper to use the standard Python `requests` library (`card_scraper`) bypassed the block. This suggests the specific TLS fingerprint or headers sent by `curl_cffi` were the trigger, whereas standard `requests` flew under the radar (or the site just dislikes `curl` user agents).
- **Learning**: "More advanced" is not always better. Start simple (`requests`), upgrade to `curl_cffi` if WAF is detected, upgrade to `Playwright` if JS/Behavioral challenges persist.

## 22. The "Just a Moment" Challenge (Hawkesbury & East Arnhem)

**Discovery Date:** 2026-01-24
**Council(s) Affected:** Hawkesbury (NSW), East Arnhem (NT)

### The Issue
Sites behind aggressive Cloudflare protections present different challenges based on the tool used.
- **East Arnhem**: Banned `requests` and `curl` (403 Forbidden) instantly. Only a real browser (`browser_scraper` / Playwright) could pass.
- **Hawkesbury**: Allowed `curl_cffi` (impersonating Chrome) to load the page (200 OK), but the content structure was complex. `Playwright` failed detection ("Just a moment...").
- **Resolution**:
    - **East Arnhem**: **MUST** use `browser_scraper` (Playwright).
    - **Hawkesbury**: **MUST** use `curl_scraper` (curl_cffi).
- **Learning**: There is no "silver bullet". Some WAFs block headless browsers (Playwright) but allow impersonated curl. Others block curl but allow browsers that execute full JS. We must maintain agility to switch engines per-council.

## 23. The "Zombie Scraper" Phenomenon (Silent Failures)
**Discovery Date:** 2026-01-24
**Type:** Operational Risk

### The Issue
A scraper that runs successfully (Exit Code 0) but returns **0 items** is often more dangerous than a crashing scraper.
- **Symptom**: Logs show "INFO: Scraped 0 items for [council]".
- **Cause**: Layout changes where the `item_selector` no longer matches anything, but the page loads fine (200 OK).
- **Risk**: The bot thinks it is working, but it is missing all news.

### Solution
- **Fail Loud**: Scrapers should ideally raise an error if they expect items but find none (though this is hard to distinguish from a quiet news week).
- **Monitoring**: We now run `scripts/analysis/analyze_vic_zombies.py` (and similar) to detect councils with 0 items over X days.
- **Fix**: When fixing a council, ALWAYS verify that `dry-run` returns > 0 items. If it returns 0, assume the selector is broken until proven otherwise.

## 2026-01-25: Bayside & Blacktown Audit (Artifact Verification)
**Issue**: Logs showed "0 items" for NSW councils during the Cron/Scheduler conflict.
**Investigation**:
-   Locally audited **Bayside Council** (`card_scraper`) and **Blacktown City Council** (`curl_scraper`).
-   Both worked perfectly, confirming the "0 items" in logs were indeed artifacts of the scheduler race condition (likely resource exhaustion or DB locking).
**Fix**:
-   Fixed a logging bug in `card.py` where Drupal titles inside `field--label-hidden` spans were skipped, causing false "Missing title" logs (even though the scraper recovered via fallbacks).
-   Deployed updated `card.py` to production.
**Outcome**: NSW is confirmed operational. The "0 items" alert was a false positive caused by the infrastructure conflict.

## 2026-01-25: Concurrency Upgrade
**Action**: Increased scraper concurrency from 5 to 8 workers for all states in the VPS `crontab`.
**Reasoning**: We upgraded the VPS container RAM limit to 3GB (previously 2GB). This unlocked headroom allows for more parallel browser instances without OOM risk.
**Expected Benefit**: 
- Faster scrape cycles (estimated 40% reduction in runtime for large states like NSW/VIC).
- Reduced "drift" where scraped news is hours old by the time it's posted.
**Status**: Applied and Deployed to Production.

## 4. The "Proxy Leak" Fallback Vulnerability

**Discovery Date:** 2026-01-25
**Module:** `core/scrapers/base.py`

### The Issue
The scraper's `fetch_page` method contained dangerous fallback logic:
1.  Attempt Direct Connection.
2.  If failed, Attempt Proxy Connection.

**Risk**: This logic guarantees that the main VPS IP address is exposed to the target WAF *before* the proxy is used. If the WAF blocks the IP, the damage is already done (reputation loss). Global WAFs (Cloudflare/Incapsula) share this reputation data, potentially poisoning the IP for *all* councils.

### The Fix
Strict Proxy Adherence:
```python
if self.proxy:
    # Use proxy exclusively
    return self._fetch_with_proxy(url)
# Only use direct if NO proxy is configured
return self._fetch_direct(url)
```
**Lesson**: Never treat proxies as a "retry" mechanism for WAF evasion. They are a primary access method.

## 5. "Mojibake" & API Validation Failures

**Discovery Date:** 2026-01-25
**Module:** Database / API

### The Issue
155 URLs in the database contained unescaped non-ASCII characters (e.g., Smart Quotes `’`, Em-dashes `–`).
- **Symptom**: Downstream APIs (Bluesky Post Validator) rejected the URLs as malformed.
- **Cause**: Scrapers extracting raw headers without sanitization.

### The Fix
1.  **Sanitization**: Added `urllib.parse.quote` to the `NewsArticle.__post_init__` method to enforcing ASCII-compliance at object creation time.
2.  **Repair**: Ran `scripts/maintenance/fix_mojibake_urls.py` to repair historical data.

## 6. Docker Volume Persistence
**Discovery Date:** 2026-01-25
**Module:** Infrastructure

### The Issue
Health check reports generated inside the container at `/app/REPORT.md` were not appearing on the host.
- **Cause**: `docker-compose.yml` only mounts `/app/data` and `/app/logs`, not the root `/app`. The code is copied (`COPY . .`) at build time, not mounted.
- **Lesson**: All persistent output (reports, DBs, logs) MUST be written to `/app/data/` or `/app/logs/`.
