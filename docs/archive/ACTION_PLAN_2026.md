# Action Plan 2026: The "Deep Dive" Recovery

**Status:** ACTIVE
**Last Updated:** 2026-02-15
**Priority:** STABILITY > COVERAGE > FEATURES

## 0. Scheduling Overhaul: Twice-Daily Model (In Progress, Feb 2026)

Transitioning from **continuous 3-hourly scraping** to a **twice-daily schedule** (06:00 & 18:00 local per state).

**Status:** 
- ✅ Core timezone and cron generation utilities created
- ✅ Test coverage for DST transitions and timezone conversions
- ✅ `main.py` updated with `--time-window` flag for dynamic concurrency
- ✅ Crontab generation script deployed (`generate_crontab.py`)
- ✅ Documentation (SCHEDULING_GUIDE.md) written
- ✅ DEPLOYMENT.md updated
- 🔄 Ready for VPS deployment and monitoring

**Key Changes:**
- **Frequency**: 8 scrapes/day → 2 scrapes/day (75% load reduction)
- **Timing**: Localized to each state's timezone (accounts for DST)
- **Concurrency**: Dynamic reduction during morning peak (06:00–08:30)
- **Queue**: Every 10 minutes (down from 5)
- **Staggering**: 4 state groups, 30 min apart to avoid thundering herd

**Next Steps:**
1. Deploy crontab to VPS (via `generate_crontab.py --static`)
2. Monitor first 2 weeks for coverage & performance
3. Adjust concurrency if needed based on proxy failures
4. Document DST handling for future maintainers

**References:**
- [SCHEDULING_GUIDE.md](SCHEDULING_GUIDE.md)
- [Timezone Utils](core/timezone_utils.py)
- [Crontab Generation](scripts/deployment/generate_crontab.py)

---

## 1. Immediate Maintenance (Completed)
- [x] **Audit VPS Health**: Confirmed healthy (Docker, Postgres, Disk).
- [x] **Fix Critical Security Flaw**: Patched `base.py` to prevent "Proxy Leak" (using direct connection when proxy is configured).
- [x] **Sanitize Database**: Ran `fix_mojibake_urls.py` to fix 155 corrupted URLs.
- [x] **Prevent Future Corruption**: Added `urllib.parse.quote` to `NewsArticle` post-init hook.
- [x] **Fix Infinite Loops**: Updated `cleanup_remote_db.py` to archive (not delete) future-dated articles.

## 2. High Priority: Silent Failures (Zombies)
The recent health check identified several councils returning `0 articles` without throwing errors. This is the "Zombie Scraper" state.

**Task**: Investigate and Fix Selectors for:
- **Peppermint Grove (WA)**
- **Quairading (WA)**
- **Sandstone (WA)**
- **Vincent (WA)** (Note: Bayside VIC also showed issues in dry-run)

**Action**:
1. Run `./debug_council.sh <id>` (or `main.py --dry-run`).
2. Update `councils.json` selectors or headers.
3. Deploy fix.

## 3. Medium Priority: Monitoring Scalability (Partially Completed ✅)

The current monitoring had two issues:
1. ✅ **Discord Webhook Reliability**: `discord_logger.py` lacked retry logic and error handling.
   - **Status: RESOLVED (Feb 15, 2026)**
   - **Fix**: Added exponential backoff, timeout enforcement, 429 rate-limit handling, and response validation.
   - **Outcome**: Discord summaries now post reliably with accurate council/article counts.

2. ✅ **Council Counting Accuracy**: Summaries were showing "Councils: 0" because the accumulator wasn't called for councils with 0 articles.
   - **Status: RESOLVED (Feb 15, 2026)**
   - **Fix**: Added `current_run.log_success()` calls for zero-article councils and error councils in `main.py`.
   - **Outcome**: Discord summaries now show accurate metrics (e.g., "Councils: 79, Articles Found: 175").

**Remaining Task**: Implement proactive alerting for "consecutive zero counts" (3+ runs with 0 articles for a council).
- **Implementation Approach**: Add `log_error()` method to `RunAccumulator` for failure tracking; store persistent state via DB `scraper_stats` table.
- **Priority**: Medium (useful for detecting broken selectors early).


## 4. Low Priority: Infrastructure Hygiene
- **Task**: Standardize Logging.
- **Goal**: Replace `print()` with `logger` across *all* scripts (started in `base.py`, need to finish `main.py`).
- **Task**: Fix Report Persistence.
- **Goal**: Update `scripts/comprehensive_health_check.py` to write to `/app/data/` so reports can be read from the host.

## 5. Long Term: "Generic" Evolution
- **Goal**: Move away from per-council CSS selectors where possible.
- **Idea**: Use LLM-based parsing for "difficult" sites (only if cost-effective), or invest in `JsonScraper` discovery for more councils (like Armadale).
