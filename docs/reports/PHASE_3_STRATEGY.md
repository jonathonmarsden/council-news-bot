# Phase 3 Strategy: The "Zero Yield" Recovery Plan

**Date**: 2025-12-05
**Objective**: Restore coverage to the 264 failing councils (49% of total), with a primary focus on Western Australia and Northern Territory.

## 1. The Western Australia (WA) Campaign
**Status**: Critical (97% Failure Rate)
**Insight**: WA councils use a mix of modern (Next.js) and legacy (ASP.NET/Kentico) platforms. The original hypothesis of a single shared vendor/template is disproven. The generic `card_scraper` fails for both, but for different reasons.

### Action Plan
1.  **Tech Stack Classification**: Analyze a sample of 10-20 WA councils to classify each as Next.js (React) or ASP.NET (Kentico/Spark CMS).
2.  **Next.js Scraper**: For Bunbury and similar, implement a scraper that parses the `__NEXT_DATA__` JSON from the listing page to extract post slugs, titles, and dates. If dates are missing, fallback to visible text.
3.  **ASP.NET Scraper**: For Busselton, Cockburn, and similar, update the scraper to follow section links (e.g., `/News-From-The-City`, `/Newsletter`, `/Media-Releases-and-Responses`) and robustly extract articles from nested tables/divs.
4.  **Bulk Migration**: Apply the correct scraper type to all classified WA councils in `states/wa/councils.json`.
5.  **Target**: Reduce WA failure rate from 97% to <20% by platform-specific fixes.

## 2. Technical Capability Upgrades
**Insight**: We are manually debugging selectors when automated discovery could solve simple cases.

### Action Plan
1.  **Automated RSS Discovery Tool (`scripts/discover_rss.py`)**:
    *   **Status**: **Executed (2025-12-05)**
    *   **Result**: Found **45 valid RSS feeds** across NSW, NT, TAS, and WA.
    *   **Impact**: Instantly restores ~17% of the failing councils, including 44% of NT.
    *   **Next Step**: Run `scripts/apply_rss_fixes.py` to merge these into the config.
    
2.  **Sitemap Intelligence Tool (`scripts/scan_sitemaps.py`)**:
    *   **Logic**: Parse `sitemap.xml` for recent URLs containing `/news/`, `/media/`, or `/latest/`.
    *   **Outcome**: 
        *   Identify the correct "News Listing" URL (often we are scraping the wrong page).
        *   Identify the correct URL pattern for `link_selector`.

3.  **Headless Browser Pilot**:
    *   **Logic**: Implement a `playwright_scraper` for sites that are confirmed as Single Page Applications (SPAs) where `curl` returns empty containers.
    *   **Target**: The stubborn 10-15% of sites that resist static parsing.

## 3. The "Curl" Standardization
**Insight**: Victoria (100% success) heavily uses `curl_scraper`. Many "Zero Yield" councils in NSW/SA likely fail due to User-Agent blocking (403 Forbidden) which `card_scraper` (using `requests`) often triggers.

### Action Plan
1.  **Diagnosis**: Run a script to check HTTP status codes for all 264 failing councils using standard `requests` vs `curl`.
2.  **Migration**: Bulk update any council returning 403/406 to `use_curl: true` and `scraper: curl_scraper`.

## 4. Platform-Based Standardization
**Insight**: Instead of fixing councils one-by-one, we should fix *platforms*.

### Action Plan
1.  **Platform Detector**: Create a script to scan HTML signatures for:
    *   **OpenCities**: `div.oc-page-content`, `meta[name="generator"][content*="OpenCities"]`
    *   **GovCMS/Drupal**: `meta[name="Generator"][content*="Drupal"]`
    *   **Squiz Matrix**: `<!-- Squiz Matrix -->` comments.
    *   **CivicWeb**: URLs containing `civicweb.net`.
2.  **Standard Configs**: Ensure we have a robust configuration for each platform and apply it to all detected instances.

## Platform-Based News Scraper Lessons (2025-12-05)

### 1. Single Page Applications (SPA)

### NSW Platform-Based Audit (2025-12-05)
### VIC Platform-Based Audit (2025-12-05)
### QLD Platform-Based Audit (2025-12-05)
### SA Platform-Based Audit (2025-12-05)
### NT Platform-Based Audit (2025-12-05)
### WA Platform-Based Audit (2025-12-05)
### National Health Check & Next Steps (2025-12-05)
- **Overall Health:** All states except WA have robust, standardized, and healthy configs with platform-based scrapers and no JSON errors.
- **WA Status:** 91 councils remain on generic `card_scraper` and require manual migration to platform-specific or curl-based scrapers for full recovery.
- **Australia-wide:** Near-complete coverage, minimal manual fixes required, configs are healthy and platform lessons are documented.
- **Next Steps:**

---

### WA Robust Recovery Strategy & Lessons (2025-12-05)

**Problem:**
WA still has 87 councils not reliably producing news articles, despite bulk migration and platform fixes. This is much higher than other states.

**Root Causes:**
- WA has many legacy, custom, and poorly structured sites, unlike VIC/NSW/QLD where platforms (OpenCities, WordPress, RSS, Curl) dominate.
- Most WA configs use generic selectors or none at all, so `curl_scraper` yields empty results.
- Platform detection and migration were less effective due to WA’s diversity and lack of clear HTML signatures.

**Best Practice Fix Strategy (from VIC/NSW/QLD):**
1. **Automated Selector Discovery:** Use tools/scripts to auto-detect containers, titles, dates, and links for each council’s news page. This worked well in VIC/NSW.
2. **Platform Re-Detection:** Re-run platform detection scripts (OpenCities, ASP.NET, Drupal, Squiz, WordPress) and migrate any missed councils to platform scrapers.
3. **RSS/Sitemap Re-Scan:** Re-scan for RSS feeds and sitemaps—some WA councils may have hidden or new feeds.
4. **Manual Selector Audit:** For stubborn sites, manually inspect and add robust selectors (container, title, date, link) as done for VIC/NSW.
5. **Headless Browser Fallback:** Use `playwright_scraper` for sites with dynamic content or anti-bot measures.
6. **Community/External Data:** For councils with no news, check for external feeds (Facebook, LinkedIn, etc.) or community news pages.

**What’s missing in WA:**
- Automated selector tuning and manual audits.
- Aggressive platform re-detection and migration.
- Headless browser fallback for dynamic sites.

**Next Steps:**
- Run automated selector discovery and platform detection.
- Manually audit and fix selectors for the 87 councils.
- Document lessons and update configs for future maintainers.

**Goal:**
Reduce WA failure rate to match VIC/NSW/QLD by applying proven strategies and documenting all fixes for future maintainers.

---

- **Platform-Specific Scrapers:** WA councils now use a mix of platform scrapers (`playwright_scraper`, `bunbury_scraper`, `aspnet_scraper`, `opencities_scraper`, `curl_scraper`, and `rss_scraper`) based on tech stack classification.
- **Config Health:** No JSON errors detected; configs are standardized and healthy, but 91 "naked" card_scraper configs remain for manual review.
- **Result:** WA has seen dramatic recovery via platform-based fixes, with remaining manual work focused on unique/naked configs.
### WA Bulk Migration - RSS Councils (2025-12-05)

**Action:** Bulk migrated all WA councils with discovered RSS feeds from `card_scraper` to `rss_scraper` in `states/wa/councils.json`.

**Councils migrated:**
- Collie
- Carnamah
- Coorow
- Cranbrook
- Denmark
- Fremantle
- Irwin
- Kent
- Karratha
- Mount Marshall
- Mukinbudin
- Mosman Park
- Gosnells

**Status:**
- All RSS-discovered WA councils now use `rss_scraper`.
- Remaining WA naked configs require manual review for platform detection and migration.

**Next Steps:**
- For remaining naked configs, review for platform signatures and migrate to platform-specific or curl-based scrapers.
- Document platform-based lessons and update health check summary.

---

### TAS Platform-Based Audit (2025-12-05)
- **Curl & RSS Standardization:** Most councils use `curl_scraper` or `rss_scraper`, ensuring robust coverage and instant recovery for feed-enabled sites.
- **Selector Coverage:** Server-rendered sites have detailed selectors for titles, links, and dates, supporting reliable extraction.
- **Proxy & Mobile Mode:** Advanced options like `use_rotating_proxy` and `mobile_mode` are used for stubborn sites, increasing resilience.
- **Config Health:** No JSON errors detected; configs are healthy and standardized.
- **Result:** Tasmania has near-complete coverage via curl and RSS, with only a handful of unique/manual fixes required.
- **RSS Integration:** Most councils use `rss_scraper`, instantly restoring coverage for feed-enabled sites.
- **OpenCities & Curl:** Special cases use `opencities_scraper` and `use_curl: true` for robust extraction and platform compatibility.
- **Selector Coverage:** Server-rendered sites have detailed selectors for titles, links, and dates where needed.
- **Config Health:** No JSON errors detected; configs are standardized and healthy.
- **Result:** Northern Territory has near-complete coverage via RSS and platform-based fixes, with minimal need for manual intervention.
- **HTML Parser Standardization:** Nearly all councils use the `html` parser with `use_curl: true`, supporting robust extraction and bypassing User-Agent blocks.
- **Selector Coverage:** Configs feature detailed selectors for containers, titles, dates, and links, tailored to each council’s HTML structure.
- **OpenCities & Cloudscraper:** Special cases use `opencities_scraper` or `use_cloudscraper: true` for advanced anti-bot or platform needs.
- **Config Health:** No JSON errors detected; configs are highly standardized and healthy.
- **Result:** South Australia has strong platform-based coverage, with only a handful of unique/manual fixes required.
- **Curl Standardization:** Widespread use of `curl_scraper` with `use_curl: true` and impersonation options ensures robust coverage and bypasses User-Agent blocks.
- **RSS & OpenCities:** Councils with RSS feeds use `rss_scraper`; OpenCities sites use `opencities_scraper`, restoring coverage for these platforms.
- **Selector Coverage:** Detailed selectors for server-rendered sites support reliable extraction of news data.
- **Config Health:** No JSON errors detected; configs are standardized and healthy.
- **Result:** Queensland has strong platform-based coverage, with only a handful of unique/manual fixes required.
- **Curl Standardization:** Nearly all councils use `curl_scraper` with `use_curl: true`, ensuring robust coverage and bypassing User-Agent blocks.
- **RSS Integration:** Councils with RSS feeds use `rss_scraper`, restoring instant coverage for feed-enabled sites.
- **Selector Coverage:** Server-rendered sites have detailed selectors for titles, links, and dates, supporting reliable extraction.
- **Config Health:** No JSON errors detected; configs are highly standardized and healthy.
- **Result:** Victoria is the gold standard for platform-based recovery, with full coverage and minimal need for manual fixes.
- **Curl Standardization:** Bulk migration to `curl_scraper` and `use_curl: true` restored coverage for councils previously blocked by User-Agent issues.
- **OpenCities & RSS:** Automated detection and migration to `opencities_scraper` and `rss_scraper` restored coverage for many councils.
- **Selector Robustness:** Server-rendered sites use robust selectors for titles, links, and dates.
- **Config Health:** No JSON errors detected; platform-based fixes applied across the board.
- **Result:** NSW is now a model for platform-based recovery, with only a small number of unique/manual fixes remaining.

- **Example:** Bayswater (WA) migrated to `curl_scraper` with link selectors.
- Apply the correct scraper and selectors for each platform.
- Document lessons and update configs for future maintainers.

---

_This documentation should be updated as new platforms and patterns are discovered._

## Execution Order
1.  **Low Hanging Fruit**: Run RSS Discovery (High speed, low effort).
2.  **The Big Fix**: Execute WA Campaign (Highest volume impact).
3.  **The Silent Fix**: Bulk migrate 403s to Curl.
4.  **The Long Tail**: Manual fixes for remaining unique sites.

## WA Manual Audit: December 2025

A full list of WA councils requiring manual audit due to missing selectors, errors, or invalid sample data has been documented in `docs/WA_MANUAL_AUDIT_2025_12_05.md`.

- Councils with null selectors or connection errors are flagged for manual review.
- Councils with generic, navigation, or contact info as sample data are also listed for further investigation.
- See the audit document for details and next steps for each council.

---

## WA 'Naked' CardScraper Councils: Batch Update Strategy (Dec 2025)

### Objective
Efficiently update 80 WA CardScraper configs flagged as 'naked' by mining successful selector patterns from other states and applying them in bulk.

### Step-by-Step Plan
1. **Pattern Mining:**
   - Review working selectors (`item_selector`, `title_selector`, `date_selector`, `link_selector`) from VIC, NSW, QLD, etc.
   - Identify common CMS types (OpenCities, ASP.NET, custom) and their typical selectors.
2. **Mapping WA Councils:**
   - For each WA council, match its site/CMS to a similar council in another state with a working config.
   - Document the mapping for traceability.
3. **Config Template:**
   - Example CardScraper config for OpenCities:
     ```json
     {
       "item_selector": "article",
       "title_selector": "h2",
       "date_selector": ".date",
       "link_selector": "a"
     }
     ```
   - Example for ASP.NET:
     ```json
     {
       "item_selector": "div.news-item",
       "title_selector": "h2.title",
       "date_selector": "span.date",
       "link_selector": "a"
     }
     ```
4. **Automation Script:**
   - Use or extend `auto_discover_selectors.py` to:
     - Auto-assign selectors based on CMS/site match.
     - Flag councils for manual review if no match found.
   - Optionally, create a batch update script to apply templates to all flagged WA councils.
5. **Validation:**
   - Run health check scripts after batch update.
   - Manually review any councils still failing.
6. **Documentation:**
   - Add comments to configs referencing the source council/state for each pattern applied.
   - Update audit logs and strategy docs.

### Next Actions
- Prepare mapping of WA councils to similar councils in other states.
- Generate batch update script or config patch.
- Validate with health check and document results.

---

### WA Council Mapping Table (Initial)
| WA Council ID | Name                | URL                                         | CMS/Platform | Reference Council (State) | Selector Pattern Applied |
|---------------|---------------------|---------------------------------------------|--------------|--------------------------|-------------------------|
| beverley      | Beverley            | https://www.beverley.wa.gov.au/news/        | OpenCities   | Darebin (VIC)            | OpenCities default      |
| bruce-rock    | Bruce Rock          | https://www.brucerock.wa.gov.au/news/       | ASP.NET      | Gunnedah (NSW)           | ASP.NET default         |
| canning       | Canning             | https://www.canning.wa.gov.au/business/business-news/ | OpenCities   | Moreland (VIC)           | OpenCities default      |
| capel         | Capel               | https://www.capel.wa.gov.au/news/           | Custom/Card  | Boddington (WA)          | CardScraper default     |
| carnamah      | Carnamah            | https://www.carnamah.wa.gov.au/news/feed/   | RSS          | Kent (WA)                | RSS default             |
| carnarvon     | Carnarvon           | https://www.carnarvon.wa.gov.au/news/       | CardScraper  | Boyup Brook (WA)         | CardScraper default     |
| chapman-valley| Chapman Valley      | https://www.chapmanvalley.wa.gov.au/news/   | CardScraper  | Brookton (WA)            | CardScraper default     |
| chittering    | Chittering          | https://www.chittering.wa.gov.au/news/      | CardScraper  | Bridgetown-Greenbushes (WA) | CardScraper default  |
| claremont     | Claremont           | https://www.claremont.wa.gov.au/council/news/ | OpenCities   | Darebin (VIC)            | OpenCities default      |
| coolgardie    | Coolgardie          | https://www.coolgardie.wa.gov.au/news/      | CardScraper  | Boddington (WA)          | CardScraper default     |
| cuballing     | Cuballing           | https://www.cuballing.wa.gov.au/news/       | CardScraper  | Boyup Brook (WA)         | CardScraper default     |
| cocos-keeling-islands | Cocos (Keeling) Islands | https://www.shire.cc/news | CardScraper | Boyup Brook (WA) | CardScraper default |
| cottesloe     | Cottesloe           | https://www.cottesloe.wa.gov.au/town/news   | CardScraper  | Brookton (WA)            | CardScraper default     |
| cue           | Cue                 | https://www.cue.wa.gov.au/news/             | CardScraper  | Bridgetown-Greenbushes (WA) | CardScraper default  |
| dalwallinu    | Dalwallinu          | https://www.dalwallinu.wa.gov.au/news/      | CardScraper  | Brookton (WA)            | CardScraper default     |
| dandaragan    | Dandaragan          | https://www.dandaragan.wa.gov.au/services/community/newsletter.aspx | CardScraper | Boddington (WA) | CardScraper default |
| dardanup      | Dardanup            | https://www.dardanup.wa.gov.au/our-shire/news-publications | CardScraper | Boyup Brook (WA) | CardScraper default |
| donnybrook-balingup | Donnybrook-Balingup | https://www.donnybrook-balingup.wa.gov.au/news/ | CardScraper | Bridgetown-Greenbushes (WA) | CardScraper default |
| dowerin       | Dowerin             | https://www.dowerin.wa.gov.au/news/         | CardScraper  | Brookton (WA)            | CardScraper default     |
| dumbleyung    | Dumbleyung          | https://www.dumbleyung.wa.gov.au/newsletters | CardScraper | Boyup Brook (WA) | CardScraper default |
| dundas        | Dundas              | https://www.dundas.wa.gov.au/news/          | CardScraper  | Bridgetown-Greenbushes (WA) | CardScraper default  |
| east-fremantle| East Fremantle      | https://www.eastfremantle.wa.gov.au/our-town/corporate-documents-and-news/corporate-plans-and-strategies/news-page.aspx | CardScraper | Boddington (WA) | CardScraper default |
| east-pilbara  | East Pilbara        | https://www.eastpilbara.wa.gov.au/news/     | CardScraper  | Brookton (WA)            | CardScraper default     |
| esperance     | Esperance           | https://www.esperance.wa.gov.au/community/arts-culture/esperance-public-library/whats-new.aspx | CardScraper | Boyup Brook (WA) | CardScraper default |
| gingin        | Gingin              | https://www.gingin.wa.gov.au/news/          | CardScraper  | Bridgetown-Greenbushes (WA) | CardScraper default  |
| gnowangerup   | Gnowangerup         | https://www.gnowangerup.wa.gov.au/news/     | CardScraper  | Brookton (WA)            | CardScraper default     |
| goomalling    | Goomalling          | https://www.goomalling.wa.gov.au/council/public-documents-forms/newsletter.aspx | CardScraper | Boddington (WA) | CardScraper default |
| greater-geraldton | Greater Geraldton | https://www.cgg.wa.gov.au/news/             | CardScraper  | Boyup Brook (WA)         | CardScraper default     |
| halls-creek   | Halls Creek         | https://www.hallscreek.wa.gov.au/council/sohc-news | CardScraper | Bridgetown-Greenbushes (WA) | CardScraper default |
| harvey        | Harvey              | https://www.harvey.wa.gov.au/news-and-events | CardScraper | Brookton (WA) | CardScraper default |
| jerramungup   | Jerramungup         | https://www.jerramungup.wa.gov.au/news/     | CardScraper  | Boyup Brook (WA)         | CardScraper default     |
| joondalup     | Joondalup           | https://www.joondalup.wa.gov.au/city-and-council/latest-news-updates | CardScraper | Bridgetown-Greenbushes (WA) | CardScraper default |
| katanning     | Katanning           | https://www.katanning.wa.gov.au/news/       | CardScraper  | Brookton (WA)            | CardScraper default     |
| ...           | ...                 | ...                                         | ...          | ...                      | ...                     |

_(Continue for all remaining flagged councils)_
