# Full Council Health Check Report
**Date:** 2025-12-03

## Summary
| Category | Count | Description |
|----------|-------|-------------|
| **Total Enabled** | 312 | Total councils configured in the system. |
| **✅ Healthy** | 162 | Have collected news in the last 7 days. |
| **⚠️ Quiet** | 0 | Have collected news 7-30 days ago. |
| **❌ Silent** | 0 | Have collected news >30 days ago. |
| **💀 No Recent News** | 150 | No articles in database. (See Analysis below) |

## Analysis of "No Recent News" (150 Councils)
These councils have **0 articles** in the database. This can mean two things:
1.  **Scraper Broken:** The scraper is failing to find any articles (selectors changed, site blocked, etc.).
2.  **Old News Only:** The scraper is working and finding articles, but they are all older than the 7-day cutoff (`MAX_ARTICLE_AGE_DAYS = 7`), so they are skipped.

**Spot Checks:**
- `[vic] ballarat`: Found 9 articles in logs (all >7 days old). **Status: Working (Quiet)**
- `[nsw] burwood`: Found 10 articles in logs. **Status: Working (Quiet)**
- `[qld] aurukun`: Found 10 articles in logs. **Status: Working (Quiet)**

**Conclusion:**
The system is likely much healthier than the "162/312" stat suggests. Many of the 150 "No Recent News" councils are likely working but just haven't published news in the last week.

## Recommendations
1.  **Increase Initial Lookback:** Consider increasing `MAX_ARTICLE_AGE_DAYS` to 30 or 60 temporarily to populate the database with older news for these quiet councils (marking them as "old" so they don't post to Bluesky, just to fill the DB).
2.  **Log Scraper Stats:** Implement a `scraper_stats` table to record "Articles Found" vs "Articles Saved" per run. This would allow distinguishing "Broken" from "Quiet" instantly.

## Detailed List: No Recent News
### NSW (50+)
- burwood-council
- camden-council
- campbelltown-city-council
- ... (and many others)

### QLD (30+)
- aurukun
- balonne
- brisbane
- ...

### TAS (10+)
- launceston
- clarence
- glamorgan-spring-bay
- ...

### VIC (10+)
- ballarat
- buloke
- merri-bek
- ...
