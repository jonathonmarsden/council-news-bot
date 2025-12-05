# Deployment Report - OpenCities Fixes

## Status: SUCCESS

### 1. Deployment Details
- **Target**: `vps.example.com` (DigitalOcean Droplet)
- **Timestamp**: 2025-12-05 00:41 AEDT
- **Version**: Includes OpenCities Scraper and fixes for 55 councils.

### 2. Verification
- **Service Status**: Running (Docker Container `council_news_bot`)
- **Logs**: Confirmed startup and scheduler initialization.
- **Configuration**: Verified `nsw` and others are being scraped.

### 3. OpenCities Summary
- **Total Councils Updated**: 55
- **New Scraper**: `OpenCitiesScraper` (handles Standard and Squiz/Funnelback layouts).
- **Key Fixes**:
    - **Goulburn Mulwaree**: Fixed URL and implemented standard OpenCities scraping.
    - **Albury City**: Fixed URL and implemented Cloudflare bypass + Squiz scraping.
    - **WAF Bypass**: Enabled `use_curl` for all 55 OpenCities councils to handle Cloudflare/Imperva.

### 4. Next Steps
- Monitor logs for `nsw` scrape completion to verify OpenCities councils are yielding results.
- Check `bot.db` tomorrow to confirm new articles from these previously "Zero-Yield" councils.

---

# Deployment Report - Western Australia Expansion


## Status: SUCCESS

### 1. Deployment Details
- **Target**: `vps.example.com` (DigitalOcean Droplet)
- **Timestamp**: 2025-12-04 12:24 UTC
- **Version**: Includes full Western Australia (WA) rollout

### 2. Verification
- **Service Status**: Running (Docker Container `council_news_bot`)
- **Logs**: Confirmed startup and scheduler initialization.
- **Configuration**: Verified `wa` is included in the scrape list: `['act', 'nsw', 'nt', 'qld', 'sa', 'tas', 'vic', 'wa']`

### 3. Western Australia (WA) Summary
- **Total Councils**: 138
- **Active Scrapers**: 34
- **Empty/Valid Feeds**: 104
- **Errors**: 0
- **Key Fixes**:
    - **Mingenew**: Custom CSS selectors implemented.
    - **Menzies**: Switched to Instagram feed (News page was empty).
    - **Perth**: Added WAF bypass headers.
    - **Redirects**: Fixed 17 councils with changed URLs.

### 4. Next Steps
- Monitor the logs over the next 24 hours to ensure WA councils are being scraped correctly in the production environment.
- Check `bot.db` (via `debug_db.py` locally or on server) tomorrow to confirm new articles are being ingested.
