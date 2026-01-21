# Post-Mortem Analysis of Council Scraper Success (NSW vs WA)

## 1. The Strategy Gap
Comparing the successful NSW configuration (127/128 online) with the struggling WA configuration (online count improving) reveals a distinct difference in strategy:

| Feature | NSW (Success) | WA (Failure) |
| :--- | :--- | :--- |
| **Abstraction** | Heavy use of Classes (`OpenCitiesScraper`, `WordPressScraper`) | Heavy use of raw CSS selectors (`card_scraper`) |
| **Maintenance** | Single point of fix (update the Class) | 100 points of fix (update every JSON entry) |
| **Resilience** | `curl_scraper` (50% of councils) | `card_scraper` (77% of councils) without `curl` |

## 2. WA "Catalyst" Pattern Discovery
A manual review of WA URLs reveals a massive cluster of identical websites (e.g., Ashburton, Beverley, Boddington).
These need a dedicated `CatalystScraper` class.

## 3. The Recovery Plan

### Phase 1: Immediate Wins (Completed 2026-01-21)
- [x] **Goal:** Enable reliable data sources (RSS, APIs)
- [x] **Councils:** Fremantle, Bunbury, Denmark, Gosnells
- [x] **Status:** **DEPLOYED & ACTIVE**

### Phase 2: The "OpenCities" Migration (Completed 2026-01-21)
- [x] **Goal:** Validate and migrate purported OpenCities sites.
- [x] **Success:**
    - **Canning**: Migrated to `opencities_scraper`. Fixed class to handle JSON-in-script data.
    - **Stirling**: Migrated to `stirling_scraper` (Custom API). Refactored config.
- [x] **Findings:**
    - Many sites labeled as OpenCities are actually **Sitefinity** or **Alyka/Kentico** custom builds.
    - **Swan, Rockingham**: Identified as Alyka/Kentico (Same platform as Stirling). Moved to Phase 3.
    - **Vincent**: WAF protected (Barracuda). Moved to Phase 4.
    - **South Perth**: Sitefinity. Moved to Phase 4.
    - **Belmont**: Investigation needed. Moved to Phase 3.

### Phase 3: The "Platform" Consolidation (In Progress)
- [x] **Goal 1: Catalyst Cluster (Completed 2026-01-21)**: Solved the 77 "Small Shire" sites (Ashburton, Beverley, Brookton, Carnarvon, etc).
    - Created `core/scrapers/catalyst.py`.
    - Migrated 77 councils from generic selectors to `catalyst_scraper` (fixing "malformed post" issues).
- [x] **Goal 2: Alyka/Kentico Cluster (Partially Complete)**:
    - **Stirling**: Custom scraper refactored into generic `AlykaScraper`. **FIXED**.
    - **Swan, Rockingham**: Confirmed Alyka/Kentico, but use different API endpoints (`/v1/aapi/search/htmlresult`). Disabled pending API reverse engineering.
    - **Belmont**: Confirmed Kentico CSR. Disabled.

### Phase 4: The "Too Hard Basket" (Custom Dev)
- [x] **South Perth**: Resolved! (Was sitefinity, but `card_scraper` works fine with correct URL).
- [ ] **Vincent**: WAF protected (Barracuda). `curl_cffi` blocked. Requires Playwright/Puppeteer.
- [ ] **Armadale**: React Server Components. Requires Playwright.
- [ ] **Joondalup**: Custom scraper (Working).
- [ ] **Action:** Write individual custom scrapers if ROI (population size) justifies it.

## 4. Continuous Improvement
- **Validation:** Added `core/validator.py` to prevent malformed posts.
- **Logging:** Added Discord-style logging (even if just to stdout) to track "Zero Article" runs.
