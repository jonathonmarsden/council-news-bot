# Victorian Council News Pages - Survey Results

**Survey Date:** November 28, 2025
**Total Councils:** 79

## Summary

| HTTP Status | Count | Description |
|-------------|-------|-------------|
| 200 OK | 21 | Direct access - easiest to scrape |
| 301 Redirect | 10 | Redirects to actual page - usually accessible |
| 403 Forbidden | 46 | WAF/bot protection - needs curl bypass or headers |
| 404 Not Found | 2 | URL incorrect or page moved |

## Accessibility Categories

### ✅ Category A: Direct Access (200 OK) - 21 Councils
These councils can be scraped with simple HTTP requests:

1. Ballarat - https://www.ballarat.vic.gov.au/news
2. Bass Coast - https://www.basscoast.vic.gov.au/about-council/news-listing
3. Bayside - https://www.bayside.vic.gov.au/news
4. Benalla - https://www.benalla.vic.gov.au/latest-news/
5. Buloke - https://www.buloke.vic.gov.au/news-and-consultation
6. Cardinia - https://www.cardinia.vic.gov.au/news
7. Casey - https://www.casey.vic.gov.au/news
8. East Gippsland - https://www.eastgippsland.vic.gov.au/council/media-releases
9. Glen Eira - https://www.gleneira.vic.gov.au/about-council/news/latest-news
10. Golden Plains - https://www.goldenplains.vic.gov.au/news
11. Greater Geelong - https://www.geelongaustralia.com.au/news/default.aspx
12. Greater Shepparton - https://greatershepparton.com.au/whats-happening/news
13. Latrobe - https://www.latrobe.vic.gov.au/Council/Media_and_Publications/Latest_News
14. Merri-bek - https://www.merri-bek.vic.gov.au/my-council/news-and-publications/news/
15. South Gippsland - https://www.southgippsland.vic.gov.au/news
16. Strathbogie - https://www.strathbogie.vic.gov.au/
17. Towong - https://www.towong.vic.gov.au/1-council/news-and-media/media-releases
18. Wellington - https://www.wellington.vic.gov.au/council/media-releases
19. Whitehorse - https://www.whitehorse.vic.gov.au/news-and-media
20. Wodonga - https://www.wodonga.vic.gov.au/Newsroom/Archive
21. Wyndham - https://www.wyndham.vic.gov.au/news?service-area=All&media-release=1

### 🔄 Category B: Redirects (301) - 10 Councils
These councils redirect to the actual page, usually accessible:

1. Ararat Rural - https://www.ararat.vic.gov.au/news/
2. Boroondara - https://www.boroondara.vic.gov.au/about-council/news-and-media/boroondara-news
3. Brimbank - https://www.brimbank.vic.gov.au/news-and-events/media-releases
4. Greater Bendigo - https://www.bendigo.vic.gov.au/About/Media-Releases
5. Greater Dandenong - https://www.greaterdandenong.vic.gov.au/contact-us/news-and-media
6. Knox - https://www.knox.vic.gov.au/news
7. Manningham - https://www.manningham.vic.gov.au/news-centre
8. Melbourne - https://news.melbourne.vic.gov.au/media-centre/
9. Mitchell - https://www.mitchellshire.vic.gov.au/about-council/news-and-media/news-archive
10. Moonee Valley - https://mvcc.vic.gov.au/play/my-week/news/

### 🛡️ Category C: WAF Protected (403) - 46 Councils
These councils have bot protection and need curl bypass or browser headers:

Banyule, Baw Baw, Campaspe, Central Goldfields, Colac Otway, Corangamite, Darebin, 
Frankston, Gannawarra, Glenelg, Hepburn, Hindmarsh, Hobsons Bay, Horsham, Hume, 
Indigo, Kingston, Loddon, Macedon Ranges, Mansfield, Maribyrnong, Maroondah, 
Melton, Mildura, Moira, Monash, Moorabool, Mornington Peninsula, Mount Alexander, 
Moyne, Murrindindi, Nillumbik, Northern Grampians, Pyrenees, Queenscliffe, 
Southern Grampians, Stonnington, Surf Coast, Swan Hill, Wangaratta, Warrnambool, 
West Wimmera, Whittlesea, Yarra, Yarra Ranges, Yarriambiack

### ❌ Category D: Not Found (404) - 2 Councils
URL may be incorrect or page has moved:

1. Alpine Shire - https://www.alpineshire.vic.gov.au/news- (trailing hyphen issue)
2. Port Phillip - https://www.portphillip.vic.gov.au/about-the-council/news-and-media

## Page Structure Analysis

Based on sampling accessible councils, common patterns identified:

### Pattern 1: HTML Card Layout (Most Common)
- News items displayed as cards with headline, date, excerpt
- Links follow pattern: `/news/article-slug` or `/news-and-media/article-title`
- Pagination via `?page=N` query parameter
- **Examples:** Casey, Wyndham, Ballarat, Whitehorse, Glen Eira

### Pattern 2: Simple List Layout
- News items as simple list with title and date
- Links follow various patterns
- **Examples:** Towong, Wellington, East Gippsland

### Pattern 3: ASP.NET Sites
- Different URL structure using .aspx pages
- May require different parsing approach
- **Examples:** Greater Geelong

## Common HTML Structures

### News Article Card (typical)
```html
<article class="news-item">
  <h3><a href="/news/article-slug">Article Title</a></h3>
  <span class="date">28 Nov 2025</span>
  <p class="excerpt">Brief summary of the article...</p>
</article>
```

### Date Formats Observed
- "28 Nov 2025" (most common)
- "Thu 28 Nov 2025"
- "28 November 2025"
- "Published 28 Nov 2025"
- "Updated Wed 26 Nov 2025"

## Recommended Implementation Strategy

### Phase 1: Start with Category A (21 councils)
Focus on 200 OK councils first - no WAF bypass needed

### Phase 2: Add Category B (10 councils)
Follow redirects to get actual content

### Phase 3: Add Category C with curl bypass (46 councils)
Use the same curl bypass pattern we developed for Stonnington in council-bot

### Phase 4: Investigate Category D (2 councils)
- Alpine Shire: Try https://www.alpineshire.vic.gov.au/news
- Port Phillip: Search for actual news page URL

## Scraper Template Selection

Based on patterns, we can reuse:
1. **base_scraper.py** - Core HTTP fetching, HTML parsing
2. **glen_eira.py** - Two-step card-based scraper (works for most)
3. **stonnington.py** - curl bypass for WAF-protected sites

## Content Types Expected

From council-bot experience and news page sampling:
- Media releases
- Council news/updates
- Community announcements
- Event notices
- Public consultations
- Infrastructure updates
- Service changes
- Emergency/disaster information

## Deduplication Strategy

Each news item needs unique identifier:
- Option A: Full URL as ID
- Option B: Hash of title + date + council
- Option C: Council prefix + article slug

**Recommended:** Full URL as unique identifier (simplest and most reliable)

## Next Steps

1. Create project structure mirroring council-bot
2. Implement base news scraper class
3. Build scrapers for 10 representative councils from Category A
4. Test deduplication and BlueSky posting
5. Expand to remaining councils
