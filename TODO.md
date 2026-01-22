# Project TODOs

## 🔴 Critical (Immediate Actions)
- [x] **Operation "Revive SA"**: Fixed 35 SA councils (Impersonation + Selector Update).
- [x] **Core Logic Fix**: Fixed False Positive Cloudflare detection in `base.py` (caused by CDNJS scripts).
- [ ] **Data Quality**: Monitor redirect URLs from new SA platform (ensure no duplicate spam).
- [x] **Zombie Scraper Recovery**: Fixed Ballarat (Core Bug) and SA Cluster (Selector Bug). Pending: Wollongong.
- [ ] **monitor_waf_fixes**: Verify successful parsing for Vincent and Burwood in VPS logs.
- [ ] **Phase 3 (Western Expansion)**:
    - [ ] Run coverage audit for WA.
    - [ ] Create Batch 1 of missing councils.
    - [ ] Implement fixes.

## 🟡 Improvements (Robustness)
- [ ] **RSS Migration (Phase 2)**: Run `scripts/analysis/diagnose_scrapers.py` periodically to catch new RSS feeds.
- [ ] **Database Upgrade**: Migrate from SQLite (`bot.db`) to PostgreSQL (Dockerized) to support higher concurrency.
- [ ] **Alerting**: Connect `scripts/maintenance/health_check.py` to a Discord Webhook or Email service for passive monitoring.
- [x] **Config Validation**: Added `scripts/audit_configs.py`.
- [x] **Doc Review**: Updated DEPLOY, ARCHITECTURE, and README docs to match reality.

## 🟢 Nice to Have (Features)
- [ ] **Auto-Hashtagging**: Use keyword analysis on article titles to add specific tags (e.g., #Library, #Roads).
- [ ] **Web Dashboard**: A simple Flask/FastAPI page to view the status of all 500+ scrapers.
- [ ] **Public API**: Expose the aggregated news feed as a JSON API for other developers.
- [ ] **Consolidate Scrapers**: Migrate discovered WordPress sites from `card_scraper` to `wordpress_scraper` or `rss_scraper`.
- [ ] **Vendor Scrapers**: Build `AlykaScraper` for the WA Kentico cluster.
- [x] **Scheduler Tuning**: Increased posting throughput to 10/run and documented constraints.
- [ ] **Scheduler Tuning**: Increase timeout for NSW/WA or randomize council order to prevent "Z-starvation" due to 600s timeout.

## 🔵 Maintenance
- [x] **Codebase Cleanup**: Archived debug files, organized `scripts/`.
- [x] **Config Standardization**: Implemented `core/config.py`.
- [x] **Safety Valve**: Implemented `max_per_council` limit.
- [x] **WAF Fixes**: Enabled `curl_cffi` for blocked councils.
- [x] **Logging**: Implemented structured JSON logging.
- [x] **Health Check**: Added daily "Zombie Audit" to scheduler.
- [x] **Circuit Breaker**: Added `consecutive_empty_runs` tracking.
- [ ] **Dependency Audit**: Pin versions in `requirements.txt` to ensure long-term stability.
- [ ] **Log Rotation**: Configure Docker logging driver to prevent `scheduler.log` from filling the disk.
