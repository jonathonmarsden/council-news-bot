# Twice-Daily Scheduling Guide

**Last Updated:** February 15, 2026
**Status:** Active Deployment
**Reference Architecture:** VPS Cron + Docker Compose

---

## Overview

The Council News Bot has transitioned from **every 3-hour continuous scraping** to a **twice-daily schedule** with localized time windows per state.

**Key Changes:**

| Aspect | Old | New |
|--------|-----|-----|
| **Frequency** | Every 3 hours (8× daily) | 2× daily (morning & evening) |
| **Target Times** | Arbitrary (00:00, 03:00 UTC) | 06:00 & 18:00 local per state |
| **Load Management** | Fixed concurrency | Dynamic (reduced during morning peak) |
| **Queue Processing** | Every 5 minutes | Every 10 minutes |
| **Total Cron Jobs** | 8 states × 8 times = 64 lines | 16 states × 2 times + queue + monitoring = ~30 lines |

---

## Schedule Architecture

### Time Windows (Local per State)

Two distinct scraping windows per state:

- **Morning Window:** 06:00 ± 2 hours (06:00–08:30 local)
  - Captures overnight news from council websites.
  - Reduced concurrency to manage proxy/network load during peak hours.
  
- **Evening Window:** 18:00 ± 2 hours (18:00–20:30 local)
  - Captures business-hours updates.
  - Standard concurrency (no reduction).

### Auto-Staggering Between States

To avoid thundering herd during exact times, states are grouped and staggered:

| Group | Morning | Evening | States |
|-------|---------|---------|--------|
| 1 | 06:00-06:30 local | 18:00-18:30 local | NSW, VIC |
| 2 | ~06:30-07:00 local | ~18:30-19:00 local | QLD, TAS |
| 3 | ~07:00-07:30 local | ~19:00-19:30 local | WA, SA |
| 4 | ~07:30-08:00 local | ~19:30-20:00 local | NT, ACT |

**Note:** The exact stagger offset depends on UTC conversion per state (time zones differ).

### UTC Conversion Example (Feb 15, 2026, Summer in Australia)

| State | Timezone | Morning Local | Morning UTC | Evening Local | Evening UTC |
|-------|----------|---------------|-------------|---------------|-------------|
| NSW | AEDT (UTC+11) | 06:00 | 19:00 prev | 18:00 | 07:00 |
| WA | AWST (UTC+8, no DST) | 06:00 | 22:00 prev | 18:00 | 10:00 |
| SA | ACDT (UTC+10:30) | 06:00 | 19:30 prev | 18:00 | 07:30 |

---

## Dynamic Concurrency Rules

To reduce strain on proxy servers and network during morning peak (06:00–08:30 local):

### Off-Peak (Evening & Off-Hours)

```
NSW, VIC, WA:      concurrency 8
QLD, SA:           concurrency 6
TAS, NT, ACT:      concurrency 4
```

### Morning Peak (06:00–08:30 Local)

```
NSW, VIC, WA:      concurrency 4    (50% reduction)
QLD, SA:           concurrency 3    (50% reduction)
TAS, NT, ACT:      concurrency 2    (50% reduction)
```

**Implementation:**

The `--time-window` flag is passed from cron to `main.py`:

```bash
python3 main.py --state nsw --concurrency 4 --time-window morning
```

If `--time-window` is not provided, `main.py` auto-detects based on current time in the state's local timezone.

---

## Daylight Saving Time (DST) Handling

Australia observes DST in different regions at different times:

### DST Transitions

| Region | Summer Offset | Winter Offset | Spring Forward | Fall Back |
|--------|---------------|---------------|---|---|
| **Eastern (NSW, VIC, TAS, ACT)** | UTC+11 (AEDT) | UTC+10 (AEST) | 1st Sun Oct | 1st Sun Apr |
| **Central (SA)** | UTC+10:30 (ACDT) | UTC+9:30 (ACST) | 1st Sun Oct | 1st Sun Apr |
| **Western (WA, NT) & Queensland** | UTC+8 (AWST) | UTC+8 (AWST) | Never | Never |

### Handling DST Changes

The `generate_crontab.py` script calculates UTC times per state **at the time of crontab generation**. 

**Important:** After DST transitions (early October and early April), **regenerate the crontab** to recalculate UTC offsets:

```bash
# Re-generate and deploy crontab after DST change
python3 scripts/deployment/generate_crontab.py --static > /tmp/crontab_new.txt
# SSH to VPS and manually update crontab -e with new times
```

**Why?** Cron only understands UTC, and changing offsets shifts UTC times by ±1 hour.

---

## Deployment & Operations

### Initial Deployment

1. **Generate the crontab:**
   ```bash
   python3 scripts/deployment/generate_crontab.py --static
   ```

2. **SSH to VPS and apply:**
   ```bash
   ssh root@vps.example.com
   crontab -e
   # Paste contents generated above
   ```

3. **Verify:**
   ```bash
   crontab -l | grep "council"
   ```

### Monitoring

Run the health check to verify the schedule is working:

```bash
python3 scripts/deployment/check_twice_daily_schedule.py
```

Ensure the summary jobs are in cron:

```bash
# Hourly activity summary
0 * * * * cd /opt/council-news-bot && docker compose exec -T bot python3 scripts/monitoring/hourly_briefing.py

# Daily briefing (21:00 UTC)
0 21 * * * cd /opt/council-news-bot && docker compose exec -T bot python3 scripts/monitoring/daily_briefing.py
```

Expected output:
```
NSW morning: Last run 2026-02-15 06:15 UTC ✓
VIC evening: Last run 2026-02-14 18:45 UTC ✓
WA morning: Last run 2026-02-15 05:50 UTC ✓ (within 1 hour of 06:00 local)
...
```

### Emergency Operations

**Stop all scraping immediately:**
```bash
ssh root@vps.example.com
crontab -e
# Comment out all 'council-news-bot' lines, save & exit
crontab -l  # Verify
```

**Re-enable scraping:**
```bash
# Uncomment lines in crontab
crontab -e
```

---

## Troubleshooting

### Issue: Cronrunning at wrong times

**Cause:** UTC offset mismatch due to DST or timezone misconfiguration.

**Solution:**
1. Check current DST status: `date` on VPS
2. Regenerate crontab:
   ```bash
   python3 scripts/deployment/generate_crontab.py --timeline-only --date 2026-02-15
   ```
3. Compare generated times vs actual cron execution (check logs).
4. Redeploy if needed.

### Issue: Morning runs exceeding 2-hour window

**Cause:** High concurrency or slow proxy responses causing run to extend past 08:30.

**Solution:**
1. Reduce concurrency further in `timezone_utils.py`:
   ```python
   # In get_recommended_concurrency():
   NSW: 3 (was 4)   # morning
   ```
2. Regenerate crontab and deploy.

### Issue: No articles found during morning run

**Cause:** WAF/proxy rejecting requests during peak hours, or selectors broken.

**Solution:**
1. Check logs for HTTP 407 (proxy auth) or 403 (WAF):
   ```bash
   ssh root@vps.example.com
   tail -100 /var/log/council_bot_scraper.log | grep -i "407\|403\|error"
   ```
2. If proxy issue: rotate credentials in `.env`.
3. If selector issue: debug specific council with `main.py --council <id> --dry-run`.

### Issue: Too many posts per hour (BlueSky rate limit)

**Cause:** Queue processor running every 10 minutes × all states = ~12 posts/min potential.

**Solution:**
1. Increase queue processor frequency to 15–20 minutes:
   ```bash
   # In crontab:
   */20 * * * * cd /opt/council-news-bot && docker compose exec -T bot ...
   ```
2. Reduce `--limit` in `process_global_queue.py` from 2 to 1 per state per run.

---

## Performance Baseline

Expected resource usage under twice-daily schedule (Feb 2026):

| Metric | Value | Note |
|--------|-------|------|
| **Concurrent Threads (Morning Peak)** | ~20 | 4 states × avg 5 councils each |
| **CPU Usage (Morning)** | 40–60% | Reduced from 70%+ (every 3 hours) |
| **Network Throughput** | 2–5 MB/s | Per state group |
| **Queue Size (Evening)** | 50–150 articles | Balanced across states |
| **Avg Post Latency** | 5–10 min | From scrape → posting |
| **Database Write Rate** | 20–50 rows/min | Articles + scraper_stats |

---

## Future Optimization Ideas

1. **Selective Council Scraping:** Only scrape councils with >5% success rate during evening, full scan at morning.
2. **Proxy Connection Pooling:** Keep proxy connections alive across consecutive requests.
3. **Caching Layer:** Local Redis for "check if council updated since last scrape."
4. **ML-Based Scheduling:** Analyze council "news frequency" and only scrape at optimal times.

---

## References

- [Timezone Utilities](../../core/timezone_utils.py)
- [Crontab Generation](../../scripts/deployment/generate_crontab.py)
- [Main Entry Point (--time-window)](../../main.py)
- [DEPLOYMENT.md](../../DEPLOYMENT.md)

```