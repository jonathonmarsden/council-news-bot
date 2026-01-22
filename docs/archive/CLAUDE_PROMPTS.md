# CLAUDE.md - Council News Bot

## Project Overview
Automated scraper and BlueSky poster for Australian local government news. Posts to @roundupnewsbot.bsky.social for Chris Eddy's LG News Roundup.
Supports 7 states/territories: VIC, NSW, QLD, TAS, SA, NT, ACT.

## Quick Reference

### Run Commands
```bash
# Activate environment first
source venv/bin/activate

# Run full scrape and post
python main.py

# Dry run (no posting)
python main.py --dry-run

# Post from backlog only (no scraping)
python main.py --post-only

# Scrape specific council
python main.py --council cardinia

# Limit to N posts
python main.py --limit 1

# Test BlueSky connection
python main.py --test

# Run tests
pytest
```

### Project Structure
```text
council-news-bot/
├── main.py              # Entry point, state management, priority queue
├── scheduler.py         # VPS service loop
├── core/                # Core logic (scraper, database, poster)
├── states/              # Config (vic/councils.json, nsw/councils.json, etc.)
└── bot.db               # SQLite database
```

### Key Files
- `main.py` - Orchestration, 7-day freshness filter, priority queue (new articles first)
- `core/scraper.py` - BaseScraper and CardScraper logic
- `states/*/councils.json` - State-specific Council configurations

### BlueSky Credentials
- Handle: `roundupnewsbot.bsky.social`
- App Password: `esdi-vwhx-eujl-luk2`
- Owner: Chris Eddy (lgweeklynews@gmail.com)

### Post Format (NO EMOJIS EVER)
```text
[Title - clickable link]

[Excerpt if available]
[Council Name]
Published: [Date if available]
#LGNewsRoundup #VLGA #VicCouncils #CouncilHashtag
```

## Scraper Architecture

### How the Scraper Works
The `CardScraper` in `core/scraper.py` uses a multi-strategy approach:

1. **Configured Selectors**: Checks `councils.json` for `item_selector`, `title_selector`, etc.
2. **Fallback Strategies**: Tries common patterns (GovCMS, Webflow, etc.) if no config is present.
3. **Direct Link Scraping**: Falls back to finding news-like links on the page.

### Debugging
See `AI_CONTEXT.md` for the "Fixing a Broken Scraper" workflow.
