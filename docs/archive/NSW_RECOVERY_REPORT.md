# NSW Recovery Report (2026-01-24)

## Summary
A targeted campaign was run to fix "Silent Failures" in NSW. These were councils where the scraper ran successfully (Status 200) but returned **0 articles**. This usually indicates a broken selector, a layout change (e.g., empty view), or a CMS migration.

**Total Fixed:** 11/11
**Strategy**:
1.  **Selector Hardening**: Updates to `councils.json` for new CMS layouts (OpenCities, generic templates).
2.  **Strategy Pivot**: Switching to PDF Newsletter lists when HTML news feeds are deprioritized or broken by the council.
3.  **Code Enhancements**: Updating `core/scrapers/card.py` to support `self` selectors for direct link lists.

## Fixed Councils

| Council | Issue | Resolution | Scraper Type |
| :--- | :--- | :--- | :--- |
| **Bogan Shire Council** | 0 Articles | Switched to RSS Feed | `rss_scraper` |
| **Lake Macquarie City Council** | 0 Articles | Updated selectors for new layout | `card_scraper` |
| **Wollondilly Shire Council** | 0 Articles | Updated selectors for new layout | `card_scraper` |
| **Snowy Valleys Council** | 0 Articles | Updated selectors for new layout | `card_scraper` |
| **Lithgow City Council** | 0 Articles | Updated selectors for new layout | `card_scraper` |
| **Murray River Council** | 0 Articles | Fixed `opencities_scraper` config | `opencities_scraper` |
| **Murrumbidgee Council** | 0 Articles | Fixed `opencities_scraper` config | `opencities_scraper` |
| **Narrandera Shire Council** | 0 Articles | Fixed `opencities_scraper` config | `opencities_scraper` |
| **Shellharbour City Council** | 0 Articles | Updated selectors for new layout | `card_scraper` |
| **Upper Lachlan Shire Council** | 0 Articles | Fixed `wordpress_scraper` config | `wordpress_scraper` |
| **Lockhart Shire Council** | 0 Articles | **Pivoted to Newsletter PDFs**. News feed page was empty/broken. | `card_scraper` (Updated) |

## Key Learnings

### 1. The "Newsletter Pivot"
For small councils (like Lockhart), the "Latest News" section is often abandoned in favor of a monthly PDF newsletter. 
- **Old Strategy**: Try to scrape a stagnant HTML news feed.
- **New Strategy**: Scrape the "Newsletters" page.
- **Tech Upgrade**: `CardScraper` now supports `title_selector: "self"` to handle lists of PDF links like `<a href="file.pdf">January 2026</a>` where the title is the link text itself.

### 2. OpenCities Fragility
Several NSW councils use OpenCities but had slight variations in their listing selectors. Hardening the `opencities_scraper` or falling back to `card_scraper` with precise selectors (`article`, `.list-item-container`) proved effective.
