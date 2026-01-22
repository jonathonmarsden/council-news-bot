# Incident Report: Malformed Content & Garbage Posts
**Date**: 22 January 2026
**Severity**: High (Content Quality / Brand Reputation)

## Issue Description
Users reported the bot publishing "garbage" posts to Bluesky, including:
1.  **"Found Cat" / "Lost Dog"**: Sourced from Lost & Found registries (e.g., Darwin, NT).
2.  **"ATO iage"**: Placeholder alt-text being scraped as titles (e.g., Light Regional, SA).
3.  **"Posted 04 December 2025"**: Date strings being scraped as titles (Widespread in WA Catalyst sites).
4.  **"2026" / "2025"**: Year headers being scraped as titles (Karoonda, SA).

## Findings
- **Catalyst CMS Scraper (`catalyst.py`)**: The selector `.h4` often matched the "Posted [Date]" span instead of the actual title in some layouts, or the site structure was ambiguous. This caused ~1300+ bad entries in the DB.
- **Darwin Scraper**: Was picking up "Lost & Found" items because the news selector was too broad or the council puts these in the main news feed.
- **Filter Logic**: The bot lacked a semantic validation layer. It assumed anything matching the CSS selector was a valid news article.

## Corrective Actions

### 1. Database Cleanup
- Ran `scripts/maintenance/cleanup_remote_db.py` on VPS.
- **Purged**:
    - ~1350 entries with titles like "Posted ..."
    - Future-dated articles (>2027)
    - "Found Cat" / "ATO image" entries
    - Commercial copyright footers

### 2. Content Firewall (`main.py`)
Implemented `is_valid_article()` function to reject articles before saving:
- **Length Check**: Rejects titles < 5 chars.
- **Numeric Check**: Rejects titles that are just numbers (e.g., "2026").
- **Semantic Check**: Rejects "Found Cat", "Lost Dog", "ATO image", "No Title".
- **Pattern Check**: Rejects "Posted [Date]" patterns.
- **Navigation Check**: Rejects "Home", "Sitemap", "Contact Us".

### 3. Scraper Hardening
- **Catalyst Scraper**: Updated to explicitly ignore titles starting with "Posted " followed by digits.

## Next Steps / Recommendations
1.  **Monitor Logs**: Watch for "Rejected X articles as invalid garbage content" in logs.
2.  **Specific Scrapers**: If `darwin` continues to yield garbage despite the generic filters (e.g. if "Found Cat" varies to "Found Tabby Cat"), we must update the `darwin` scraper selectors specifically.
3.  **Visual QA**: Manually review the Bluesky feed for the next 48h.

## Learnings
- **Trust but Verify**: CSS selectors are brittle. Just because an element is in the "news" div doesn't mean it's a news headline.
- **Generic Filters**: A global "quality assurance" filter is more efficient than tuning 500+ individual scrapers for edge cases.
- **Data Hygiene**: The database should be treated as a cache of *potential* posts. Validation should happen both at scrape time and post time.
