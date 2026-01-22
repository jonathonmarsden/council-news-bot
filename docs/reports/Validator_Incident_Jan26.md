# Post-Incident Review: Validator Logic Failure (Jan 2026)

## 1. Incident Summary
**Date:** 2026-01-22  
**Issue:** The bot was running successfully (scraping content) but failing to post specific articles to BlueSky, reporting "Posted 0 articles" despite a growing backlog (200+ items).  
**Root Cause:** Overly strict validation logic in `core/validator.py` and `core/poster.py`.

## 2. Technical Findings

### A. The "Silent" Failure
The `BlueSkyPoster` class catches validation errors and prints them to `stdout`, but does not raise exceptions that would crash the script. Because the scheduler captures `stdout` but only logs specific summary lines, these validation errors were hidden in the verbose logs.

### B. Validation Constraints (The "Hidden" Rules)
1.  **Excerpt Length**: The validator was hardcoded to reject any excerpt > 120 characters (`IDEAL_EXCERPT_LEN`). Many scraper excerpts (especially from RSS feeds or meta descriptions) exceed this.
2.  **Facet Indexing**: The `atproto` library requires byte-based indexing for "facets" (links/hashtags). The validator was checking character-based indices against the text length. When UTF-8 characters (emojis, fancy quotes) were present, the byte length differed from the char length, causing the validator to falsely flag `Facet span invalid`.

### C. Rate Limiting Limits
The `scheduler.py` invokes `main.py` with `--limit 2` per state every 5 minutes.
- **Max Throughput**: 24 posts/hour per state.
- **Backlog Clearance**: With 200+ items in WA, it will take ~8.5 hours to clear the backlog, assuming 100% success rate.

## 3. Corrective Actions Taken
1.  **Patched `core/validator.py`**:
    - Increased `IDEAL_EXCERPT_LEN` to 250 chars.
    - Updated facet validation to use `len(text.encode('utf-8'))` for accurate boundary checks.
2.  **Deployed**: Hot-patched the container `council_news_bot` on the VPS.
3.  **Verified**: Manually triggered a post to WA, confirming success.

## 4. Recommendations
1.  **Loosen Scheduler Limits**: Increase `--limit` in `scheduler.py` from 2 to 5 to clear backlogs faster during peak times.
2.  **Improve Logging**: Update `scheduler.py` to capture and log lines containing "Validation failed" or "Skipping" to make these errors visible without deep diving.
3.  **Database Health**: The `bot.db` is robust, but the backlog distribution suggests we need to balance the posting slots better (WA has 200 items, SA has 2).

