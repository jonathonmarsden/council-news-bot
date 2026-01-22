# System Scaling & Limits Report (Jan 2026)

## 1. Overview
This document records the analysis of system throughput, bottlenecks, and configuration limits conducted on Jan 22, 2026.

## 2. Bottleneck Analysis

### A. The "Four Layers" of Constraint
Articles must pass through four distinct filters/bottlenecks to reach BlueSky.

| Layer | Constraint | Config File | Behaviour |
| :--- | :--- | :--- | :--- |
| **1. Freshness** | `MAX_ARTICLE_AGE_DAYS = 7` | `main.py` | **Hard Filter**. Any article older than 7 days at scrape time is marked `archived` and *never* posted. |
| **2. Validation** | `IDEAL_EXCERPT_LEN = 250` | `core/validator.py` | **Quality Filter**. Articles with malformed content or overly long excerpts are silently skipped (logged to stdout). |
| **3. Scheduler** | `--limit 10` per state | `scheduler.py` | **Throughput Cap**. Controls how many items clear the backlog every 5 minutes. |
| **4. Variety** | Round Robin Logic | `core/database.py` | **Distribution**. prevents one council from dominating the feed. Cycles through available councils A->B->C->A... |

### B. Recent Tuning (Jan 22, 2026)
We identified that the backlog was clearing too slowly (2 posts/run) for large states like WA.
- **Change**: Increased scheduler limits in `scheduler.py`.
    - `--limit` (Total jobs per state): **2** -> **10**.
    - `--max-per-council` (Anti-monopoly): **Default (5)** -> **10**.
- **Impact**: Theoretical max throughput increased from 24 posts/hour/state to **120 posts/hour/state**.

## 3. The "Missing Posts" Phenomenon
**Observation**: "There doesn't seem to be as many posts as there should be."
**Root Cause**: The **Freshness Filter**.
- When a broken scraper is fixed, it often retrieves historical data (e.g., last 30 days).
- ~85% of these retrieved articles are >7 days old.
- The system correctly identifies them as "Stale" and archives them without posting.
- **Implication**: Fixing a scraper often results in `0 posted` immediately, but `New articles` appearing in the database for *future* posts.

## 4. Operational Recommendations
1.  **Backlog Management**: The current limit of 10/run is sufficient to clear a 200-item backlog in approx 2 hours.
2.  **Monitoring**: Watch for API Rate Limit errors (BlueSky limit is approx 3,000/hour, so we are safe, but burst limits apply).
3.  **Future "Force Post" Feature**: If we want to announce historical news for a newly onboarded council, we would need to implement a `--force-fresh` flag in `main.py` to bypass the 7-day check.
