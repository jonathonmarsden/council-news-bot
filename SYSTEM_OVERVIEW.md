# Council News Bot - System Overview

**Version:** 2.0 (February 2026)  
**Purpose:** Automated aggregation and publishing of Australian Local Government news  
**Status:** Production (170.64.186.16)  

---

## Tech Stack

### Backend
- **Language:** Python 3.10+
- **Web Scraping:** BeautifulSoup4, curl_cffi, Playwright
- **Database:** PostgreSQL 15 (production), SQLAlchemy ORM
- **Publishing:** ATProto SDK (BlueSky), Discord webhooks
- **Scheduling:** Cron (twice-daily), GitHub Actions (CI/CD)

### Infrastructure
- **Hosting:** DigitalOcean VPS (4GB RAM, Ubuntu)
- **Containerization:** Docker + Docker Compose
- **Version Control:** Git + GitHub
- **CI/CD:** GitHub Actions (test, deploy, rollback, monitoring)
- **Monitoring:** Discord webhooks + daily briefings

### Key Libraries
```
requests>=2.31.0          # HTTP client
beautifulsoup4>=4.12.0    # HTML parsing
atproto>=0.0.55           # BlueSky API
python-dateutil>=2.8.2    # Australian date parsing
curl_cffi>=0.5.10         # CloudFlare bypass
playwright>=1.41.0        # JavaScript rendering
SQLAlchemy>=2.0.0         # Database ORM
alembic>=1.13.0           # Database migrations
psycopg2-binary>=2.9.9    # PostgreSQL driver
pytz>=2024.1              # Timezone handling
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     COUNCIL NEWS BOT                        │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    INPUT LAYER (Sources)                     │
├──────────────────────────────────────────────────────────────┤
│  560+ Australian Council Websites                            │
│  ├─ VIC (79) │ NSW (128) │ QLD (77) │ WA (137) │ SA (68)     │
│  ├─ TAS (29) │ ACT (1)   │ NT (17)                           │
│  └─ Scrapers: BeautifulSoup, Playwright, curl_cffi, RSS      │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│               SCRAPING ENGINE (Core Logic)                   │
├──────────────────────────────────────────────────────────────┤
│  ScraperFactory                                              │
│  ├─ BaseScraper (CSS selectors + date parsing)               │
│  ├─ JsonScraper (API endpoints)                              │
│  ├─ RssScraper (RSS/Atom feeds)                              │
│  ├─ BrowserScraper (Playwright for JS-heavy sites)           │
│  └─ Custom Scrapers (WA councils, special cases)             │
│                                                              │
│  Proxy Layer: Webshare rotating proxy (WAF bypass)           │
│  Rate Limiting: 2s delay, dynamic concurrency (4-8)          │
│  Error Handling: 9 custom exception types                    │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│           DATA PROCESSING & STORAGE (State)                  │
├──────────────────────────────────────────────────────────────┤
│  PostgreSQL Database (council_news)                          │
│  ├─ articles (URL, title, date, excerpt, state, status)      │
│  ├─ scraper_stats (run_at, articles_found, duration)         │
│  └─ council_health (consecutive_failures, last_success)      │
│                                                              │
│  Deduplication: URL-based (primary key)                      │
│  Staleness Filter: Articles >7 days auto-suppressed          │
│  Round-Robin Queue: Varies councils to avoid spam            │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│              PUBLISHING LAYER (Output)                       │
├──────────────────────────────────────────────────────────────┤
│  BlueSky (ATProto)                                           │
│  ├─ 8 state-specific accounts (@vic.councils.lgau.net...)    │
│  ├─ Rate Limit: 24 posts/hour per account                    │
│  ├─ Format: Title + Date + Council + Hashtags + Link         │
│  └─ Posting Window: Every 10 minutes (6 posts/hour)          │
│                                                              │
│  Discord Webhooks                                            │
│  ├─ Logs: Scraper run summaries                              │
│  ├─ Alerts: Critical failures (>3 consecutive)               │
│  └─ Feed: Post confirmation (optional)                       │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│           MONITORING & OPERATIONS (Oversight)                │
├──────────────────────────────────────────────────────────────┤
│  GitHub Actions CI/CD                                        │
│  ├─ Test & Lint (on every push)                              │
│  ├─ Auto-Deploy (after tests pass)                           │
│  ├─ Rollback (1-click revert)                                │
│  └─ Daily Ops (health + backup)                              │
│                                                              │
│  Health Checks                                               │
│  ├─ Daily briefing (success rates, top councils)             │
│  ├─ Broken scrapers report (>3 failures)                     │
│  └─ Database backups (14-day retention)                      │
└──────────────────────────────────────────────────────────────┘
```

---

## Daily Workflow

### **06:00 Local (Morning Scrape)**
```
Cron → main.py --state vic --concurrency 4 --time-window 24h
├─ Scrapes 79 VIC councils (4 concurrent workers)
├─ Finds new articles (avg: 50-150)
├─ Saves to PostgreSQL (deduplicated by URL)
├─ Logs to Discord (summary: found, errors, duration)
└─ Updates scraper_stats table
```

**06:10 Local (Other States):** NSW scrapes (staggered by 10 min)  
**06:20 Local:** QLD, WA, SA, TAS, NT, ACT (staggered)  

**Concurrency:** Morning = 4 workers (gentle load)

---

### **Every 10 Minutes (Posting Loop)**
```
Cron → scripts/cron/process_global_queue.py
├─ Fetches unposted articles (round-robin by council)
├─ Posts to BlueSky (max 3 per run, 18/hr per state)
├─ Marks as posted in database
├─ Respects rate limits (18/hr = 75% of BlueSky 24/hr limit)
└─ Logs success to Discord
```

**States:** Each state has dedicated BlueSky account  
**Cadence:** ~3,456 posts/day across 8 accounts (18/hr × 8 × 24)  

---

### **18:00 Local (Evening Scrape)**
```
Cron → main.py --state vic --concurrency 8 --time-window 6h
├─ Scrapes 79 VIC councils (8 concurrent workers)
├─ Shorter time window (6h since morning run)
├─ Higher concurrency (evening = less traffic)
├─ Finds breaking news from afternoon
└─ Populates posting queue for evening/night
```

**Concurrency:** Evening = 8 workers (aggressive)

---

### **21:00 UTC (~08:00 AEDT - Daily Ops)**
```
GitHub Actions → Ops Monitoring Workflow
├─ Daily Briefing
│   ├─ Last 24h stats (runs, articles, errors)
│   ├─ Top 5 councils by activity
│   ├─ Broken scrapers (>3 failures)
│   └─ Quiet councils (>10 empty runs)
│
├─ Health Report
│   ├─ Generates HEALTH_REPORT.md
│   ├─ Lists stale scrapers (>30 days)
│   └─ Lists dead scrapers (never worked)
│
└─ Database Backup
    ├─ pg_dump to /opt/council-news-bot/backups/
    ├─ Gzip compression
    └─ Auto-prune backups >14 days old
```

**Output:** Discord notifications + GitHub Actions logs

---

## Outputs Summary

| Output Type | Frequency | Destination | Purpose |
|-------------|-----------|-------------|---------|
| **BlueSky Posts** | Every 10 min | 8 state accounts | Public news feed |
| **Scraper Logs** | Twice daily | Discord #logs | Run summaries |
| **Error Alerts** | On failure | Discord #alerts | Critical issues |
| **Daily Briefing** | Once daily | Discord #alerts | 24h health summary |
| **Health Report** | Once daily | VPS file | Dead/stale scrapers |
| **DB Backups** | Once daily | VPS backups/ | Disaster recovery |
| **Deploy Alerts** | On push | Discord #alerts | CI/CD status |

---

## Data Flow (Single Article Lifecycle)

```
1. Council publishes news article on website
   ↓
2. Scraper finds URL during scheduled run (06:00 or 18:00)
   ↓
3. BaseScraper extracts: title, date, URL, excerpt
   ↓
4. Database checks if URL exists (deduplication)
   ↓
5. If new: INSERT with status='new', first_seen_at=now()
   ↓
6. Article sits in posting queue (status='new')
   ↓
7. process_global_queue.py fetches (round-robin)
   ↓
8. Checks staleness (>7 days? suppress)
   ↓
9. Posts to BlueSky ATProto API
   ↓
10. Marks as posted: posted_at=now(), status='posted'
    ↓
11. Discord logs successful post (optional)
```

**Deduplication:** URL is primary key, no duplicates possible  
**Freshness:** Articles >7 days auto-suppressed before posting  
**Rate Limiting:** Max 24 posts/hour per state account  

---

## Performance Characteristics

### Scraping Speed
- **Single council:** 2-5 seconds (avg)
- **Full state (VIC 79):** 4-8 minutes (concurrency=4)
- **All states (560):** ~90 minutes (staggered)

### Throughput
- **Articles found:** 500-2000/day (varies by state)
- **Articles posted:** ~3,456/day (18/hr per state, 75% of BlueSky 24/hr limit)
- **Previous rate:** 144/day (increased Feb 16, 2026 after metrics analysis)
- **Posting queue depth:** 100-500 articles (normal)

### Reliability
- **Success rate:** 95%+ (healthy)
- **Silent failures:** <5% (detected by health checks)
- **Uptime:** 99.5% (Docker restart policy)

### Resource Usage (VPS)
- **CPU:** 10-30% (during scrapes), <5% (idle)
- **Memory:** 1-2GB (normal), 3GB (peak)
- **Disk:** ~500MB code, ~2GB database, ~1GB backups
- **Bandwidth:** ~5GB/month (mostly scraping)

---

## Configuration Management

### State Configs
```
states/{state_code}/councils.json
├─ id: Unique council identifier
├─ name: Display name
├─ news_url: Target URL to scrape
├─ scraper: Scraper type (base, rss, json, browser)
├─ selectors: CSS selectors for extraction
│   ├─ item_selector: Container for each article
│   ├─ link_selector: <a> tag (relative to item)
│   ├─ title_selector: Headline text
│   ├─ date_selector: Publication date
│   └─ excerpt_selector: Summary text (optional)
└─ enabled: Boolean (active/inactive)
```

**Example:**
```json
{
  "id": "melbourne",
  "name": "City of Melbourne",
  "news_url": "https://melbourne.vic.gov.au/news-and-media",
  "scraper": "base",
  "selectors": {
    "item_selector": ".news-item",
    "link_selector": "a.title",
    "title_selector": "h3",
    "date_selector": ".date"
  },
  "enabled": true
}
```

---

## Deployment Architecture

### Production Environment
```
VPS: 170.64.186.16 (DigitalOcean)
├─ Docker Compose
│   ├─ council_news_bot (app container)
│   └─ council_db (PostgreSQL 15)
│
├─ Cron Jobs (on host)
│   ├─ Scraping (twice-daily per state)
│   └─ Posting (every 10 minutes)
│
└─ GitHub Actions (remote)
    ├─ Test & Lint (on push)
    ├─ Auto-Deploy (after tests pass)
    ├─ Rollback (manual trigger)
    └─ Daily Ops (scheduled)
```

### CI/CD Pipeline
```
Local → GitHub → Actions → VPS

1. Developer pushes code
   ↓
2. GitHub Actions runs tests (pytest, flake8, mypy)
   ↓
3. If tests pass → Deploy workflow triggers
   ↓
4. Rsync code to VPS (excludes .env, data/)
   ↓
5. Docker rebuild (docker compose up -d --build)
   ↓
6. Post-deploy health check
   ↓
7. Discord notification (success/failure)
```

**Rollback:** Revert to previous commit via GitHub Actions (1-click)

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **PostgreSQL over SQLite** | Concurrent access, better performance at scale |
| **Twice-daily scraping** | Balances freshness vs server load |
| **Staggered state scrapes** | Prevents thundering herd on proxy |
| **Round-robin posting** | Varies content, avoids council spam perception |
| **7-day staleness filter** | Keeps feed current, auto-cleans queue |
| **ATProto (BlueSky)** | Open protocol, better API than Twitter |
| **Docker containers** | Reproducible deploys, resource limits |
| **GitHub Actions CI/CD** | Free tier, integrated with repo |
| **Discord webhooks** | Real-time alerts, no separate monitoring service |
| **CSS selectors over XPath** | More maintainable, simpler debugging |

---

## Operational Commands

### Local Development
```bash
# Run single council (dry-run)
python main.py --state vic --council melbourne --dry-run

# Run full state
python main.py --state vic --concurrency 4

# Post from queue
python scripts/cron/process_global_queue.py

# Health check
python scripts/maintenance/health_check.py
```

### Production Operations
```bash
# Check VPS status
ssh root@170.64.186.16 "cd /opt/council-news-bot && docker compose ps"

# View logs
ssh root@170.64.186.16 "cd /opt/council-news-bot && docker compose logs --tail=100 bot"

# Manual deploy
bash scripts/deployment/deploy_to_vps.sh

# Database backup
ssh root@170.64.186.16 "cd /opt/council-news-bot && docker compose exec db pg_dump -U councilbot council_news > backup.sql"
```

### CI/CD Operations
```bash
# Push to deploy
git push origin master
# → Tests run → Auto-deploy (if green)

# Rollback (via GitHub Actions UI)
# Actions → Rollback → Run workflow → (leave commit empty)

# Manual deploy (bypass tests)
# Actions → Deploy to VPS → Run workflow
```

---

## Security & Secrets

### Environment Variables (.env)
```bash
# BlueSky Publishing
BSKY_HANDLE_VIC=vic.councils.lgau.net
BSKY_PASSWORD_VIC=***
# (repeat for NSW, QLD, WA, SA, TAS, ACT, NT)

# Database
DATABASE_URL=postgresql://councilbot:***@db:5432/council_news

# Proxy
PROXY_URL=http://bgytwxqn-rotate:***@p.webshare.io:80

# Discord
DISCORD_WEBHOOK_ALERTS=https://discord.com/api/webhooks/***
DISCORD_WEBHOOK_LOGS=https://discord.com/api/webhooks/***
```

### GitHub Secrets
```
VPS_HOST=170.64.186.16
VPS_USER=root
VPS_SSH_KEY=(deploy_key private key)
DISCORD_WEBHOOK_ALERTS=(webhook URL)
```

---

## Documentation Index

| Document | Purpose |
|----------|---------|
| **README.md** | Project overview, quick start |
| **SYSTEM_OVERVIEW.md** (this doc) | Architecture & tech stack |
| **.github/CI_CD_GUIDE.md** | CI/CD operations |
| **docs/operations/RUNBOOK.md** | Daily operations manual |
| **docs/operations/MONITORING.md** | Health checks & alerting |
| **docs/operations/TROUBLESHOOTING.md** | Problem resolution |
| **docs/architecture/SYSTEM_DESIGN.md** | Detailed design decisions |
| **SCHEDULING_GUIDE.md** | Twice-daily schedule explanation |
| **PHASE_1_COMPLETION.md** | Code professionalization report |
| **PHASE_2_COMPLETION.md** | Operations docs added |

---

## Success Metrics

### Scraping Health
- ✅ 95%+ success rate
- ✅ <5% silent failures
- ✅ Average 500-2000 articles/day

### Publishing Health
- ✅ 3,456 posts/day (18/hr per state, 75% BlueSky capacity)
- ✅ 100% post success (BlueSky uptime)
- ✅ <500 article backlog

### System Health
- ✅ 99.5% uptime
- ✅ Daily backups completing
- ✅ Discord alerts working
- ✅ No manual interventions needed

---

**System Status:** 🟢 Production  
**Last Deploy:** 2026-02-15 (Auto-deployed via CI/CD)  
**Next Review:** Phase 3 (code refactoring, optional)  

---

*For operational questions, see [docs/operations/RUNBOOK.md](docs/operations/RUNBOOK.md)*  
*For troubleshooting, see [docs/operations/TROUBLESHOOTING.md](docs/operations/TROUBLESHOOTING.md)*
