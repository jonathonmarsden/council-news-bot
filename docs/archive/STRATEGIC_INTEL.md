# Strategic Intelligence Report
**Date:** 21 January 2026

This document outlines high-level strategic risks, opportunities, and patterns discovered during the National Health Check.

## 1. System Risks

### The "OpenCities" Dependency
*   **Status**: **42 Councils** (concentrated in NSW/VIC) rely on `opencities_scraper`.
*   **Risk**: High. This is a single point of failure. If the vendor (OpenCities/Granicus) updates their frontend markup globally, ~8% of our national coverage goes dark instantly.
*   **Mitigation**: 
    1. Monitor `opencities_scraper` success rates specifically.
    2. Investigate if OpenCities has a hidden RSS feed or API that is version-agnostic.

## 2. Optimization Opportunities

### The "Hidden WordPress" Fleet
*   **Observation**: Only 11 councils are explicitly configured as `wordpress_scraper`, yet hundreds use generic `card_scraper`.
*   **Intel**: Many `card_scraper` targets show CSS classes like `article.post`, `entry-title`, etc., which are hallmarks of WordPress.
*   **Opportunity**: WordPress sites almost always have `/feed/` available.
*   **Action**: Run `scripts/analysis/find_rss_feeds.py` specifically targeting card-scraper councils to see if we can "downgrade" them to RSS for higher reliability.

### The WA "Vendor Clusters"
The 28 disabled WA councils are not random. They are clustered by CMS vendor:
*   **Alyka / Kentico**: (e.g., Rockingham, Swan, Cambridge). These sites share a common structure. A single `AlykaScraper` could unlock ~10-15 councils.
*   **Sitefinity**: (e.g., South Perth). Requires a dedicated `SitefinityScraper`.

## 3. Specific Hard Targets

### Inverell Shire (NSW)
*   **Issue**: Uses "WPBakery Page Builder" with an AJAX Masonry grid. The news items do not exist in the initial HTML.
*   **Path Forward**: 
    1.  **RSS**: Check `inverell.nsw.gov.au/feed/` (High probability of success).
    2.  **API**: Check Network tab for the admin-ajax.php call returning the grid items.

## 4. Configuration Cleanliness
*   **Typo Fixed**: `states/qld/councils.json` contained a scraper type `html` for Cherbourg. This was identified as a WordPress site and fixed.

