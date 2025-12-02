# Project TODOs

## 🔴 Critical (Immediate Actions)
- [ ] **Tasmania Expansion**: 
    - [x] Create `states/tas/councils.json` (10/29 added).
    - [ ] Fix scrapers for initial batch (Hobart, Launceston, etc.).
    - [ ] Add remaining 19 councils.
- [ ] **South Australia Expansion**: Create `states/sa/councils.json` (68 councils).
- [ ] **Western Australia Expansion**: Create `states/wa/councils.json` (137 councils).
- [ ] **Northern Territory Expansion**: Create `states/nt/councils.json` (17 councils).

## 🟡 Improvements (Robustness)
- [ ] **RSS Migration**: Run `scripts/find_rss_feeds.py` against NSW and QLD to switch eligible councils to `rss_scraper`.
- [ ] **Database Upgrade**: Migrate from SQLite (`bot.db`) to PostgreSQL (Dockerized) to support higher concurrency.
- [ ] **Alerting**: Connect `scripts/health_check.py` to a Discord Webhook or Email service for passive monitoring.
- [ ] **Config Validation**: Add a pre-flight check to ensure `councils.json` syntax is valid before starting the scheduler.

## 🟢 Nice to Have (Features)
- [ ] **Auto-Hashtagging**: Use keyword analysis on article titles to add specific tags (e.g., #Library, #Roads).
- [ ] **Web Dashboard**: A simple Flask/FastAPI page to view the status of all 500+ scrapers.
- [ ] **Public API**: Expose the aggregated news feed as a JSON API for other developers.

## 🔵 Maintenance
- [ ] **Dependency Audit**: Pin versions in `requirements.txt` to ensure long-term stability.
- [ ] **Log Rotation**: Configure Docker logging driver to prevent `scheduler.log` from filling the disk.
