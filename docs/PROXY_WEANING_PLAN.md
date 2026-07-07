# Proxy Weaning Plan

**Test evidence (2026-07-07):** all 532 enabled councils scraped with NO proxy
from a residential IP (`scripts/analysis/test_all_councils_noproxy.py`, run
from a home connection — the same network class as Rakali):

| Result | Councils |
|--------|----------|
| OK with existing config, no proxy | 476 (89%) |
| OK after a verified one-line config fix (applied to councils.json same day) | 33 → **509/532 (96%)** |
| Still failing — confirmed twice, same errors with or without proxy | 23 (ordinary scraper rot: 404'd feeds, changed markup, path-specific 403s) |

**Conclusion: zero councils demonstrably require the proxy from a residential
IP.** The 23 failures are repair-backlog items, not proxy dependencies.

It also found the July SA incident: SA sites now WAF-block plain `requests`
fetches. That's what tripped ~29 SA councils into the empty-run breaker during
July 4–7. `use_curl` + `chrome124` impersonation fixes all but 3 of them —
those fixes are in `states/sa/councils.json` now.

## Who actually uses the proxy today (pre-weaning)

- 280 councils: `use_curl` → **never used the proxy**.
- ~32 councils (browser_scraper, wordpress, json, spark, belmont): were
  *silently* bypassing the proxy for months (SCRAPE-4 bug, now fixed to honor
  config — but the point stands: they worked direct from the VPS IP).
- ~220 councils (card/catalyst/lgasa/rss/opencities/alyka via `fetch_page`)
  route through `COUNCIL_BOT_PROXY` when it is set.
- 4 councils request `COUNCIL_BOT_ROTATING_PROXY`; 10 set `bypass_proxy`.

## The staged plan

1. **Deploy the July 2026 fix branch** (Phases 1–4 + the 33 config fixes).
   Staggered `--scrape-only` scraping + curl impersonation is the load profile
   the proxy was bought to smooth over; both are now in place.
2. **Re-enable the trapped councils.** ~80 are disabled (mostly the SA WAF
   wave). After deploy, either wait ≤3 days for automatic probation (CORE-1)
   or run the one-off reset:
   `UPDATE council_health SET is_disabled=false, disabled_at=null, consecutive_empty_runs=0 WHERE is_disabled;`
3. **Watch for a few days with the proxy still ON.** feed_watchdog (4h, VPS +
   GitHub runner) and alert_check (6h, now with missed-run + stalled-queue
   checks) are the tripwires.
4. **Turn the proxy off on the VPS:** blank `COUNCIL_BOT_PROXY` and
   `COUNCIL_BOT_ROTATING_PROXY` in `/opt/council-news-bot/.env`. Caveat: the
   test ran from a residential IP; the DigitalOcean IP may be treated worse by
   some WAFs. That's fine — regressions now show up as *failures* (ScrapeError
   → alert within hours), not silent empty-runs, and the per-council fix is
   `use_curl`/`impersonate`/`bypass_proxy` as usual.
5. **Watch one more week, then cancel the proxy subscriptions.**
6. **Migrate to Rakali** (`docs/MIGRATION_TO_RAKALI.md`) — the home IP is the
   IP class this plan was validated on. Sizing stays 2–3 GB / 2 vCPU thanks to
   staggering + the Chromium semaphore.

## The 23 confirmed-broken councils (repair backlog, proxy-irrelevant)

Failures identical on two runs, no proxy involved. Triage with
`docs/SCRAPER_REPAIR_PLAYBOOK.md`.

| Council | Scraper | Symptom |
|---------|---------|---------|
| nsw/bogan-shire-council | rss | feed URL fetch fails |
| nsw/upper-lachlan-shire-council | wordpress | API returns no posts |
| nt/barkly | card | 0 items (markup changed?) |
| qld/pormpuraaw | curl | 0 items |
| qld/south-burnett | curl | 0 items |
| qld/yarrabah | rss | feed 404 (long-standing; PDF-only site) |
| sa/berri-barmera | lgasa | listing fetch fails |
| sa/mount-barker-district | lgasa | listing fetch fails (403 even with curl) |
| sa/yankalilla | lgasa | 0 items |
| sa/burnside | card | 0 items |
| tas/glenorchy | card | 0 items |
| tas/kentish | lgasa | 0 items |
| tas/tasman | rss | feed 404 — site removed the feed |
| vic/bayside, buloke, greater-geelong, mansfield, wyndham | curl | 0 items (markup changed) |
| vic/cardinia | rss | feed 403 (WAF on the feed path) |
| wa/harvey, mandurah, subiaco | browser | selector matches 0 items after JS load |
| wa/laverton | catalyst | 403 on /news/ |

Also: nsw/balranald-shire-council passed the rescue but flaked on re-test —
site appears intermittent; new config kept (strictly better).

## Re-running the test

```bash
# Full sweep (≈4 min at concurrency 10, no proxy, no DB needed)
python3 scripts/analysis/test_all_councils_noproxy.py

# One state, no rescue pass
python3 scripts/analysis/test_all_councils_noproxy.py --state sa --no-rescue
```

Run it once from Rakali before the migration cutover — it is the acceptance
test for step 6.
