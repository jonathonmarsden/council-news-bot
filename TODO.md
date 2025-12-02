# Project TODOs

## 🔴 Critical (Immediate Actions)
- [ ] **Fix Remaining Dead Scrapers**:
    - [x] **Selector Repair**: Applied fixes for ~5 councils. Created `docs/MANUAL_FIXES_REQUIRED.md` for the rest.
    - [ ] **WAF Verification**: Verify that the 173 councils switched to `use_curl` are actually working (wait for next scheduled scrape or run a test batch).
    - [ ] **Manual Review**: Investigate the 2 councils with 404 errors (from `DEAD_SCRAPERS_REPORT.md`).
- [ ] **South Australia Expansion**: Create `states/sa/councils.json` (68 councils).
- [ ] **Western Australia Expansion**: Create `states/wa/councils.json` (137 councils).
- [ ] **Northern Territory Expansion**: Create `states/nt/councils.json` (17 councils).
- [ ] **Bluesky Credentials**: Obtain and configure Bluesky handles/app passwords for TAS, SA, WA, NT, ACT.

## 🟡 Improvements (Robustness)
- [ ] **RSS Migration (Phase 2)**: Run `scripts/analysis/diagnose_scrapers.py` periodically to catch new RSS feeds.
- [ ] **Database Upgrade**: Migrate from SQLite (`bot.db`) to PostgreSQL (Dockerized) to support higher concurrency.
- [ ] **Alerting**: Connect `scripts/maintenance/health_check.py` to a Discord Webhook or Email service for passive monitoring.
- [ ] **Config Validation**: Add a pre-flight check to ensure `councils.json` syntax is valid before starting the scheduler.

## 🟢 Nice to Have (Features)
- [ ] **Auto-Hashtagging**: Use keyword analysis on article titles to add specific tags (e.g., #Library, #Roads).
- [ ] **Web Dashboard**: A simple Flask/FastAPI page to view the status of all 500+ scrapers.
- [ ] **Public API**: Expose the aggregated news feed as a JSON API for other developers.

## 🔵 Maintenance
- [x] **Codebase Cleanup**: Archived debug files, organized `scripts/`.
- [x] **Config Standardization**: Implemented `core/config.py`.
- [x] **Safety Valve**: Implemented `max_per_council` limit.
- [x] **WAF Fixes**: Enabled `curl_cffi` for 173 blocked councils.
- [ ] **Dependency Audit**: Pin versions in `requirements.txt` to ensure long-term stability.
- [ ] **Log Rotation**: Configure Docker logging driver to prevent `scheduler.log` from filling the disk.
