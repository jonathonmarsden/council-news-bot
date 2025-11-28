# CLAUDE.md - Council News Bot

## Project Overview
Automated scraper and BlueSky poster for Victorian local government news and media releases. Monitors 79 Victorian councils and posts new articles to BlueSky.

## Quick Reference

### Run Commands
```bash
# Run full scrape and post
python main.py

# Dry run (no posting)
python main.py --dry-run

# Scrape specific council
python main.py --council casey

# Include disabled councils
python main.py --all

# Test BlueSky connection
python main.py --test

# Run tests
pytest
```

### Project Structure
```
council-news-bot/
├── main.py              # Entry point
├── poster.py            # BlueSky posting
├── config/councils.json # Council configuration (79 councils)
├── data/posted_articles.json  # Deduplication tracking
├── scrapers/
│   ├── __init__.py
│   └── base_scraper.py  # BaseScraper, CardScraper, NewsArticle
└── tests/test_scrapers.py
```

### Council Categories
- **Category A (21)**: Direct HTTP access (200 OK) - enabled by default
- **Category B (10)**: Redirect (301) - enabled by default
- **Category C (46)**: WAF protected (403) - disabled, needs curl bypass
- **Category D (2)**: URL issues (404) - disabled, needs investigation

### Adding a New Council
1. Add entry to `config/councils.json`
2. Set `enabled: true` for Category A/B
3. For Category C, set `scraper: "curl_scraper"` and test with `--council <id>`

### Environment Variables
- `BLUESKY_HANDLE`: BlueSky handle (councilnewsbot.bsky.social)
- `BLUESKY_PASSWORD`: BlueSky app password

### BlueSky Account
- Display Name: Council News Bot
- Handle: @councilnewsbot.bsky.social
- Post Format: 📰 [Council Name]: [Title] [URL]

### Related Projects
- council-bot: Meeting documents scraper (14 councils)

### Key Files
- `scrapers/base_scraper.py`: Contains `BaseScraper`, `CardScraper`, `NewsArticle`
- `poster.py`: BlueSky authentication and posting
- `config/councils.json`: All 79 Victorian councils with URLs and settings
