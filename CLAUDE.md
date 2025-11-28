# CLAUDE.md - Council News Bot

## Project Overview
Automated scraper and BlueSky poster for Victorian local government news. Posts to @roundupnewsbot.bsky.social for Chris Eddy's LG News Roundup.

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
```
council-news-bot/
├── main.py              # Entry point, state management, priority queue
├── poster.py            # BlueSky posting with facets for clickable links
├── config/councils.json # 79 councils configured, 27 enabled
├── data/posted_articles.json  # State: posted_urls, known_urls, last_post_time
├── scrapers/
│   ├── __init__.py
│   └── base_scraper.py  # BaseScraper, CardScraper, NewsArticle
└── tests/test_scrapers.py
```

### Key Files
- `main.py` - Orchestration, 7-day freshness filter, priority queue (new articles first)
- `poster.py` - BlueSky facets for clickable titles, hashtag formatting
- `scrapers/base_scraper.py` - Multiple parsing strategies for different HTML layouts
- `config/councils.json` - Council URLs, enabled status, scraper type
- `.github/workflows/scrape.yml` - GitHub Actions (every 5 mins, concurrency control)

### BlueSky Credentials
- Handle: `roundupnewsbot.bsky.social`
- App Password: `esdi-vwhx-eujl-luk2`
- Owner: Chris Eddy (lgweeklynews@gmail.com)

### Post Format (NO EMOJIS EVER)
```
[Title - clickable link]

[Excerpt if available]
[Council Name]
Published: [Date if available]
#LGNewsRoundup #VLGA #VicCouncils #CouncilHashtag
```

### State Management
`data/posted_articles.json` contains:
- `posted_urls`: Already posted to BlueSky
- `known_urls`: Seen in previous scrapes (for priority detection)
- `last_post_time`: Timestamp of last post

**Priority System:** 
1. Newly discovered articles (not in `known_urls`) posted FIRST
2. Then backlog items
3. Round-robin across councils for feed diversity

### Current Settings (TEMPORARY - for backlog clearing)
- Schedule: Every 5 minutes (revert to 15 min)
- Hours: 24/7 (revert to 5am-10pm Melbourne)
- Posts per run: 3 articles (revert to 1)
- Council diversity: Round-robin across councils
- Overnight: Post-only mode (no scraping)
- Health monitoring: Healthchecks.io alerts if workflow stops

### Council Categories
- **Enabled (27)**: Direct HTTP access, working scrapers
- **WAF Protected (46)**: 403 errors, need curl bypass
- **URL Issues (2)**: 404 errors, need investigation

### Adding a New Council
1. Add entry to `config/councils.json`
2. Set `enabled: true`
3. For WAF sites, set `scraper: "curl_scraper"`
4. Test with `python main.py --council <id> --dry-run`

### GitHub Actions Workflow
- Runs on schedule + manual dispatch
- Concurrency control prevents duplicate posts
- Commits state changes back to repo
- Secrets: `BLUESKY_HANDLE`, `BLUESKY_PASSWORD`, `HEALTHCHECK_URL`
- Health monitoring: Pings healthchecks.io on success/failure
- Alert if no ping received within 15 minutes (5 min period + 10 min grace)

### Common Issues
1. **Title/excerpt merged**: Check scraper parsing - some sites wrap both in one `<a>` tag
2. **Duplicate posts**: Race condition - concurrency control added
3. **Missing dates**: Many councils don't include dates - we omit "Published:" line
4. **WAF blocked**: Use curl_scraper, may need custom headers

### Delete a Post
```python
from atproto import Client
client = Client()
client.login('roundupnewsbot.bsky.social', 'esdi-vwhx-eujl-luk2')
client.delete_post("at://did:plc:.../app.bsky.feed.post/...")
```

### Related Projects
- `council-bot` - Meeting documents bot (separate project)

## TODO / Next Session

1. **REVERT TEMPORARY SETTINGS** once backlog cleared (~530 articles at ~10/hour = ~53 hours)
   - Change schedule from `*/5 * * * *` to `0,15,30,45 18-23,0-10 * * *`
   - Change `--limit 3` back to `--limit 1`
   - Re-enable business hours only check
   - Remove `--post-only` overnight mode
   - Keep council diversity (round-robin) - it's a good feature

2. **Enable more councils** - 52 still disabled
   - Test WAF-protected councils with curl_scraper
   - Fix URL issues for 2 councils

3. **State expansion** - Potential to expand to NSW, QLD, SA, WA, TAS, NT, ACT
   - Hashtag format: `#LGNewsRoundup #[StateLGA] #[StateCouncils] #[CouncilName]`
   - BlueSky accounts: `roundupnewsbotnsw.bsky.social`, etc.
   - Email aliases: `lgweeklynews+nsw@gmail.com`, etc.

4. **Improve date parsing** - 74% of articles lack dates
   - Hashtag format: `#LGNewsRoundup #[StateLGA] #[StateCouncils] #[CouncilName]`
   - BlueSky accounts: `roundupnewsbotnsw.bsky.social`, etc.
   - Email aliases: `lgweeklynews+nsw@gmail.com`, etc.

4. **Improve date parsing** - 74% of articles lack dates
