# Project TODOs

## 🔴 Critical (Immediate Actions)
- [x] **Tasmania Expansion**: 
    - [x] Create `states/tas/councils.json` (29/29 added).
    - [x] Fix scrapers for initial batch (Hobart, Launceston, etc.).
    - [x] Configure selectors for remaining 19 councils.
- [ ] **Fix Hard Nuts (WAF/Broken)**:
    - [ ] **Bass Coast (VIC)**: WAF blocking (403). `curl_cffi` failed.
    - [ ] **Blue Mountains (NSW)**: WAF blocking (403). `curl_cffi` failed.
    - [ ] **Liverpool (NSW)**: WAF blocking (403). `curl_cffi` failed.
    - [ ] **Ballarat (VIC)**: Selectors broken (200 OK).
    - [ ] **Brisbane (QLD)**: Selectors broken (200 OK).
    - [ ] **Gold Coast (QLD)**: Selectors broken (200 OK).
    - [ ] **Cumberland (NSW)**: Selectors broken (200 OK).
- [ ] **South Australia Expansion**: Create `states/sa/councils.json` (68 councils).
- [ ] **Western Australia Expansion**: Create `states/wa/councils.json` (137 councils).
- [ ] **Northern Territory Expansion**: Create `states/nt/councils.json` (17 councils).
- [x] **ACT Expansion**: Create `states/act/councils.json` (1 council).
- [ ] **Bluesky Credentials**: Obtain and configure Bluesky handles/app passwords for TAS, SA, WA, NT, ACT.

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
