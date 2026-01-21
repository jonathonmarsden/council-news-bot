# Strategic Improvements & Streamlining Plan

## 1. Streamlining Scrapers
The disparity between VIC (100% coverage) and WA (16% coverage) highlights a key architectural lesson: **Generic Scrapers Win.**

### The "Catalyst" Lesson
WA has ~70-100 councils using the exact same "Catalyst" CMS template.
- **Old Strategy:** Individual config entries with CSS selectors for each. Fragile.
- **New Strategy:** `CatalystScraper` class. Robust.
- **Action:** audit SA and QLD for similar "clusters" of vendor templates and create dedicated Scraper classes for them immediately. Validated vendors include:
    - OpenCities (Used heavily in NSW/VIC)
    - Datascape (Used in NZ/some AU)
    - Squiz Matrix

## 2. Bluesky Feed Optimization
The current Bluesky feed risks becoming a "firehose" of irrelevant administrative data.

### Analysis of Feed
- **Volume:** Potential for 50-100 posts/day if all WA councils go live.
- **Relevance:** "Notice of Meeting" vs "New Park Opening".
- **Suggestion:** Implement an **AI Filter / Classification Step**.
    - Before posting, pass the headline/excerpt to a lightweight LLM (or regex filter).
    - **Discard:** "Meeting Minutes", "Public Notice", "Tender RFT-2026".
    - **Prioritize:** "Community", "Events", "Construction", "Health Alert".

## 3. Deployment & Monitoring
The high number of "Silent" councils (Configured but 0 data) indicates a lack of visibility into the *execution* of the bot.

- **Problem:** We didn't know WA was failing until we manually audited the DB.
- **Solution:** Add a `health_check.py` to the GitHub Actions workflow (or cron job).
    - If `active_councils < 50%` of `configured_councils`, send an alert (Discord/Email).
    - If `total_articles_scraped == 0` for 3 consecutive runs, alert.

## 4. Technical Debt Clean-up
- **Archives:** The `wa_custom.py` file is growing large.
- **Refactor:** Move `JoondalupScraper` and `PerthScraper` to their own files if they grow further.
- **Verification:** The "Snowflake" hardcoding in `update_snowflakes.py` is technical debt. These should be standard configuration options in `councils.json`.

## 5. Next Steps
1.  **Immediate:** Run the WA scraper in production mode to hydrate the 116 silent councils.
2.  **Short-term:** Archive the backlog of old articles to prevent Bluesky spam.
3.  **Medium-term:** Implement the regex-based "Boring Content Filter".
