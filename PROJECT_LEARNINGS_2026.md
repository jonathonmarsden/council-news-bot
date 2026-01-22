# Project Learnings & Strategic Analysis (January 2026)

## 1. National Health Check Findings

A comprehensive audit of all 540 tracked councils was conducted on 22 Jan 2026.

- **Overall Health**: 85.9% (464 councils) successfully returned news articles.
- **Failures**: 0 errors/exceptions. The code is stable.
- **Warnings**: 14.1% (76 councils) returned 0 articles. This is the primary area for improvement.

### Jurisdiction Weaknesses
- **WA** has the lowest success rate (76.1%) among major states. This correlates with the high number of custom/complex scrapers required for WA.
- **NT** is challenging (66.7%), likely due to small councils with infrequent updates or poor web infrastructure.
- **VIC** is the strongest major state (97.5%), suggesting the strategy there (heavy use of `curl_scraper`) is highly effective.

## 2. Technical Architecture & Workflow Comparison

The scraping strategy varies significantly by state, driven by the underlying vendor landscape of council websites.

### Western Australia (The "Catalyst" State)
- **Dominant Tech**: 71% of WA councils use `catalyst_scraper`.
- **Workflow**: Highly specialized. The project detected a common CMS vendor (Catalyst) and built a dedicated scraper, significantly reducing maintenance for ~100 councils.
- **Risk**: High fragmentation in the remaining 30%. Custom scrapers (`belmont`, `wanneroo`, `perth`) are required for specific non-standard sites.

### Victoria (The "Hardened" State)
- **Dominant Tech**: 93% use `curl_scraper`.
- **Workflow**: VIC councils appear to have higher security/bot-protection or use complex SPA frameworks. The workflow defaults to the heavy-duty `curl_cffi` implementation.
- **Learning**: This "sledgehammer" approach works. 97.5% success rate proves that using the robust scraper by default reduces fragility.

### South Australia (The "Simple" State)
- **Dominant Tech**: 97% use `card_scraper`.
- **Workflow**: SA sites are mostly standard HTML. The workflow is lightweight and fast using standard execution.
- **Opportunity**: Minimal maintenance required.

### New South Wales (The "Diverse" State)
- **Dominant Tech**: Mixed. `curl` (46%), `opencities` (21%), `wordpress` (8%).
- **Workflow**: Requires a multi-faceted approach. We successfully identified "OpenCities" as a major platform (similar to Catalyst in WA) and standardizing this was a key win.

## 3. Strategic Recommendations

### A. Standardization of Scraper Types
The success of `catalyst_scraper` (WA) and `opencities_scraper` (NSW) proves that identifying CMS vendors is better than generic scraping.
- **Action**: Analyze the 74 `curl_scrapers` in VIC to see if they share a common CMS (e.g., Squiz Matrix, Drupal) and create a dedicated subclass if beneficial.
- **Action**: Review WA's 33 "Zero Article" councils. Are they broken Catalyst sites? Or custom sites needing fixes?

### B. Adoption of "Curl by Default"
VIC's 97.5% success rate with `curl_scraper` suggests that the performance cost of `curl_cffi` is worth the reliability.
- **Action**: For the 76 councils returning 0 articles, immediate trial of `curl_scraper` (use_curl=True) is the first troubleshooting step.

### C. Zero-News Investigation
The 76 warnings need triage:
1.  **Truly Quiet**: Small shires often post news only on Facebook. (Check Facebook cross-posting feasibility?)
2.  **Broken Selectors**: DOM changes.
3.  **Geo-blocking/Bot-blocking**: Silent failures where 0 items are found.

## 4. Documentation Updates
- `HEALTH_CHECK_REPORT_2026.md` generated with full audit logs.
- `scripts/comprehensive_health_check.py` added to codebase for routine auditing.
- `scripts/analyze_state_scrapers.py` added for architectural visibility.
