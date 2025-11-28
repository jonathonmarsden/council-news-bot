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
- Owner: Chris Eddy (REDACTED@example.com)

### Post Format (NO EMOJIS EVER)
```
[Title - clickable link]

[Excerpt if available]
[Council Name]
Published: [Date if available]
#LGNewsRoundup #VLGA #VicCouncils #CouncilHashtag
```

## Scraper Architecture

### How the Scraper Works
The `CardScraper` in `scrapers/base_scraper.py` uses a multi-strategy approach:

1. **ARTICLE_SELECTOR** matches container elements on the page
2. **`_parse_article()`** tries multiple strategies in order until one succeeds
3. If no structured elements match, falls back to `_scrape_links_directly()`

### Current Scraper Strategies (in order)
| Strategy | Pattern | Sites | Key Selectors |
|----------|---------|-------|---------------|
| 0 | GovCMS card | Golden Plains, Greater Bendigo | `div.card > a[href*="/news/"] > .card__title h2` |
| 0a | Webflow article-item | East Gippsland | `div.article-item > a.article-link > h4` |
| 0b | Webflow media-item | Wellington | `div.media-item > a.media-link > .media-title` |
| 0c | Shepparton news-item | Greater Shepparton | `article.news-item > a > h1.news-item-heading` |
| 0d | Cardinia listing | Cardinia | `article.listing > a.listing__link > h2.listing__heading` |
| 0e | Clickable card | Various | `a[href] > h2/h3/h4` (whole card is link) |
| 0.5 | GovCMS teaser | Latrobe | `.teaser__title + a.read-more` |
| 1 | Listing pattern | Various | `.listing__heading` with parent `<a>` |
| 2 | Longest link | Fallback | Finds link with longest text |

### ARTICLE_SELECTOR Elements
```css
article.news-item,     /* Shepparton */
article.listing,       /* Cardinia */
.news-card,
.listing-item,
.views-row,
.content-card,
.article-container,
.media-item,           /* Wellington */
a.card--news,
a.card__news-listing,
a.card[href*="/news/"],
div.card,              /* GovCMS/Greater Bendigo */
.article-item          /* East Gippsland */
```

## Troubleshooting Scraper Issues

### Symptom: Title contains date/garbage text
**Cause:** Scraper grabbing full link text instead of specific title element
**Solution:** Add a dedicated strategy that extracts title from the correct nested element

**Diagnostic Steps:**
```bash
# 1. Check what HTML structure the site uses
curl -sL "https://council.vic.gov.au/news" | grep -A20 "article-title-text"

# 2. Test what ARTICLE_SELECTOR matches
python -c "
from scrapers.base_scraper import CardScraper
scraper = CardScraper('council-id', 'Council Name', 'https://council.vic.gov.au/news')
html = scraper.fetch_page(scraper.news_url)
soup = scraper.parse_html(html)
for item in soup.select(scraper.ARTICLE_SELECTOR)[:3]:
    print(f'{item.name}.{item.get(\"class\")}')
"

# 3. If nothing matches, check actual element structure
curl -sL "URL" | grep -E "class=.*(news|article|card|listing)" | head -20
```

### Symptom: Title and excerpt concatenated
**Cause:** Both are inside same `<a>` tag, scraper grabs all text
**Example:** `"Council invites community...From 25 November to 10 December..."`
**Solution:** Add strategy to extract title from specific heading element (h2, h3, etc.)

**Fix Pattern (Cardinia example):**
```python
# Structure: article.listing > a.listing__link > h2.listing__heading + p.listing__summary
if item.name == 'article' and 'listing' in item.get('class', []):
    listing_link = item.select_one('a.listing__link')
    if listing_link:
        url = listing_link.get('href', '')
        title_elem = item.select_one('h2.listing__heading')
        excerpt_elem = item.select_one('p.listing__summary')
        # Extract separately
```

### Symptom: Promotional/static pages being posted
**Cause:** Scraper matching category cards or promo boxes without dates
**Example:** "GB news and magazine", "Your shire and Council news"
**Solution:** Require date element for certain URL patterns

**Filters Added:**
- `/news-and-media/` URLs require a date element (filters promo cards)
- `/news/NNNNN/` URLs without `/article/` are skipped (category pages)

### Symptom: 403 Forbidden errors
**Cause:** WAF (Web Application Firewall) blocking requests
**Solution:** Set `"scraper": "curl_scraper"` in councils.json, may need custom headers

### Adding a New Scraper Strategy
1. Identify the HTML structure with curl/browser dev tools
2. Add container element to `ARTICLE_SELECTOR` if needed
3. Add new strategy block in `_parse_article()` BEFORE generic strategies
4. Strategy must return `self.create_article(title, url, date, excerpt)` or `None`
5. Test with `python main.py --council <id> --dry-run`

## State Management
`data/posted_articles.json` contains:
- `posted_urls`: Already posted to BlueSky
- `known_urls`: Seen in previous scrapes (for priority detection)
- `last_post_time`: Timestamp of last post

**Priority System:** 
1. Newly discovered articles (not in `known_urls`) posted FIRST
2. Then backlog items
3. Round-robin across councils for feed diversity

## Managing Posts

### Delete a BlueSky Post
```python
from atproto import Client
client = Client()
client.login('roundupnewsbot.bsky.social', 'esdi-vwhx-eujl-luk2')
did = client.me.did

# Get post rkey from URL (last part of at:// URI)
rkey = '3m6ojgb4hq625'
client.delete_post(f'at://{did}/app.bsky.feed.post/{rkey}')
```

### Remove URL from Posted History (for reposting)
```python
import json
with open('data/posted_articles.json') as f:
    data = json.load(f)
url = 'https://council.vic.gov.au/news/article/...'
if url in data.get('posted_urls', []):
    data['posted_urls'].remove(url)
with open('data/posted_articles.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### View Recent BlueSky Posts
```python
from atproto import Client
client = Client()
client.login('roundupnewsbot.bsky.social', 'esdi-vwhx-eujl-luk2')
feed = client.get_author_feed(actor='roundupnewsbot.bsky.social', limit=10)
for post in feed.feed:
    text = post.post.record.text[:80].replace('\n', ' ')
    rkey = post.post.uri.split('/')[-1]
    print(f'[{rkey}] {text}...')
```

## GitHub Actions

### Workflow Details
- **File:** `.github/workflows/scrape.yml`
- **Schedule:** Every 5 minutes (temporary) → revert to 15 min
- **Concurrency:** Single run at a time (prevents duplicates)
- **Health monitoring:** Pings healthchecks.io on success/failure
- **Secrets:** `BLUESKY_HANDLE`, `BLUESKY_PASSWORD`, `HEALTHCHECK_URL`

### Check Workflow Status
```bash
gh run list --limit 5
gh run view <run_id> --log
gh run view <run_id> --log-failed
```

### Manual Trigger
```bash
gh workflow run scrape.yml
```

### Git Push Conflicts
The workflow commits state changes. If you push manually during a run:
- The workflow's push will fail with "rejected - fetch first"
- Articles are still posted (just state not saved)
- Next run will have correct state

## Current Settings (TEMPORARY - for backlog clearing)
- Schedule: Every 5 minutes (revert to 15 min)
- Hours: 24/7 (revert to 5am-10pm Melbourne)
- Posts per run: 3 articles (revert to 1)
- Council diversity: Round-robin across councils
- Overnight: Post-only mode (no scraping)

## TODO / Next Session

1. **REVERT TEMPORARY SETTINGS** once backlog cleared
   - Change schedule from `*/5 * * * *` to `0,15,30,45 18-23,0-10 * * *`
   - Change `--limit 3` back to `--limit 1`
   - Re-enable business hours only check

2. **Enable more councils** - 52 still disabled
   - Test WAF-protected councils with curl_scraper
   - Fix URL issues for broken councils

3. **Known Issues:**
   - Merri-bek URL needs update to `/my-council/news-and-publications/news/`
   - Greater Geelong returns 403 (WAF)
   - Latrobe times out occasionally

4. **State expansion potential** - NSW, QLD, SA, WA, TAS, NT, ACT
