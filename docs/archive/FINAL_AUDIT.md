# Comprehensive WA Council Bot Audit & Health Check
**Date:** 2026-01-21
**Author:** GitHub Copilot (Gemini 3 Pro)

## 1. Executive Summary

A comprehensive audit of the Western Australia (WA) configuration for the Council News Bot was conducted following the successful implementation of custom scrapers for the "Big 4" snowflake councils (Joondalup, Perth, Claremont, Wanneroo).

**Current Status:**
- **Codebase:** Fully deployed with fixes for all 4 major difficult councils.
- **Coverage:** Only **15.9%** (22/138) of WA councils have active data in the database.
- **Backlog:** 1350 articles have been scraped but not posted to Bluesky.
- **Critical Gap:** 116 "Catalyst" councils (small shires sharing the same template) are configured but have not yet been scraped in the production cycle.

## 2. State Comparison

WA lags significantly behind other states in terms of active coverage, primarily due to the previous lack of a dedicated `CatalystScraper` for the small shires and the complexity of the metropolitan councils.

| State | Total Articles | Active Councils | Coverage Estimate |
|---|---|---|---|
| **VIC** | 2610 | 79 | ~100% |
| **QLD** | 1304 | 72 | ~92% |
| **NSW** | 1049 | 68 | ~53% |
| **WA** | 1388 | 22 | **15.9%** |
| **ACT** | 627 | 1 | 100% |
| **SA** | 585 | 38 | ~55% |
| **TAS** | 227 | 23 | ~79% |

## 3. The "Snowflake" Solution Verification

The four most difficult WA councils have been successfully reverse-engineered and implemented.

| Council | Challenge | Solution | Status | Latest Data |
|---|---|---|---|---|
| **Joondalup** | Complex Kentico CMS AJAX payload | Reverse-engineered `aw_pagetypelisting.js` payload structure. | ✅ FIXED | 12 articles |
| **Perth** | Blocking & DOM obfuscation | `curl_cffi` + `chrome110` impersonation. | ✅ FIXED | 4 articles |
| **Claremont** | Non-standard DOM | Custom HTML parser. | ✅ FIXED | 8 articles |
| **Wanneroo** | Partial feed | `curl_cffi` + Custom parser. | ✅ FIXED | 36 articles |

## 4. Discrepancy Analysis (Bluesky)

There is a massive discrepancy between **Scraped** and **Posted** content for WA.

- **Scraped (WA):** 1388
- **Posted (WA):** 38
- **Gap:** 1,350 articles.

**Root Cause:**
1.  **Freshness Filter:** The bot's default logic archives articles older than 7 days. Since many WA scrapers were just enabled or fixed, they fetched months of history which is immediately archived.
2.  **Rate Limiting:** The Bluesky poster has a safety limit (default 5 posts per council per run).
3.  **New Snowflake Data:** The 50+ articles just scraped from the snowflakes are marked as `new` in the DB (because the manual `run_wa_snowflakes.py` script bypassed the freshness filter logic), but they haven't been processed by the poster loop yet.

## 5. Improvement Strategy

### Phase 1: Activate the Catalyst Cluster (Immediate)
The config for 116 small shires has been updated to use `catalyst_scraper`, but the scraper hasn't run.
**Action:** Run `python3 main.py --state wa --dry-run` to verify, then full run.

### Phase 2: Backlog Management
To avoid spamming the Bluesky feed with 1,350 old articles:
1.  Run a DB update to mark all `new` articles older than 7 days as `archived`.
2.  Allow the bot to post only the truly fresh content from the recent fixes.

### Phase 3: Cross-State Standardization
- WA's "Catalyst" pattern (shared templates) is similar to NSW's "OpenCities" pattern.
- **Recommendation:** Refactor `catalyst_scraper` into a generic `SharedTemplateScraper` if other states show similar patterns.

## 6. Failed/Silent Councils (Sample)
The following councils are correctly configured but have 0 articles in the DB. This is a "Deployment" issue, not a "Code" issue. Running the bot will fix this.
- City of Armadale
- Shire of Ashburton
- Shire of Augusta Margaret River
- City of Belmont
- Shire of Beverley
- ... and 100+ more.
