# Project TODOs

## 🔴 Critical (Immediate Actions)
- [ ] **Western Australia Expansion**: Create `states/wa/councils.json` (137 councils).
- [ ] **Final Verification**: Ensure all 8/8 states are posting successfully.

## 🟡 Improvements (Robustness)
- [ ] **RSS Migration (Phase 2)**: Run `scripts/analysis/diagnose_scrapers.py` periodically to catch new RSS feeds.
- [ ] **Database Upgrade**: Migrate from SQLite (`bot.db`) to PostgreSQL (Dockerized) to support higher concurrency.
- [ ] **Alerting**: Connect `scripts/maintenance/health_check.py` to a Discord Webhook or Email service for passive monitoring.
- [x] **Config Validation**: Added `scripts/audit_configs.py`.

## 🟢 Nice to Have (Features)
- [ ] **Auto-Hashtagging**: Use keyword analysis on article titles to add specific tags (e.g., #Library, #Roads).
- [ ] **Web Dashboard**: A simple Flask/FastAPI page to view the status of all 500+ scrapers.
- [ ] **Public API**: Expose the aggregated news feed as a JSON API for other developers.

## 🔵 Maintenance
- [x] **Codebase Cleanup**: Archived debug files, organized `scripts/`.
- [x] **Config Standardization**: Implemented `core/config.py`.
- [x] **Safety Valve**: Implemented `max_per_council` limit.
- [x] **WAF Fixes**: Enabled `curl_cffi` for blocked councils.
- [ ] **Dependency Audit**: Pin versions in `requirements.txt` to ensure long-term stability.
- [ ] **Log Rotation**: Configure Docker logging driver to prevent `scheduler.log` from filling the disk.
