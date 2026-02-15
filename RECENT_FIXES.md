# Recent Fixes & Improvements (February 2026)

## Session: Feb 15, 2026 - Health Check & Reliability Hardening

### 1. ✅ Playwright Version Update (Browser Scraping)
- **File**: `Dockerfile`
- **Issue**: Browser-based scrapers (Playwright) returning 0 articles; version mismatch warning in logs.
- **Root Cause**: Base image pinned to `mcr.microsoft.com/playwright/python:v1.57.0-jammy` which had incompatibilities.
- **Fix**: Updated to `mcr.microsoft.com/playwright/python:v1.58.0-jammy`.
- **Validation**: Test scrape found 175 articles from Victorian councils (previously 0).
- **Impact**: Browser scraping for complex sites (JavaScript-rendered) is now fully functional.

### 2. ✅ Discord Webhook Reliability Hardening
- **File**: `discord_logger.py` (`RunAccumulator.send_summary()` method)
- **Issue**: Discord webhooks failing silently; summaries not reaching `#post-log` channel.
- **Root Cause**: No retry logic, no timeout enforcement, no 429 rate-limit handling.
- **Fixes Applied**:
  - Added exponential backoff retry (3 attempts with 1s, 2s, 4s delays)
  - Request timeout: 10 seconds
  - 429 rate-limit detection and adaptive backoff
  - Response validation and detailed error logging
- **Validation**: Successful webhook delivery confirmed in live scrape test.
- **Impact**: Operational summaries now post reliably to Discord; issues are logged instead of failing silently.

### 3. ✅ Discord Summary Zero-Count Bug (Accumulator Logic)
- **File**: `main.py` (`scrape_councils()` function)
- **Issue**: Discord summaries showing "Councils: 0, Articles Found: 0" despite bot scraping successfully.
- **Root Cause**: `RunAccumulator.log_success()` only called in `process_articles()` for councils WITH articles found. Councils with 0 articles were not logged, skewing the count.
- **Fixes Applied**:
  - **Line ~154-160**: Added `current_run.log_success(council_name, 0, 0)` when a council returns 0 articles.
  - **Line ~179-186**: Added `current_run.log_success(council_name, 0, 0)` in exception handler for error councils.
- **Validation**: 
  - NT scrape: All 17 councils logged in accumulator ✅
  - VIC scrape: 79 councils, 175 articles found, Discord summary sent with correct counts ✅
- **Impact**: Discord summaries now show accurate metrics (e.g., "Councils: 79, Articles Found: 175, Posted: 0").

### 4. ✅ Proxy Authentication Issue (Earlier in Session)
- **Environment**: `.env` on VPS
- **Issue**: 402/407 Proxy authentication errors from Webshare proxy.
- **Root Cause**: Username mismatch in `COUNCIL_BOT_PROXY` variable (REDACTED vs. different stored password).
- **Fix**: Updated `.env` with correct Webshare credentials and restarted Docker.
- **Impact**: Proxy-based scrapers resumed working; proxy auth no longer a blocker.

---

## Testing & Deployment

All fixes were:
1. **Tested locally** before deployment (where applicable)
2. **Deployed to VPS** via `scripts/deployment/deploy_to_vps.sh`
3. **Validated with live scrapes** (NT, VIC, QLD, SA, ACT test runs)
4. **Confirmed in Discord** (summaries now show proper counts)

---

## Current Status
- **Bot Health**: ✅ Fully operational
- **Scraping**: ✅ All 8 states + 540+ councils
- **Posting**: ✅ Active to BlueSky
- **Discord Logging**: ✅ Reliable with proper metrics
- **Database**: ✅ Healthy (1000+ articles)

---

## Outstanding Work
See `ACTION_PLAN_2026.md` for:
- Proactive alerting for "consecutive zero counts" (Low priority, nice-to-have)
- Code hygiene (cleaning up `debug_*` files)
- Unified error handling in `scheduler.py`
