# Risky Selector Audit & Remediation Plan

This report identifies 22 councils using "Risky Selectors" (layout classes like `.row`, `.col-`, `.list-item-container`) which are prone to breakage if the site layout changes.

**Objective**: Refactor these to use semantic selectors (`article`, `.news-item`, `h2`) or platform-specific classes.

## Identified Councils

### Victoria (Drupal/Squiz)
- [ ] **whitehorse**: `.views-row` -> Look for `.node` or `.news-teaser`
- [ ] **wodonga**: `.postcard.row` -> Look for `article` or `div.card`
- [ ] **greater-dandenong**: `.view-news .views-row` -> Look for `article`
- [ ] **warrnambool**: `.listing.views-row` -> Look for `article`

### Northern Territory
- [x] **katherine**: `.module-list .row` (Fixed - SparkCMS/ASP)
- [x] **macdonnell**: `.module-list .row` (Fixed - SparkCMS/ASP)
- [x] **tiwi_islands**: `.module-list .row` (Fixed - SparkCMS/ASP)

### South Australia
- [ ] **holdfast-bay**: `div.news-listing__item` (better), but generic fallback implies risk.
- [ ] **onkaparinga**: `div.list-item-container` (OpenCities)

### Queensland (OpenCities)
- [ ] **logan**: `.list-item-container`
- [ ] **moreton-bay**: `.list-item-container`
- [ ] **rockhampton**: `div.list-item-container`

### New South Wales
- [ ] **bayside-council**: `.views-row article` -> This is actually okay (`article`), but `.views-row` is redundant. Use `article`.
- [ ] **city-of-canada-bay**: `.rows-content-view--wrapper` -> Inspect.
- [ ] **maitland-city-council**: `.civictheme-card-container__card` -> This looks specific (CivicTheme), might be okay, but verify.
- [ ] **midcoast-council**: `.list-item-container article` -> Okay.
- [ ] **nambucca-valley-council**: `div.list-item-container`

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
