# WA Recovery Report (West Coast Recovery)

## Overview
Investigation and remediation of failures in Western Australia (WA) councils.
Focus was on verifying access, enabling WAF bypass (`use_curl`), and fixing broken URLs.

## Fixed / Verified Councils

### 1. City of Belmont
- **Issue**: 404 on API endpoint and News page.
- **Fix**: 
  - Updated `news_url` to `https://www.belmont.wa.gov.au/api/search/search`.
  - Enabled `use_curl: true` to bypass generic blocking/header issues.
  - Validated API returns JSON with HTML content containing items.
- **Status**: PASSED.

### 2. City of Bayswater
- **Issue**: Suspected failure (debug file existed).
- **Verification**: `check_site.py` confirmed 12 items found with existing selectors. WAF bypass (`chrome124`) is active and working.
- **Status**: PASSED.

### 3. City of Rockingham
- **Issue**: Suspected failure.
- **Verification**: `check_site.py` confirmed 9 items found. `curl_scraper` is working correctly with `impersonate: chrome124`.
- **Status**: PASSED.

### 4. City of Cockburn
- **Issue**: Suspected failure.
- **Verification**: `check_site.py` confirmed 8 items found. `curl_scraper` works.
- **Status**: PASSED.

### 5. Shire of Broome
- **Issue**: Reported as `HARD_BLOCK` by diagnosis tool.
- **Verification**: `check_site.py` confirmed 3 items found. `use_curl: true` is effective.
- **Status**: PASSED.

### 6. Town of Cambridge
- **Issue**: OpenCities site suspected failing.
- **Verification**: Page loads (Status 200) with `curl`. Title "Latest News" found.
- **Status**: PASSED.

## Unfixable / Hard Cases (Disabled)

### 7. City of Armadale
- **Issue**: Next.js site with React Server Components (RSC). Content hydrated client-side or during RSC flight.
- **Action**: Confirmed `enabled: false` is correct. No RSS feed found despite extensive scan.
- **Recommendation**: Needs Playwright or Reverse Engineering of internal API.

### 8. City of Swan
- **Issue**: Alyka/Dynamic content.
- **Action**: Confirmed `enabled: false`.

## Summary
The "West Coast Recovery" phase has stabilised. Major metro councils (Belmont, Bayswater, Rockingham, Cockburn) are functional. 14% failure rate is likely reduced significantly by these and the broader `use_curl` rollout.
