# Code Review & Refactoring Plan

## Code Review

### Strengths
1.  **Flexible Scraping Architecture**: The `CardScraper` class, especially with the recent addition of configurable CSS selectors, is highly adaptable. It can handle a wide variety of council website layouts (OpenCities, Squiz Matrix, Webflow, etc.) without requiring custom code for each one.
2.  **Robust WAF Evasion**: The inclusion of a `curl` fallback mechanism allows the bot to bypass strict Web Application Firewalls (like Akamai/Cloudflare) that often block Python `requests`.
3.  **Feed Quality Logic**: The `_diversify_by_council` function ensures the social media feed isn't dominated by a single council, providing a better user experience.
4.  **Freshness Filtering**: The logic to filter out old articles prevents the bot from spamming the feed with outdated news when a new council is added.

### Areas for Improvement
1.  **Scalability (State Management)**:
    *   **Issue**: The current reliance on a single `posted_articles.json` file is risky. As the number of councils and articles grows (especially when expanding to all states), this file will become large, slow to parse, and prone to corruption if the process is interrupted during a write.
    *   **Solution**: Migrate to a SQLite database. This provides ACID compliance, faster lookups, and better data integrity.

2.  **Configuration Management**:
    *   **Issue**: `councils.json` is a flat list. Managing hundreds of councils across multiple states in a single file will be unwieldy.
    *   **Solution**: Split configuration by state (e.g., `states/vic/councils.json`, `states/nsw/councils.json`).

3.  **Multi-Tenancy (Multi-State Support)**:
    *   **Issue**: The bot currently assumes a single BlueSky account (via environment variables). Running bots for "VIC", "NSW", "QLD" simultaneously would require complex environment management or code duplication.
    *   **Solution**: Refactor `main.py` and `poster.py` to accept configuration objects that define the target state and credentials, allowing a single codebase to run multiple bot instances.

4.  **Project Structure**:
    *   **Issue**: `main.py` is becoming a "god object", handling orchestration, state loading, and business logic.
    *   **Solution**: Modularize the code into a `core/` package (database, scraper, poster) and a `states/` directory for configuration.

---

## Refactoring Plan

### 1. Directory Structure
We will reorganize the project to separate core logic from configuration.

```text
council-news-bot/
├── core/
│   ├── __init__.py
│   ├── database.py       # New: SQLite database handler
│   ├── scraper.py        # Refactored: BaseScraper, CardScraper
│   ├── poster.py         # Refactored: BlueSkyPoster (accepts creds)
│   └── utils.py          # Logging, date parsing
├── states/
│   ├── vic/
│   │   ├── config.json   # State settings (handle, password_env_var)
│   │   └── councils.json # VIC councils list
│   ├── nsw/
│   │   ├── config.json
│   │   └── councils.json
│   └── ...
├── main.py               # CLI entry point (accepts --state arg)
├── requirements.txt
└── README.md
```

### 2. Database Implementation (`core/database.py`)
Replace `posted_articles.json` with a SQLite database `bot.db`.

**Schema:**
```sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    council_id TEXT NOT NULL,
    title TEXT,
    date TEXT,
    state TEXT NOT NULL,
    first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    posted_at TIMESTAMP
);
```

### 3. Configuration Strategy
Each state directory will have a `config.json`:
```json
{
  "state_code": "VIC",
  "state_name": "Victoria",
  "bluesky_handle": "vic-council-news.bsky.social",
  "bluesky_password_env": "BLUESKY_PASSWORD_VIC",
  "timezone": "Australia/Melbourne"
}
```

### 4. CLI Updates (`main.py`)
The main script will be updated to accept a state argument:
```bash
python main.py --state vic
python main.py --state nsw --dry-run
```

### 5. Action Plan
1.  **Create `core/` module**: Move and refactor `scrapers/base_scraper.py` to `core/scraper.py`. Move `poster.py` to `core/poster.py`.
2.  **Implement `core/database.py`**: Create the SQLite wrapper.
3.  **Migrate Data**: Write a script to convert existing `posted_articles.json` to the new SQLite database.
4.  **Restructure Config**: Create `states/vic/` and move `councils.json` there.
5.  **Rewrite `main.py`**: Implement the new CLI logic and orchestration using the `core` modules.
6.  **Verify**: Run tests to ensure the VIC bot still works as expected.

Shall I proceed with this refactoring plan?