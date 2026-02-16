# AI Context & Developer Guide

This document is designed to help AI agents and developers understand the Council News Bot architecture, workflows, and common tasks.

**Authoritative Sources**: Use docs in `docs/` and root-level guides only. Ignore `docs/archive/` and `_archived_old_code/`.

## 🚀 Deployment Workflow

**The VPS does NOT pull from GitHub automatically.**

We use a **Push-to-Deploy** model using `rsync` via a local script.

👉 **See [docs/DEPLOYMENT.md](DEPLOYMENT.md) for full instructions.**

### Quick Deploy Command
```bash
python3 scripts/deployment/deploy_with_password.py
```

## 🏗 Project Structure

The project is a **Dockerized, VPS-hosted application** designed for concurrent execution.

```text
council-news-bot/
├── main.py                 # Core Worker (CLI Entry Point, called by cron)
├── Dockerfile              # Container definition
├── docker-compose.yml      # Orchestration config (bot + postgres)
├── core/                   # Core Application Logic
│   ├── scrapers/           # Scraper implementations
│   ├── database.py         # PostgreSQL database handler
│   ├── poster.py           # BlueSky API client
│   └── ...
├── states/                 # Configuration by State
│   ├── vic/councils.json   # VIC Council configurations
│   ├── nsw/councils.json   # NSW Council configurations
│   └── ...
├── scripts/                # Utility scripts
│   ├── deployment/         # Deployment scripts (deploy_to_vps.sh, deploy_secrets.py)
│   └── ...
└── docs/                   # Architecture, operations, and runbooks
```
```

## 🤖 Scraper Architecture

The bot uses a configuration-driven approach. We support both HTML scraping and RSS feeds.

### `core/scraper.py`

- **`BaseScraper`**: Handles HTTP requests. Supports `requests` and `curl_cffi` (for WAF bypass).
- **`CardScraper`**: The default HTML scraper. Configurable via CSS selectors in JSON.
- **`RSSScraper`**: The preferred scraper. Consumes standard RSS/Atom feeds.

### Configuration (`states/{state}/councils.json`)

Each council entry looks like this:

```json
{
    "id": "council-id-kebab-case",
    "name": "Council Name",
    "news_url": "https://example.com/rss.xml",
    "scraper": "rss_scraper",  // or "card_scraper"
    "enabled": true
}
```

## 🛠 Workflow: Fixing a Broken Scraper

If a council is not scraping correctly (e.g., finding 0 articles, or missing dates), follow this process:

### 1. Check for RSS First!

Before debugging HTML selectors, check if the council has an RSS feed. This is much more reliable.
- Look for the RSS icon on their news page.
- Check common paths: `/rss`, `/feed`, `/news/rss`, `/news/feed`.
- Use the `scripts/find_rss.py` tool (if available) or just `curl` and `grep`.

If an RSS feed exists, switch the `scraper` type to `rss_scraper` in `councils.json` and update the `news_url`.

### 2. Create a Reproduction Script

If you must use HTML scraping, create a temporary file (e.g., `test_council.py`) to isolate the council.

```python
import sys
import os
import json
from core.scraper import CardScraper

# Mock config
config = {
    "id": "test-council",
    "name": "Test Council",
    "news_url": "https://target-url.com/news",
    "scraper": "card_scraper",
    # Add current selectors from councils.json here
}

def test():
    scraper = CardScraper(
        config['id'], 
        config['name'], 
        config['news_url'], 
        selectors=config
    )
    articles = scraper.scrape()
    print(f"Found {len(articles)} articles")
    for a in articles:
        print(f"- {a.title}\n  Date: {a.date}\n  Link: {a.url}")

if __name__ == "__main__":
    test()
```

### 3. Analyze the HTML

Download the page HTML to inspect the structure. Use `curl` to mimic the bot.

```bash
curl -A "Mozilla/5.0" "https://target-url.com/news" -o debug.html
```

### 3. Identify Selectors

Open `debug.html` or use `grep` to find the article title, date, and container.

- **Container (`item_selector`)**: The element wrapping the whole news card.
- **Date (`date_selector`)**: The element containing the date text.
- **Title (`title_selector`)**: The element containing the headline.

### 4. Update Configuration

Modify `states/{state}/councils.json` with the new selectors.

### 5. Verify

Run your reproduction script again. If it works, delete the script and the HTML file.

## 🚀 Deployment (VPS)

The bot runs as a Docker container on a DigitalOcean Droplet.

### Deployment Script
We use a custom script to handle deployment because we don't have SSH keys set up on the VPS yet (password auth).

```bash
# Deploy code and rebuild containers
python3 scripts/deploy_with_password.py
```

### Manual Management (SSH)
If you need to debug on the server:

1. SSH in: `ssh root@170.64.186.16`
2. View logs: `docker compose logs -f`
3. Restart: `docker compose restart`
4. Rebuild: `docker compose up -d --build`

### Data Persistence
- PostgreSQL data is persisted via the `postgres_data` volume.
- Logs are accessible via `docker compose logs`.

## 🧪 Testing

Run the full test suite:

```bash
pytest
```

Run a specific test file:

```bash
pytest tests/test_scrapers.py
```
