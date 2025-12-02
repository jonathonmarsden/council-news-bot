# Prompt for National Scale-Up

**Role:** Senior Python Architect & DevOps Engineer
**Project:** Council News Bot (National Scale-Up)
**Context:** The bot currently runs on a VPS, scraping ~30-50 councils across VIC, NSW, QLD, and TAS. We are preparing to scale to all ~537 Australian Local Government Areas (LGAs).

**Current Architecture:**
- **Core:** Python 3.11, `requests`, `BeautifulSoup`, `ThreadPoolExecutor`.
- **Database:** SQLite (`bot.db`).
- **Scheduler:** Simple Python loop spawning `subprocess` calls to `main.py`.
- **Deployment:** Docker on DigitalOcean Droplet.

**Objective:**
Refactor and optimize the codebase to support 500+ councils reliably, ensuring performance, stability, and maintainability.

**Tasks:**

1.  **Database Optimization (Critical for Scale):**
    -   **Bulk Inserts:** Refactor `core/database.py` to support `add_articles_bulk(articles)` using `executemany` and a single transaction. The current implementation commits after every row, which will be too slow for 5000+ articles.
    -   **WAL Mode:** Enable SQLite Write-Ahead Logging (WAL) mode (`PRAGMA journal_mode=WAL;`) to improve concurrency and prevent "database locked" errors if we parallelize state scrapes.
    -   **Migration Path:** Create a schema migration script (or use a lightweight tool like `alembic` if justified, though raw SQL is likely fine for this size) to ensure the DB schema is consistent.

2.  **Scheduler Improvements:**
    -   **Dynamic State Discovery:** Modify `scheduler.py` to automatically detect available states in the `states/` directory instead of using a hardcoded list `["vic", "nsw", "qld", "tas"]`.
    -   **Parallel State Execution:** (Optional but recommended) Allow scraping multiple states in parallel processes. *Note: Requires WAL mode enabled first.*

3.  **Scraper Resilience (Circuit Breaker):**
    -   Implement a "Circuit Breaker" mechanism in `core/scraper.py` or `main.py`.
    -   Track consecutive failures for each council in the database (new table or column).
    -   If a council fails (e.g., 403 Forbidden, Connection Error) > 5 times consecutively, automatically mark it as `disabled` or `quarantined` and log a high-priority warning. This prevents the bot from wasting resources on broken targets.

4.  **Config Validation:**
    -   Create a script `scripts/validate_configs.py` that checks all `councils.json` files against a schema (e.g., using `pydantic` or `jsonschema`).
    -   Ensure all required fields (`id`, `name`, `news_url`, `scraper`) are present and valid.

5.  **Logging & Monitoring:**
    -   Ensure all logs are structured (JSON logs preferred for production) or at least consistently formatted with timestamps.
    -   Create a `scripts/daily_report.py` that generates a summary of:
        -   Total articles scraped today.
        -   Number of active vs. failed councils.
        -   List of councils that triggered the Circuit Breaker.

**Deliverables:**
-   Updated `core/database.py` with bulk operations and WAL mode.
-   Updated `scheduler.py` with dynamic discovery.
-   New `scripts/validate_configs.py`.
-   (Optional) Implementation of the Circuit Breaker pattern.

**Next Steps:**
Once these architectural improvements are in place, proceed to:
1.  Fix the broken Tasmania scrapers (Batch 5+).
2.  Begin onboarding South Australia (SA) councils.
