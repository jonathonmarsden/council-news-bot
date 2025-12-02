# Council News Bot Architecture

## Overview
The Council News Bot is a scalable system designed to scrape news from Australian local government websites and publish updates to social media (BlueSky). It currently supports Victoria (VIC) and New South Wales (NSW), with a design ready to scale to all ~500 councils across Australia.

## Project Structure

```
council-news-bot/
├── main.py                 # CLI Entry Point
├── scheduler.py            # Simple task scheduler
├── core/                   # Core logic
│   ├── scraper.py          # Base scraper classes (CardScraper, InnerWestScraper)
│   ├── database.py         # SQLite database handler
│   ├── poster.py           # BlueSky API client
│   └── utils.py            # Logging and utilities
├── states/                 # State-specific configurations
│   ├── vic/
│   │   ├── config.json     # State metadata
│   │   └── councils.json   # List of councils and scraper configs
│   └── nsw/
│       ├── config.json
│       └── councils.json
├── scripts/                # Maintenance and testing scripts
└── data/                   # (Ignored) Runtime data
```

## Core Components

### 1. Scraper Engine (`core/scraper.py`)
-   **`CardScraper`**: The workhorse class. It handles 90% of councils that use a standard "card" layout for news. It supports:
    -   CSS Selectors for title, date, link, content.
    -   `curl` mode for sites blocking `requests`.
    -   Mobile User-Agent mode.
-   **Custom Scrapers**: For complex sites (e.g., `InnerWestScraper`), we subclass `CardScraper` to add specific logic (like fetching detail pages for dates).

### 2. Configuration (`states/{state}/councils.json`)
Configuration is decoupled from code. Each council is defined by JSON:
```json
{
    "id": "inner-west-council",
    "name": "Inner West Council",
    "news_url": "...",
    "scraper": "inner_west_scraper",
    "item_selector": "article.block",
    "title_selector": "h2"
}
```

### 3. Database (`core/database.py`)
-   **SQLite**: Stores article URLs, titles, dates, and posting status.
-   **Deduplication**: Ensures we don't post the same article twice.
-   **Schema**: Simple `articles` table.

### 4. Scheduler (`scheduler.py`)
-   Currently runs a simple loop.
-   **Scraping**: Every 3 hours.
-   **Posting**: Every 15 minutes (05:00 - 22:00).

## Scalability Strategy (500+ Councils)

To support 500+ councils, we have implemented the following:

1.  **Concurrent Scraping**: 
    -   Implemented `ThreadPoolExecutor` in `main.py`.
    -   Allows scraping multiple councils simultaneously (default 5 workers).
    -   Reduces total scrape time significantly.
2.  **Smart Proxying**:
    -   "Direct First" strategy in `core/scraper.py`.
    -   Only uses proxy bandwidth when direct connection fails.
    -   Minimizes costs while maintaining access reliability.
3.  **Configuration Management**: 
    -   Split by state (`states/vic`, `states/nsw`, `states/qld`).

## Scheduling

To ensure freshness without spamming:

-   **Scraping**:
    -   Runs every 3 hours via `scheduler.py`.
    -   Uses concurrency to complete quickly.
-   **Posting**:
    -   The bot posts *one* article every 5-15 minutes (configurable).
    -   This acts as a "buffer". If we scrape 50 articles at 06:00, they will be dripped out over the next few hours.
    -   *Benefit*: Prevents flooding the feed.

## Future Improvements

1.  **PostgreSQL**: Migrate from SQLite to PostgreSQL if concurrency becomes an issue.
2.  **Web UI**: A simple dashboard to view scraper status and errors.
3.  **VPS Deployment**: Move from local execution to a cloud VPS for 24/7 uptime.
