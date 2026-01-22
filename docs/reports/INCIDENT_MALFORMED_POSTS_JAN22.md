# Incident Report: Malformed Post Floods (Jan 2026)

## Executive Summary
On Jan 22, 2026, the `council-news-bot` began publishing "malformed" posts to BlueSky. These posts contained future dates (e.g., Year 6175, Year 2070) or nonsense titles (e.g., "38", "6175").
**Root Cause**: Overly aggressive date parsing logic in `core/utils.py` combined with loose CSS selectors in multiple council configurations (`mackay`, `narromine`, `kwinana`).

## Detailed Findings

### 1. The "Kwinana" Anomaly (Year 6175)
- **Symptoms**: Posts with titles "6175", "38" and dates like `6175-12-05`.
- **Cause**: The `kwinana` scraper was configured as `catalyst_scraper`. The target site (Alyka CMS) uses `<span class="sr-only">NUMBER</span>` for accessibility counters. The scraper's fuzzy date parser interpreted these 4-digit numbers as years.
- **Action**: Disable `kwinana` scraper immediately. Develop dedicated `AlykaScraper`.

### 2. The "Mackay" Future Shock (Year 2070)
- **Symptoms**: Valid titles but impossible dates (2070, 7500).
- **Cause**: The configuration used `date_selector: "p"`. The scraper grabbed the first paragraph of content. If that paragraph mentioned a year (e.g., "Vision 2030") or a dollar amount/statistic, the `dateutil.parser(fuzzy=True)` logic extracted it as the publication date.
- **Action**: Tighten selectors. Disable `fuzzy=True` globally or restrict it to "Date-like" strings only.

### 3. The "Narromine" & "Chapman Valley" Data Leaks
- **Symptoms**: Addresses and Lot Numbers parsed as dates.
- **Cause**: Similar to Mackay—parsing non-date text as dates.
    - Narromine: "Lot 112 DP 755126" -> Year 7551.
    - Chapman Valley: "3270 Chapman Valley Road" -> Year 3270.

## Corrective Actions Taken (Immediate)
1.  **Emergency Stop**: Deployed `scripts/maintenance/cleanup_remote_db.py` to VPS.
2.  **Data Scrub**: Deleted ~50 malformed records from the production database.
3.  **Containment**: Disabled `kwinana` config.
4.  **Code Fix (Jan 22)**: Modified `core/utils.py` to remove `fuzzy=True` from date parsing for general cases, and added sanity checks (Year must be between 2020 and Current Year + 2). This prevents addresses and generic numbers from being interpreted as dates.
5.  **Verified**: Ran `test_date_logic.py` locally and verified fix via VPS cleanup logs.

## Strategic Shift: "Quality over Quantity"
The project has reached a tipping point where adding more scrapers increases the risk of "Z-starvation" (good content buried by bad) and "Hallucination" (bad data).

### New Protocols
1.  **Strict Date Parsing**: Deprecate `fuzzy=True` in `core/utils.py`. Dates must match specific formats (DD/MM/YYYY, Month DD YYYY).
2.  **Pre-Flight Validation**: New scrapers must pass a "Future Check" (Date <= Today + 1) before deployment.
3.  **Selector Audits**: Review all `curl_scraper` configs for generic selectors like `p`, `div`, `span` without classes.

## Next Steps
- [ ] **Fix Date Parser**: Modify `core/utils.py` to be stricter.
- [ ] **Audit "Loose" Scrapers**: Identify other councils with `date_selector: "p"`.
- [ ] **Implement `AlykaScraper`**: Properly support Kwinana, Stirling, etc.
- [ ] **Database Constraints**: Add a CHECK constraint to the SQLite DB `date <= '2030-01-01'` to reject bad writes at the storage level.
