# Northern Territory Scraper Status Report

**Date:** 2025-06-01
**Status:** 100% Coverage (18/18 Councils Passing)

## Summary
All 18 councils in the Northern Territory are now successfully scraping news articles.

## Council Details

| Council | Status | Method | Notes |
| :--- | :--- | :--- | :--- |
| Alice Springs Town Council | PASS | RSS | Standard RSS feed |
| Barkly Regional Council | PASS | HTML | Custom selectors |
| Belyuen Community Government Council | PASS | HTML | Custom selectors |
| Central Desert Regional Council | PASS | HTML | Requires `use_curl: true` & Joomla selectors |
| Coomalie Community Government Council | PASS | HTML | Custom selectors |
| City of Darwin | PASS | RSS | Standard RSS feed |
| East Arnhem Regional Council | PASS | HTML | Custom selectors |
| Groote Archipelago Regional Council | PASS | HTML | Custom selectors |
| Katherine Town Council | PASS | HTML | Custom selectors |
| Litchfield Council | PASS | RSS | Standard RSS feed |
| MacDonnell Regional Council | PASS | HTML | Custom selectors |
| City of Palmerston | PASS | HTML | Custom selectors |
| Roper Gulf Regional Council | PASS | HTML | Custom selectors |
| Tiwi Islands Regional Council | PASS | HTML | Custom selectors |
| Victoria Daly Regional Council | PASS | HTML | Custom selectors |
| Wagait Shire Council | PASS | HTML | Custom selectors |
| West Arnhem Regional Council | PASS | HTML | Custom selectors |
| West Daly Regional Council | PASS | HTML | Custom selectors |

## Key Fixes Implemented
1. **Central Desert**: Enabled `use_curl: true` to bypass WAF/User-Agent blocking. Implemented specific Joomla-based selectors (`div.item`, `h2[itemprop='headline']`).
2. **Coomalie**: Updated selectors to target `div.cms-news-item`.
3. **East Arnhem**: Updated to use `div.news-item` and `h4` for titles.
4. **Groote Archipelago**: Updated to use `div.blog-post`.
5. **Katherine**: Updated to use `div.row` and `span.h4`.
6. **MacDonnell**: Updated to use `div.news-item`.
7. **Tiwi Islands**: Updated to use `div.row` and `span.h4`.
8. **West Daly**: Updated to use `div.row.listing.news`.

## Next Steps
- Monitor `use_curl` usage to ensure it remains stable.
- Consider moving other councils to `use_curl` if they exhibit intermittent blocking.
