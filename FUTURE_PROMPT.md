# Architecture Refactor: Parallel Scheduler for Council News Bot

## Status: COMPLETE (2025-12-03)

The `scheduler.py` has been successfully refactored to use `asyncio`.
- **Scraping**: Runs in a non-blocking subprocess loop every 3 hours.
- **Posting**: Runs in a concurrent loop every 5 minutes.
- **Verification**: Logs confirm that posting tasks execute immediately even while scraping tasks are active.

## Future Improvements

### 1. Database Concurrency
With parallel execution, we are now running multiple instances of `main.py` simultaneously (one for scraping, potentially 5 for posting).
- **Risk**: SQLite database locking.
- **Mitigation**: WAL mode is enabled, but we should monitor for `database is locked` errors.
- **Next Step**: If locking becomes an issue, consider migrating to PostgreSQL or implementing a dedicated DB writer service.

### 2. Scrape Optimization
Scraping is currently sequential by state (`await scrape_state(state)` inside a loop).
- **Improvement**: We could run states in parallel too, but this might overload the VPS (CPU/RAM).
- **Action**: Monitor VPS resource usage (htop) during a full scrape cycle.

### 3. Error Reporting
Currently, errors are logged to stdout.
- **Improvement**: Integrate a notification system (e.g., Discord webhook, Email) for critical failures (e.g., "Scrape failed for NSW").

## Original Context (Archived)
The current `scheduler.py` implementation is single-threaded and blocking. It performs two main tasks:
1.  **Scraping**: Runs every 3 hours for all 5 states (ACT, NSW, QLD, TAS, VIC).
2.  **Posting**: Runs every 5 minutes (5am-10pm) to post 1 article per state.

## The Problem (SOLVED)
The `run_scrape` function uses `subprocess.run(..., check=True)`, which blocks the main execution thread.
-   Scraping NSW alone involves checking ~128 councils and can take 10-20 minutes.
-   Scraping all 5 states sequentially can take over an hour.
-   **Critical Issue**: During this scrape time, the scheduler is "stuck" in the scrape loop and **cannot execute the posting logic**. This results in massive gaps in posting (e.g., no posts for an hour) followed by a burst of activity, rather than the intended steady 5-minute cadence.

## Solution Implemented: Option A (Asyncio Scheduler)
Refactored `scheduler.py` to use Python's `asyncio` library.
-   Used `asyncio.create_subprocess_exec()` for scraping tasks.
-   The main event loop continues to check the time and trigger posting tasks even while a scrape subprocess is running in the background.


## Prompt for Agent
"Refactor `scheduler.py` to use `asyncio`. The goal is to ensure that long-running scrape jobs (which happen every 3 hours) do not block the posting jobs (which must happen every 5 minutes). The scraper for each state should run in a non-blocking subprocess, allowing the main loop to continue checking for posting intervals."
