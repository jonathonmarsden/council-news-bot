# Northern Territory Scraper Repairs - Jan 2026

## Summary
Audited NT councils and repaired "Zombie" scrapers (working on surface but stale or broken).

## Actions Taken

| Council | Issue | Resolution | Status |
| :--- | :--- | :--- | :--- |
| **City of Darwin** | RSS feed dead/gone. | Switched to `curl_scraper`. Selectors: `div.news-grid-item`. | ✅ Fixed |
| **City of Palmerston** | RSS availability poor. | Switched to `curl_scraper`. Selectors: `article.teaser-card`. | ✅ Fixed |
| **Litchfield Council** | RSS feed functional but serving 2014-2020 content. | Switched to `curl_scraper`. Selectors: `div.news-article-item`. | ✅ Fixed |
| **Victoria Daly** | RSS URL moved. | Updated URL to `/feed/`. | ✅ Fixed |
| **West Daly** | Server returning HTTP 500 / 509 Bandwidth Exceeded. | Disabled to prevent build failures. | ❌ Disabled |
| **Belyuen** | Suspected zombie. | Verified RSS is active and fresh (Jan 2026). No action needed. | ✅ Verified |

## Technical Details

### Darwin
- **URL**: `https://www.darwin.nt.gov.au/news`
- **Engine**: Drupal 10
- **Selectors**:
  - Item: `div.news-grid-item`
  - Title: `.field--name-node-title h3 a`
  - Date: Text parsing in container.

### Palmerston
- **URL**: `https://palmerston.nt.gov.au/news`
- **Engine**: Drupal 10 (likely)
- **Selectors**:
  - Item: `article.teaser-card`
  - Title: `h3.teaser-card__title a`
  - Date: `time.teaser-card__time`

### Litchfield
- **URL**: `https://www.litchfield.nt.gov.au/news`
- **Engine**: Drupal
- **Selectors**:
  - Item: `div.news-article-item`
  - Title: `h3 a`
  - Date: `time` (datetime attr)
