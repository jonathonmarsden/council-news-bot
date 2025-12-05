# VPS Fix Report - 2025-12-05

## Issue
The VPS bot was only posting for NSW and failing to post for other states (VIC, WA, QLD, etc.).

## Root Causes
1.  **Deployment Sync**: The Docker container on the VPS was running an old version of the code that only contained the `states/nsw` folder. It was unaware of the other state configurations.
2.  **Data Consistency**: Western Australia (WA) articles were saved with lowercase `wa` in the database, but the poster was querying for uppercase `WA`.
3.  **Scheduler Robustness**: The scheduler lacked timeouts, meaning a single hanging scraper could stall the entire bot.

## Fixes Applied
1.  **Code Update**:
    -   Modified `scheduler.py` to include timeouts (60m for scraping, 5m for posting).
    -   Modified `core/database.py` to automatically fix state code casing (uppercase) on startup.
2.  **Deployment**:
    -   Ran the deployment script to push the latest code (including all `states/` folders) to the VPS.
    -   Rebuilt the Docker container on the VPS.

## Verification
-   **Logs**: Confirmed that the scheduler now detects and processes all states: `['act', 'nsw', 'nt', 'qld', 'sa', 'tas', 'vic', 'wa']`.
-   **Posting**: The logs show the bot is now cycling through posting for all states.

## Status
✅ **RESOLVED**. The bot is now fully operational for all states.
