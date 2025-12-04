# Daily Health Check & Fix Report

## 1. Warren Shire Council Fix
**Status:** ✅ Fixed
**Issue:** Titles were malformed with date suffixes (e.g., "Title29 February 2024") and "Media Release" prefixes.
**Action Taken:**
- Updated `CardScraper` regex to handle date suffixes and prefixes.
- Ran database cleanup script (`fix_warren_db.py`) on VPS.
- **Result:** 103 articles updated in the database. Titles are now clean (e.g., "Council Meeting Highlights February 2024").
- **Bluesky:** Malformed posts were deleted. Clean articles are now marked as `[Pending]` and will be reposted automatically.

## 2. Global Health Check
**Generated At:** 2025-12-03 (VPS Time)

### Council Status (Last 7 Days)
| Council | Collected | Posted (24h) | Status |
|---------|-----------|--------------|--------|
| **Warren Shire** | 103 | 10 | ✅ Recovering (Reposting active) |
| **Cairns** | 5 | 5 | ✅ Active |
| **Circular Head** | 1 | 0 | ✅ Active |
| **Kingborough** | 4 | 0 | ✅ Active |
| **Huon Valley** | 3 | 0 | ✅ Active |
| **Glamorgan-Spring Bay** | 0 | 0 | ⚠️ No new news (Feed active) |
| **Break O'Day** | 0 | 0 | ⚠️ No new news |
| **Brighton** | 0 | 0 | ⚠️ No new news |

### System Health
- **Database:** Connected to `/opt/council-news-bot/data/bot.db`.
- **Scrapers:** VIC scraper finished successfully at 14:01 UTC.
- **Logs:** No critical errors observed in recent tail.

## 3. Recommendations
- **Monitor Warren Shire Reposts:** The bot is currently reposting the cleaned articles. Expect a flood of ~100 posts over the next few cycles (throttled).
- **Tasmania Review:** Some councils (Glamorgan, Break O'Day) have low activity. This may be normal for small councils, but worth periodic manual checks.
- **Database Cleanup:** A rogue `bot.db` exists in the root directory `/opt/council-news-bot/bot.db` which is stale. Future scripts should ensure they use the data volume path `/opt/council-news-bot/data/bot.db`.

## 4. Next Steps
- Allow the bot to run its course to repost the Warren Shire backlog.
- No further immediate action required.
