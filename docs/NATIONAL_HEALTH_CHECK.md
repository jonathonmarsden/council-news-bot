# National Health Check & Strategy Report
**Date:** 21 January 2026

## 1. National Coverage Status

| State | Total | Enabled | % Live | Primary Tech | Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ACT** | 1 | 1 | **100%** | RSS | Low |
| **NSW** | 128 | 127 | **99%** | Custom (OpenCities) + Card | High (Many vendors) |
| **NT** | 18 | 18 | **100%** | Card + RSS | Medium |
| **QLD** | 78 | 78 | **100%** | Card (WAF) | Medium |
| **SA** | 69 | 69 | **100%** | Card (WAF) | Medium |
| **TAS** | 29 | 29 | **100%** | Card | Low |
| **VIC** | 79 | 79 | **100%** | Card (WAF heavy) | Low (Standardized) |
| **WA** | 138 | 110 | **80%** | Catalyst (Templated) | High (Bimodal: Tiny Shires vs Giant Cities) |
| **Total** | **540** | **511** | **95%** | | |

## 2. Technical Approach by State

*   **VIC & SA (The "WAF States")**: highly standardized scraping using `card_scraper` reinforced with `curl_cffi` to beat Cloudflare.
*   **WA (The "Catalyst State")**: 110+ small shires use a single CMS (Catalyst). We recently deployed `CatalystScraper` to handle 99 of them efficiently.
*   **NSW (The "Custom State")**: Fragmented ecosystem. High reliance on `OpenCitiesScraper` and other custom solutions due to complex CMSs.
*   **QLD/NT/TAS**: Standard mix.

## 3. Discrepancy Report

The `README.md` claims **99.8% coverage**, but actual coverage is **94.6%** (511/540). 
The gap is entirely in **Western Australia** (28 disabled councils).

### Critical Gaps (WA)
These major councils are currently disabled:
1.  **City of Albany** (Pending Fix)
2.  **City of Belmont** (Phase 3: Custom)
3.  **City of Cockburn** (ASP.NET)
4.  **City of Rockingham** (Alyka/Kentico)
5.  **City of South Perth** (Sitefinity)
6.  **City of Swan** (Alyka/Kentico)

## 4. Recommendations
1.  **Immediate:** Update README statistics to be accurate (95%).
2.  **High Priority:** Develop `AlykaScraper` for WA councils (Rockingham, Swan).
3.  **High Priority:** Develop `SitefinityScraper` for South Perth.
4.  **Maintenance:** Audit the "Temporarily Disabled" WA shires to see if they fit the `CatalystScraper` pattern (e.g. Shire of Mingenew).
