# Task: Fix Broken and Low-Quality Scrapers

## Context
We have deployed the Council News Bot to production. It covers **539 councils** across Australia.
However, some scrapers may be:
1.  **Failing silently**: Returning 0 articles.
2.  **Returning incomplete data**: Specifically missing dates (`NULL` in database), which prevents "freshness" filtering.

## Objective
Systematically identify and fix scrapers that are underperforming.

## Step 1: Diagnosis (Run Locally)
1.  **Identify Zero-Yield Scrapers**:
    -   Query the database (or `councils.json` vs database) to find councils that have **0 articles** recorded.
    -   *Note*: Some small councils genuinely have no news. We need to distinguish "no news" from "broken scraper".
2.  **Identify Date-Parsing Failures**:
    -   Query the database for councils with a high percentage of `date IS NULL`.
    -   *Known Issues*: Kent, Mingenew, Bunbury, Carnamah (WA).

## Step 2: Execution Strategy
For each identified broken council:
1.  **Create a Debug Script**:
    -   Use `core/scrapers/test_scraper.py` or create a specific `debug_[council_name].py`.
    -   Fetch the live content.
2.  **Analyze the HTML**:
    -   Check if the selectors in `councils.json` match the current website structure.
    -   Look for `date` elements that might require custom parsing or a new selector.
3.  **Fix**:
    -   Update `councils.json` with new selectors.
    -   OR implement a custom scraper in `core/scrapers/custom.py` if the site is complex (SPA, JSON feed, etc.).
4.  **Verify**:
    -   Run the debug script again to confirm data extraction (Title, URL, Date).

## Priority List (Based on initial logs)
1.  **Western Australia (WA) Date Fixes**:
    -   Kent (21 null dates)
    -   Mingenew (9 null dates)
    -   Bunbury (8 null dates)
    -   Carnamah (8 null dates)
    -   Donnybrook-Balingup (7 null dates)
2.  **Zero-Yield Audit**:
    -   Run a script to list all enabled councils with 0 articles in `bot.db`.

## Deliverable
-   Updated `councils.json` files.
-   Updated `core/scrapers/custom.py` (if needed).
-   A report of fixed councils.
