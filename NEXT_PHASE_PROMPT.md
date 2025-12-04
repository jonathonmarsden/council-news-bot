# Next Stage: Fixing the "Empty" Councils

## Context
We have confirmed that **229/312 (73%)** of our scrapers are working correctly. However, **86 councils** are returning **0 articles** during scrapes. We need to determine if these councils are simply quiet (no news) or if their scrapers are broken (selectors mismatch).

## Objective
Reduce the number of "Empty" scrapers by identifying broken selectors and fixing them, while verifying which councils are genuinely quiet.

## Action Plan

### 1. Infrastructure Improvement (Priority)
Instead of parsing text logs to find "Empty" scrapers, we should make the bot self-reporting.
- **Task:** Create a new database table `scraper_stats` (or `scraper_runs`).
- **Schema:** `id`, `council_id`, `run_at`, `articles_found` (int), `articles_saved` (int), `status` (text), `duration_ms` (int).
- **Implementation:** Update `main.py` / `scrape_single_council` to log these stats after every scrape.
- **Benefit:** This allows us to instantly query "Which councils found 0 articles in the last 24h?" via SQL.

### 2. Diagnosis & Fixes
While the infrastructure collects data, we should start manually debugging the known "Empty" list.
- **Task:** Extract the list of 86 "Empty" councils from the recent log analysis.
- **Task:** Create a `debug_batch.py` script that:
    1. Takes a list of council IDs.
    2. Fetches their news page HTML.
    3. Saves the HTML to a `debug_html/` folder.
    4. Tries to run the current scraper and reports the result.
- **Task:** Analyze the HTML for the first batch (e.g., 10 councils) to see if news items exist but are being missed.
    - **If missed:** Update selectors in `councils.json`.
    - **If truly empty:** Mark as "Verified Quiet" (maybe add a note in `councils.json`).

### 3. Execution Prompt
```text
I am ready to tackle the "Empty" councils. 

First, please implement the `scraper_stats` table in the database and update the scraper logic to log run statistics. This is critical for long-term monitoring.

Next, extract the list of 86 councils that were identified as "Empty" (Found 0 articles) in the previous deep health check. 

Then, let's pick the first 5 of these "Empty" councils and run a deep debug on them:
1. Fetch their current HTML.
2. Check if there are actually news items on the page that we are missing.
3. If we are missing items, fix the selectors.
```
