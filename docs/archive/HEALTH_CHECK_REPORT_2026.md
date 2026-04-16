# Global Bot Health Check Report - 2026-02-15

## Executive Summary
**Overall Status:** ⚠️ **OPERATIONAL WITH CRITICAL RISK**
**Key Risks:** Proxy authentication failures (407) during WA runs, extremely high "empty" scraper rate, and no new articles saved in the last 24h.
**Production Activity:** Scrapes are running (last runs ~2026-02-15 04:10), posting continues (9 posts in last 24h), but no new articles were saved in the last 24h.

## Scope & Method
- **Environments Assessed:** Local codebase + Production VPS (`170.64.186.16`).
- **Production Checks:** Docker status, disk usage, cron schedule, container logs, Postgres metrics, council health stats.
- **Data Sources:** VPS logs (`/var/log/council_bot_scraper.log`, `/var/log/council_bot_cron.log`) and Postgres (`council_news` DB).

## 1. Production Runtime Status
- **Containers:** `council_news_bot` and `council_db` are running.
- **Disk:** 74% used (`/dev/vda1`), 6.3G free.
- **App Size:** 297M at `/opt/council-news-bot`.
- **Cron:** Scraping runs every 3 hours by state groups; posting queue every 5 minutes.

## 2. Database Health (Postgres)
**Postgres is the active production DB.** Tables exist: `articles`, `scraper_stats`, `council_health`, `alembic_version`.

**Key Metrics (Postgres):**
- **Total Articles:** 13,800
- **Last Article Seen:** 2026-02-14 03:45:29
- **Collected in Last 24h:** 0
- **Posted in Last 24h:** VIC=3, WA=6
- **Active Councils (7d):** 332

**Scraper Stats (last 24h):**
- **Total Runs:** 5,065
- **Statuses:** 4,900 empty, 156 ok, 9 error
- **Articles Found (sum):** 4,071
- **Articles Saved (sum):** 0
- **Avg Duration:** 592 ms

**Council Health:**
- **Consecutive Failures >=3:** 1 council (Knox, last failure 2026-01-25)
- **Consecutive Empty Runs >10:** 212 councils

**Interpretation:** Scrapes are running and finding items, but most runs are empty or duplicate-only. New articles are not being saved in the last 24h. Posting continues from existing backlog.

## 3. Proxy & Network Health
Recent WA cron logs show widespread **HTTP 407 Proxy Authentication Required** errors:
- Multiple councils fail on HTTPS requests (Boyup Brook, Dowerin, Wagin, Wongan, Port Hedland, Cue, Pingelly, etc.).
- Curl tunnel failure noted for Swan (`curl: (56) CONNECT tunnel failed, response 407`).

**Impact:** WA coverage is degraded and likely returning 0 articles due to proxy failures.

## 4. Scraper Coverage & Output Quality
- **High Empty Run Rate:** 4,900 of 5,065 runs in the last 24h report status `empty`.
- **Articles Found vs Saved:** 4,071 found, 0 saved (likely duplicates or failing save path).
- **Active Councils (7d):** 332 indicates scraping is still reaching a subset of councils.

## 5. Posting & Queue Health
- **Posting Active:** 9 posts in last 24h (6 WA, 3 VIC).
- **Recent Posts:** Mostly Stirling (WA) and Greater Shepparton (VIC), suggesting backlog drainage rather than new intake.
- **Cron Queue:** `process_global_queue.py` is executing regularly (log entries every 5 minutes).

## 6. Monitoring & Observability
- **Discord Summaries:** Reliable delivery fix applied recently, but no evidence in logs of summary success/failure.
- **Daily Briefing:** Configured nightly; script posts to Discord (not safe for dry-run checks).
- **Health Check Scripts:** Postgres-backed health checks are now aligned with production (SQLite is no longer used).

## 7. Critical Risks
1. **Proxy Authentication Failures (407):** Causes widespread council scrape failures (WA especially).
2. **Empty Run Flood:** 96%+ of scraper runs in last 24h are `empty`.
3. **No New Articles in 24h:** Suggests upstream blockers (proxy, WAF, selectors) or dedupe short-circuit.

## 8. Hidden Assumptions (Validated or Broken)
- **Assumption:** Scraper success rate can be inferred from `status == 'success'`.
  - **Reality:** Status values are `ok`, `empty`, `error`. Success is not encoded as `success`.
- **Assumption:** Empty runs are rare and indicate selector failure.
  - **Reality:** 212 councils have >10 consecutive empty runs (chronic).

## 9. What We Are Missing (Gaps)
1. **Proxy Health Alerts:** Automatic detection and alerting for 407/402 failures.
2. **Empty-Run Alerting:** Trigger alerts for councils with repeated empty runs (council_health already tracks this).
3. **New vs Duplicate Metrics:** Distinguish duplicate-only runs vs real new content.
4. **Backlog Visibility:** Queue size per state, oldest unposted age.
5. **DB Backups:** No documented automated Postgres backups or restore tests.
6. **Log Hygiene:** Cron logs grow without rotation safeguards.
7. **Production Runbook:** Clear decision tree for proxy issues, WAFs, and empty-run spikes.

## 10. Immediate Recommendations
1. **Fix Proxy Credentials Now:** Verify Webshare credentials and rotate if needed.
2. **Alert on Empty Runs:** Use `council_health.consecutive_empty_runs` to notify Discord.
3. **Record Duplicate Counts:** Track duplicates vs new saves per run.
4. **Rotate Cron Logs:** Add logrotate or move to Docker log driver.

## 11. Current Status Verdict
The system is running, but health indicators show **major coverage degradation** (proxy failures and high empty-run rates). Immediate attention is needed to restore WA scraping reliability and reduce empty-run spikes.
