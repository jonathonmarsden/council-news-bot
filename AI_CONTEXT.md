# AI Context & Developer Guide

This document is designed to help AI agents and developers understand the Council News Bot architecture, workflows, and common tasks.

## 🏗 Project Structure

The project has evolved from a simple script to a modular, state-based system designed for concurrent execution.

```text
council-news-bot/
├── main.py                 # Core Worker (CLI Entry Point, called by scheduler)
├── scheduler.py            # Main Service Loop (runs continuously)
├── core/                   # Core Application Logic
│   ├── scraper.py          # Scraper implementations (BaseScraper, CardScraper)
│   ├── database.py         # SQLite database handler
│   ├── poster.py           # BlueSky API client
│   └── utils.py            # Logging and utilities
├── states/                 # Configuration by State
│   ├── vic/
│   │   └── councils.json   # VIC Council configurations
│   └── nsw/
│       └── councils.json   # NSW Council configurations
├── scripts/                # Utility scripts
└── bot.db                  # SQLite Database (stores article history)
```

## 🤖 Scraper Architecture

The bot uses a configuration-driven approach. Instead of writing Python code for every council, we define CSS selectors in JSON files.

### `core/scraper.py`

- **`BaseScraper`**: Handles HTTP requests (requests/curl), WAF evasion, and basic parsing.
- **`CardScraper`**: The default scraper. It looks for a list of "cards" or news items. It is highly configurable via JSON.

### Configuration (`states/{state}/councils.json`)

Each council entry looks like this:

```json
{
    "id": "council-id-kebab-case",
    "name": "Council Name",
    "news_url": "https://example.com/news",
    "scraper": "card_scraper",
    "enabled": true,
    "item_selector": "article.news-item",      // CSS selector for the card container
    "title_selector": "h3 a",                  // Selector for title (relative to item)
    "date_selector": "span.date",              // Selector for date (relative to item)
    "link_selector": "self"                    // "self" if the item itself is the link, or a selector
}
```

## 🛠 Workflow: Fixing a Broken Scraper

If a council is not scraping correctly (e.g., finding 0 articles, or missing dates), follow this process:

### 1. Create a Reproduction Script

Create a temporary file (e.g., `test_council.py`) to isolate the council.

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

### 2. Analyze the HTML

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

The bot runs as a systemd service on a DigitalOcean Droplet.

- **Service Name**: `council-news-bot`
- **Logs**: `journalctl -u council-news-bot -f`
- **Restart**: `systemctl restart council-news-bot`

## 🧪 Testing

Run the full test suite:

```bash
pytest
```

Run a specific test file:

```bash
pytest tests/test_scrapers.py
```
