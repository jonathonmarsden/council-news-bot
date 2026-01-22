# Post-Incident Report: Malformed Posts & Tag Duplication (2026-01-22)

## Executive Summary
On Jan 22, 2026, the Council News Bot feed experienced two quality regressions:
1.  **Malformed Posts**: Posts appearing with titles like "Posted 22 January" or "Quick Links", and incorrectly identified Council Names (e.g., "LGNewsRoundup Council").
2.  **Tag Duplication**: Posts appearing with a trailing line of plain-text tags (e.g., `LGNewsRoundup LGAQ QLDCouncils`) duplicated below the real hashtags.

Both issues have been resolved, and safeguards have been implemented to prevent recurrence.

## 1. Malformed Posts (The "Fixer" Incident)
### Root Cause
The `scripts/process_bookmarks.py` script, intended to fix bad titles, used a "heuristic" approach to guess the Council Name from the post text. It scanned for "the line before the hashtags".
*   **Failure Mode**: When the text format varied (e.g., due to a previous bad scrape), the script guessed incorrectly, capturing URL fragments or tag groups as the Council Name.
*   **Compound Failure**: For Councils like **Townsville**, the strict domain lookup failed because they use a cloud host (`tcc-search.funnelback.squiz.cloud`) instead of their `.gov.au` domain.

### The Fix
We completely rewrote `scripts/process_bookmarks.py` to use a **Hybrid Safelist** approach:
1.  **Strict Domain Map**: The script now checks the URL domain against a `council_domain_map.json`.
    *   *Improvement*: Added aliases for known cloud hosts (Squiz, Funnelback).
2.  **Official Name Safelist**: If the domain check fails, the script scans the text *only* for exact matches of Official Council Names (e.g., "City of Townsville") defined in our config.
3.  **Fail-Safe**: If neither method yields a confirmed match, the script **SKIPS** the post instead of guessing.

## 2. Tag Duplication (The "Double Tag" Bug)
### Root Cause
A regex error in the updated `process_bookmarks.py`:
*   `re.findall(r'#(\w+)', text)` captured tag text *without* the `#` prefix (e.g., `LGAQ`).
*   This was passed to `poster.py`, which expects hashtags (with `#`).
*   `poster.py` treated them as "Extra Topics", and because "LGAQ" != "#LGAQ", it appended them as new plain-text words at the end of the post.

### The Fix
*   **Code**: Updated `process_bookmarks.py` to prepend `#` to extracted tags before passing them to the poster.
*   **Cleanup**: Created and executed `scripts/fix_recent_tag_mess.py`, which scanned the last 100 posts of all bots, identified the 12+ malformed posts, and automatically reposted them correctly.

## 3. System Safeguards Inventory

We now have three layers of defense against bad content:

### Layer 1: Scraper Hygiene
*   **Catalyst Scraper**: Explicitly rejects titles starting with "Posted [Date]" or numeric strings.
*   **Validator**: `core/validator.py` blocks posts with generic titles ("Home", "Quick Links"), invalid URLs, or absurd lengths.

### Layer 2: Poster Hygiene (`core/poster.py`)
*   **Title Sanitization**: Automatically strips leading dates (e.g., "Fri 28 Nov - Council Meeting" -> "Council Meeting").
*   **Length Enforcement**: Hard truncate at 300 chars to satisfy BlueSky API.
*   **Facet Validation**: Prevents byte-span errors that crash the client.

### Layer 3: The "Safe Mode" Fixer
*   **Deterministic ID**: No more guessing. Council identification is now 100% database-backed.
*   **Tag Deduplication**: Enforces strict hashtag ordering and prevents duplicates.

## 4. Operational Procedures

### Deployment
The VPS (`vps.example.com`) must be updated to include these fixes.
*   **Command**: `python3 scripts/deployment/deploy_with_password.py`
*   **Verify**: `ssh root@... 'cd /opt/council-news-bot && git log -n 1'`

### Handling Bookmarks
To process the "Saved Posts" queue (the manual review buffer):
1.  Run `python3 scripts/monitor_bookmarks.py` to see what is pending.
2.  Run `python3 scripts/process_bookmarks.py` to fix and post them.
    *   *Note*: This script is now safe to run unattended.

## 5. Next Steps
- [ ] **Deploy**: Run the deployment script immediately to push fixes to Production.
- [ ] **Monitor**: Check the timeline tomorrow morning for any new "Found Cat" or "Posted..." anomalies.
