# Risky Selector Audit & Remediation Plan

This report identifies 22 councils using "Risky Selectors" (layout classes like `.row`, `.col-`, `.list-item-container`) which are prone to breakage if the site layout changes.

**Objective**: Refactor these to use semantic selectors (`article`, `.news-item`, `h2`) or platform-specific classes.

## Identified Councils

### Victoria (Drupal/Squiz)
- [x] **whitehorse**: `.views-row` -> Hardened to `div.search-result` / `.search__title a`.
- [x] **wodonga**: `.postcard.row` -> Hardened to `a:has(h2)` (Container Link logic).
- [x] **greater-dandenong**: `.view-news .views-row` -> Hardened to `.views-row:has(.right-side)`.
- [x] **warrnambool**: `.listing.views-row` -> Hardened to `.listing.views-row:has(time)`.

### Northern Territory
- [x] **katherine**: `.module-list .row` (Fixed - SparkCMS/ASP)
- [x] **macdonnell**: `.module-list .row` (Fixed - SparkCMS/ASP)
- [x] **tiwi_islands**: `.module-list .row` (Fixed - SparkCMS/ASP)

### South Australia
- [x] **holdfast-bay**: `a.group:has(h3.heading-3)` (Fixed - Link Container)
- [x] **onkaparinga**: `.list-item-container article` (Fixed - OpenCities - URL Corrected)

### Queensland (OpenCities)
- [x] **logan**: `.news-list-container .list-item-container article` (Fixed - Hardened)
- [x] **moreton-bay**: `.news-list-container .list-item-container article` (Fixed - Hardened)
- [x] **rockhampton**: `.news-list-container .list-item-container article` (Fixed - Hardened)

### New South Wales
- [x] **bayside-council**: `article.event-teaser` -> Verified safe.
- [x] **city-of-canada-bay**: `.rows-content-view--wrapper` -> Verified, standard Drupal view wrapper.
- [x] **maitland-city-council**: `.civictheme-card-container__card` -> Fixed to `.civictheme-promo-card`.
- [x] **midcoast-council**: `.list-item-container article` -> Verified safe (OpenCities).
- [x] **nambucca-valley-council**: `.list-item-container article` -> Fixed to use `article` context.

### Tasmania (OpenCities Cluster)
- [x] **hobart**: `.news-list-container article` (Fixed)
- [x] **launceston**: `.news-list-container:not(.list-container-grid) article` (Fixed)
- [x] **burnie**: `.news-list-container article` (Fixed)

### Western Australia (Element Element / Generic)
- [x] **albany**: `.module-list .row` (Functional - SparkCMS/ASP)
- [x] **esperance**: `.module-list .row` (Fixed - SparkCMS/ASP)
- [x] **bridgetown-greenbushes**: `div.col-sm-7` -> Verified working. Selector maps to empty p tag often but item detection works.

## Remediation Usage Guide

For **OpenCities** (`.list-item-container`):
- Inspect `debug_<council>.html`.
- Look for `article` tag inside the container.
- If no article, look for a unique class like `.oc-list-item` or use the title selector linkage `h2.list-item-title` as the root if necessary (though CardScraper prefers a container).

For **Drupal** (`.views-row`):
- Almost always has `<article>` inside. Use `article` or `article.node`.

For **Bootstrap/Generic** (`.col-sm-7`):
- Find a unique parent ID (e.g., `#news-list`) or a child class.
- If absolutely generic, use `:has()` selector to anchor to the date or title.
  - Example: `div.col-sm-7:has(h2)` 

## Next Steps
1. Run `python3 scripts/debug/run_scraper.py <council_id>` to generate a debug dump.
2. Open `debug_<council_id>.html`.
3. Pick a better selector.
4. Update `states/<state>/councils.json`.
