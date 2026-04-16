# Action Plan - Next Session

**Date**: 25 January 2026
**Status**: Bot is stable, logging enabled, SA recovered.

## 🎯 Primary Goal: Stability & Coverage Repair

### 1. Fix Broken Scrapers (NSW & VIC)
These councils were identified as failing or returning 0 items during the audit.
- [ ] **Weddin Shire Council (NSW)**: 
    - Issue: Selectors broken (finding items but extraction fails).
    - File: `states/nsw/councils.json`
    - Test: `python3 main.py --council weddin --dry-run`
- [ ] **Greater Hume Council (NSW)**:
    - Issue: Selectors broken (Extraction failure).
    - File: `states/nsw/councils.json`
    - Test: `python3 main.py --council greater-hume --dry-run`
- [ ] **Georges River Council (NSW)**:
    - Issue: Proxy/Connection Error (`502 Bad Gateway`).
    - Task: Investigate if proxy credentials are stale or if site blocks proxy. Try `curl_scraper`.
- [ ] **Knox City Council (VIC)**:
    - Issue: 5 Consecutive Failures (Health Check).
    - Task: Rotate `impersonate` profile in `states/vic/councils.json` (Try `chrome110` or `safari15_5`).

### 2. Configuration Cleanup (WA)
**Risky Config**: ~50 WA councils have `"use_curl": false` hardcoded.
- [ ] **Bulk Edit**: Remove `"use_curl": false` from `states/wa/councils.json`.
    - *Why*: Prevents `BaseScraper` from auto-upgrading to `curl_cffi` if a WAF is added.
    - *Method*: Use Regex replace or a Python script to safely remove the line.

### 3. Operational Safety
- [ ] **Log Rotation**:
    - The new scraper logs (`/var/log/council_bot_scraper.log`) are **not** rotated.
    - Task: Create a logrotate config on the VPS to prevent disk fill.
- [ ] **Deadman Switch**:
    - Task: Write a script (`scripts/monitoring/deadman_check.py`) that alerts Discord if `articles` table has 0 new entries for >6 hours.

### 4. Verification
- [ ] **Check Logs**:
    - After the **12:00 UTC** run (approx 2 hours from now), SSH into VPS and check:
    `tail -n 200 /var/log/council_bot_scraper.log`
    - Confirm all states (Groups A, B, C, D) launched and completed.

## 📚 Handover Notes
- **VPS IP**: `170.64.186.16` (User: `root`)
- **App Path**: `/opt/council-news-bot`
- **Logs**:
    - Scrapers: `/var/log/council_bot_scraper.log` (New!)
    - Poster/Cron: `/var/log/council_bot_cron.log`
- **Database**: Postgres in Docker (`council_db`).
