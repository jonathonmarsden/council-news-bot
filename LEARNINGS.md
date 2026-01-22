# Project Learnings & Technical Knowledge Base

**Date:** 2026-01-22
**Scope:** Findings from the WA Recovery Plan and Risky Selector Audit.

## 1. Scraper Architecture & Patterns

### 1.1 The "Strict Config" Trap
**Issue**: The `BaseScraper` and `CardScraper` constructors often use strict arguments (`__init__(self, config, db)`), but new scrapers were being initialized with `**kwargs` from the config loader. This led to `TypeError` crashes when the config dictionary contained unrecognized keys (like `excerpt_selector`).
**Solution**: 
*   Always filter configuration dictionaries before passing them to scraper classes if not using `**kwargs` in `__init__`.
*   Moved towards a pattern of explicit argument extraction in debug scripts:
    ```python
    c_config = {k:v for k,v in config.items() if k in ['url', 'selectors', '...']}
    scraper = CardScraper(c_config, None)
    ```

### 1.2 "Risky Selectors" & Fragility
**Observation**: Many councils (especially in WA) use generic Bootstrap classes (`.row`, `.col-sm-7`) as their primary content structure.
**Risk**: If the council changes their layout grid (e.g., to `.col-md-8`), scraper fails.
**Mitigation Strategy**:
*   **Semantic Anchors**: Instead of `div.col-sm-7`, prefer selectors that anchor to content, e.g., `div:has(> h2)`.
*   **Excerpt Selectors**: Adding `excerpt_selector` (even just `"p"`) is crucial for verifying that the "Item" found isn't just an empty container.
*   **Acceptance**: For legacy ASP.NET/Catalyst sites, these generic structures are paradoxically stable because the underlying CMS templates rarely change.

### 1.3 The "Alyka/Kentico" WAF & API
**Pattern**: Councils like Stirling, Swan, Rockingham use the Alyka platform (Kentico CMS).
**Challenges**:
*   **WAF**: Often protected by Barracuda or Cloudflare. `requests` fails. `curl_cffi` with `impersonate='chrome110'` (or newer '124') is required.
*   **API**: They often use a JSON-over-HTML endpoint (`/aapi` or `/ksearch`). The "JSON" is sometimes wrapped in invalid HTML.
*   **Solution**: The `AlykaScraper` was built to handle the POST requests to these endpoints. For **Swan** specifically, the `htmlresult` field contains raw HTML that requires a second pass of `BeautifulSoup` parsing to extract the actual news item content (Excerpts).

## 2. Platform Specifics

### 2.1 OpenCities (QLD/TAS/NSW)
*   **Marker**: `div.list-item-container`.
*   **Quirk**: Sometimes the `article` tag is missing, and valid content is just in `div` soup.
*   **Action**: `OpenCitiesScraper` is the preferred handler, but `CardScraper` can work if configured with `impersonate` enabled (OpenCities often blocks standard User-Agents).

### 2.2 Catalyst (WA)
*   **Marker**: `MyCouncil` or generic ASP.NET structure.
*   **Quirk**: Hundreds of small shires share this exactly. 
*   **Action**: `CatalystScraper` handles the 70+ homogeneous WA shires.

## 3. Deployment & Operations
*   **Remote Sync**: Deployment uses `rsync` from local to remote. Local changes must be valid before running `deploy_with_password.py`.
*   **Health Checks**:
    *   `scripts/check_site.py`: Essential for pre-deploy validation.
    *   `debug_<council>_repro.py`: Create these ephemeral scripts to test fixes without running the full bot.

## 4. Pending Risks
*   **Date Hallucinations**: Some scrapers might grasp "Posted by..." text as a date if regex is too loose. Strict date parsing validation is active.
*   **React/SPA sites**: Armadale remains a blocker due to React Server Components/hydration requiring JS execution (Playwright).
