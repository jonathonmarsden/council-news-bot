# Incident Report: Malformed "Posted Date" Titles
**Date**: 22 January 2026
**Severity**: High (Content Quality)
**Status**: Resolved

## 🚨 Incident Description
Around 20+ posts appeared on the WA Bot feed (`@roundupnewsbotwa.bsky.social`) with titles consisting solely of the date, e.g., `"Posted 03 December 2025"`. The body text duplicated this line, creating low-quality output.

## 🕵️ Root Cause Analysis
1.  **Source**: The `CatalystScraper` (used by many WA councils like Gingin, Donnybrook) targets `.h4` elements for titles.
2.  **Trigger**: On some CMS pages, or due to a specific layout state, the date string (usually `.h5` or specifically tagged) was picked up as the title.
3.  **Failure of Checks**:
    *   While `catalyst.py` had logic to reject "Posted...", it may have been added *after* the initial bad scrape, or the bad data was sitting in the `bot.db` (Database) with `posted=0`.
    *   **Main Failure**: `main.py`'s `post_articles` function pulled these old/bad records from the DB and posted them **without re-validating** against the `is_valid_article()` firewall.

## 🛠️ Remediation Steps Taken
1.  **Immediate Fix (Code)**:
    *   Updated `main.py` to invoke `is_valid_article()` inside the posting loop. This acts as a final "Gatekeeper" to prevent DB poisoning from leaking to the public feed.
    *   Updated `is_valid_article` to handle both `NewsArticle` objects and Dictionary records from the DB.

2.  **Content Cleanup (Data)**:
    *   Developed `scripts/process_bookmarks.py` (originally `fix_malformed_bookmarks.py`).
    *   This script connects to the undocumented Bluesky Bookmarks API (`app.bsky.bookmark.getBookmarks`).
    *   It identifies posts with the regex `^Posted \d+` matching the specific Catalyst bug.
    *   It scrapes the *original* link to find the *real* H1 title.
    *   It logs in as the specific state bot (e.g. WA Bot).
    *   It **Deletes** the bad post and **Reposts** with the correct title.
    *   **Result**: 23 malformed posts were automatically fixed.

3.  **Verification**:
    *   `scripts/monitor_bookmarks.py` now reports **0 issues**.

## 📚 Lessons Learned
*   **Database Trust**: We cannot trust `bot.db` to contain only valid data. Validation logic must apply at *Scrape Time* AND *Post Time*.
*   **Bookmarks as Queue**: The Bluesky Bookmarks API is a powerful tool for "Human-in-the-loop" moderation. We now have a proven workflow: User bookmarks bad post -> Script fixes it.
*   **Multiple Bot Management**: Scripts must handle multi-tenant authentication (switching between WA/VIC/etc bots) when performing maintenance.

## 📋 Next Steps
*   Run `process_bookmarks.py` periodically or manually when weird posts are spotted.
*   Monitor WA feed for any new patterns of failures.
