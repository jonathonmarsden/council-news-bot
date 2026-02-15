# Victorian Scraper Audit & Repair Report 2026

**Date**: January 25, 2026
**Status**: All Victorian Councils Audited and Validated.

## 🏆 Project Completion Summary
We have systematically audited, diagnosed, and repaired scrapers for all ~79 Victorian councils. The primary issue identified was the migration of ~80% of councils to a new **OpenCities** responsive layout which broke legacy generic selectors.

## 🛠 Major Repair Patterns

### 1. The "OpenCities" Standard
Dozens of councils were migrated to a unified `CardScraper` configuration using robust container-based selectors.
- **Councils**: `moira`, `monash`, `moorabool`, `surf-coast`, `swan-hill`, `wangaratta`, `west-wimmera`, `whittlesea`, `yarra-ranges`, `yarriambiack`, `mornington-peninsula`, `mount-alexander`, `moyne`, `murrindindi`, `nillumbik`, `northern-grampians`, `pyrenees`, `queenscliffe`, `southern-grampians`, `stonnington`.
- **Config Pattern**:
  ```json
  "scraper": "card_scraper",
  "item_selector": ".list-item-container",
  "title_selector": ".list-item-title",
  "link_selector": "a",
  "date_selector": ".published-on"
  ```

### 2. GovCMS / Drupal Fixes
Several sites use GovCMS (Drupal) with `views-row` structures often nested deeply.
- **Councils**: `latrobe-vic`, `whitehorse`, `wyndham`.
- **Config Pattern (Typical)**:
  ```json
  "item_selector": ".views-row",
  "title_selector": "h3 a",
  "link_selector": "h3 a",
  "date_selector": "time, .date"
  ```

### 3. Custom / Edge Cases
- **Knox**: Modern card layout (`.card-default .card`).
- **Wodonga**: Custom `.postcard` layout with split columns.
- **Yarra**: Article Card where the entire item is the link (`a.card-y`).
- **Wellington / Warrnambool**: Validated as working with Browser Scraper fallback or RSS.

## ✅ Verification
All repaired councils were dry-run verified to ensure:
- Items are found (Quantity > 0).
- Titles are correctly extracted (No "None" or "Missing title").
- URLs are correctly formed.
- Resilience against WAF (Curl/Impersonate enabled for most).

## ⏭ Next Steps
- **Monitoring**: Watch for `Missing title or url` errors in production logs, as platform updates usually break selectors in groups.
- **NSW Audit**: Proceed to New South Wales using the same "Batch Audit -> Pattern Match -> Mass Fix" methodology.
