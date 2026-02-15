# Council News Bot - Copilot Instructions

## 1. Project Summary
A robust, Dockerized Python system for aggregating and publishing Australian Local Government news.
It scrapes hundreds of council websites using configurable strategies (BeautifulSoup, Playwright, curl_cffi), deduplicates content via PostgreSQL, and broadcasts updates to BlueSky and Discord.
The architecture uses a staggered scheduler to manage concurrency, respects `robots.txt` where possible, and emphasizes "fail-loud" reliability.
Key components: Scraper Engine (Core), State Configs (JSON), and Publishing Queue (Cron).

## 2. Key Folders & Responsibilities
- **`main.py`**: CLI entry point for scraping and posting. Orchestrates the flow.
- **`core/`**: The brain.
    - `scrapers/`: Extraction logic (`base.py`, `json_scraper.py`, etc.).
    - `database.py`: SQLAlchemy models and DB interactions.
    - `poster.py`: BlueSky/Discord API integration.
- **`states/{state_code}/`**: Configuration. `councils.json` defines target URLs and CSS selectors.
- **`scripts/`**: Operations.
    - `cron/`: Production tasks (`process_global_queue.py`).
    - `monitoring/`: Health checks and reporting (`daily_briefing.py`).
    - `maintenance/`: DB cleanup and repairs.
- **`tests/`**: Pytest suite for verifying core logic and critical parsers.

## 3. Development Commands
- **Install**: `pip install -r requirements.txt` (or `docker build -t council-bot .`)
- **Run Scraper (Dev)**: `python3 main.py --state vic --council melbourne --dry-run`
- **Run Scraper (Prod)**: `python3 main.py --state nsw --concurrency 5`
- **Run Poster**: `python3 scripts/cron/process_global_queue.py`
- **Test**: `pytest` (Run specific: `pytest tests/test_vic_extraction.py`)
- **Lint/Format**: Follow PEP8. Use `black` if available.

## 4. Coding Conventions & Error Handling
- **No Silent Failures**: If a scraper finds 0 items, raise an error or warn. Do not return empty lists silently.
- **Logging**:
    - **User-Facing**: Use `print()` (captured by manual runs).
    - **System**: Use `logging` or write to `stderr` (captured by Docker/Cron logs).
    - **Alerts**: Use `discord_logger.py` for operational alerts (e.g., "Scraper failing for 3 days").
- **Selectors**: Prefer semantic IDs/classes (`#news-list`, `.article-item`) over fragile xpaths (`div > div > div`).
- **Dates**: Always enforce Australian Date Format (`DD/MM/YYYY`) using `dateutil` with `dayfirst=True`.

## 5. Non-Negotiable Constraints
- **Secrets Management**: NEVER hardcode credentials. Use `.env` and `os.environ`.
- **Idempotency**: The Database (`articles.url`) is the source of truth. Always check existence before insertion.
- **Rate Limiting**:
    - Scrapers: Respect `time.sleep` (default 2s) between requests if iterating.
    - Poster: Max ~24 posts/hour per state to avoid BlueSky bans.
- **Schema Stability**: Do not modify the database schema without an Alembic migration script.
- **Absolute Paths**: The VPS environment differs from local. Use `Path(__file__).parent` resolution, never relative paths like `./data`.

## 6. Path-Specific Instructions (Proposed)

### `states/**/*.json` (.instructions.md)
- **Validation**: Ensure strict JSON syntax (no trailing commas).
- **Mandatory Fields**: `id`, `name`, `news_url`, `scraper`.
- **Selector Rules**: `item_selector` must identify the container; `link_selector` is relative to item.

### `core/scrapers/*.py` (.instructions.md)
- **Inheritance**: All scrapers must inherit from `BaseScraper`.
- **headers**: Always use `User-Agent` rotation or a specific `impersonate` profile for WAFs.
- **Return Type**: Must return a list of `Article` objects (never raw dicts).

### `scripts/**/*.py` (.instructions.md)
- **Safety**: Destructive scripts (delete/update) must have a `--dry-run` flag enabled by default.
- **Imports**: Must handle `sys.path` appending to ensure `core` modules are resolvable.
