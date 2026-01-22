# Manual Fixes Completed

The following councils were manually investigated and repaired.

## ✅ Fixed

- **Moonee Valley City Council (VIC)**
    - Issue: WAF (Incapsula) blocking standard requests.
    - Fix: Switched to RSS feed (`https://mvcc.vic.gov.au/rss`) and enabled `use_curl` with `impersonate="safari15_5"`.
    - Status: Verified (10 articles found).

- **MidCoast Council (NSW)**
    - Issue: 404 on old URL.
    - Fix: Updated URL to `https://www.midcoast.nsw.gov.au/Your-Council/Our-news/News-releases` and updated selectors.
    - Status: Verified (10 articles found).

- **Towong Shire Council (VIC)**
    - Issue: 403 Forbidden (WAF).
    - Fix: Enabled `use_curl` and updated selectors to `#news-listing ul li`.
    - Status: Verified (20 articles found).

- **City of Canada Bay (NSW)**
    - Issue: Broken selectors.
    - Fix: Updated selectors to `.rows-content-view--wrapper`.
    - Status: Verified (7 articles found).

- **Merri-bek City Council (VIC)**
    - Issue: Broken selectors.
    - Fix: Updated selectors to `.collection__item`.
    - Status: Verified (272 articles found).

## 🛠️ System Improvements
- Added support for `impersonate` parameter in `councils.json` to allow specific browser impersonation per council (e.g. `safari15_5`).
- Improved `curl_cffi` integration to detect Incapsula block pages (status 200 but content blocked) and trigger proxy fallback.
