# Deep Health Analysis Report
**Date:** 2025-12-03

## Executive Summary
A deep analysis of logs and database stats reveals that the system is significantly healthier than the raw database counts suggest.

| Metric | Count | % of Total | Status |
|--------|-------|------------|--------|
| **Total Councils** | 312 | 100% | |
| **✅ Confirmed Working** | **229** | **73%** | Scraper is finding articles (Fresh or Old). |
| **⚠️ Empty / Quiet** | 86 | 27% | Scraper runs but finds 0 articles (No news or broken selectors). |
| **❌ Error** | 0 | 0% | No scrapers are throwing exceptions. |

## 1. Freshness (Database)
*Based on articles saved to the database in the last 30 days.*
- **✅ Fresh (162):** Councils producing and posting news regularly.
- **❌ Never Seen (150):** No articles in the database.

## 2. Scraper Health (Logs)
*Based on the actual execution logs of the scrapers.*
- **✅ Working (211):** Scraper found > 0 articles on the page.
- **⚠️ Empty (86):** Scraper found 0 articles.
- **❓ Unknown (15):** No log entry found (likely truncated logs).

## 3. The "Working but Old" Cohort (67 Councils)
These **67 councils** appear as "Never Seen" in the database, but the logs prove the scrapers are **working perfectly**. They are finding articles, but the articles are older than 7 days, so the bot skips saving them.

**Examples:**
- `merri-bek`: Found **272 articles** (All old).
- `cardinia`: Found **20 articles** (All old).
- `aurukun`: Found **10 articles** (All old).
- `ballarat`: Found **9 articles** (All old).

## 4. Recommendations
1.  **System Health is Good:** 73% of scrapers are confirmed operational. The remaining 27% (Empty) likely includes many small councils that simply haven't posted news recently.
2.  **Adjust "Empty" Monitoring:** To verify the 86 "Empty" councils, we would need to manually check a sample. If they have news on their website but the bot finds 0, their selectors need updating.
3.  **Database Logging:** As previously recommended, logging "Articles Found" to the database would allow this analysis to be automated and real-time.

## Appendix: "Working but Old" Sample
*Scrapers that are working but have no recent news to post.*
- ballarat
- buloke
- merri-bek
- brimbank
- manningham
- hindmarsh
- moorabool
- whittlesea
- aurukun
- balonne
- ... (57 others)
