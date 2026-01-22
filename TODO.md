# Project Roadmap 2026

## 🔴 Phase 2: Targeted Recovery (Q1 2026)
*Focus: Addressing "Risky Selectors" and remaining WAF blocks.*

### Priority 1: Risky Selectors Audit (Active)
*Ref: [RISKY_SELECTORS_REPORT.md](RISKY_SELECTORS_REPORT.md)*
- [x] **Western Australia:** Albany & Bridgetown-Greenbushes verified and fixed.
- [ ] **Tasmania:** Audit Hobart, Launceston, Burnie (OpenCities cluster).
- [ ] **Victoria:** Audit Whitehorse, Wodonga, Greater Dandenong.
- [ ] **NT:** Audit Katherine, MacDonnell.

### Priority 2: Western Australia (33 Failures) - CLOSED
- [x] **Triage:** Completed.
- [x] **Platform Migration:** 77 Shires moved to `CatalystScraper`.
- [x] **Alyka/Kentico:** Swan, Rockingham, Stirling, Belmont fixed with custom scrapers/APIs.
- [ ] **Armadale:** (Deferred) Requires Playwright due to React Server Components.

### Priority 3: NSW & QLD (24 Failures Combined)
- [ ] **Bot Protection Check:** Test strict WAF failures with `curl_impersonate` options.
- [ ] **Selector Audit:** Review the 16 NSW failures for common layout changes.

## 🟡 Phase 3: Infrastructure & Stability
- [ ] **Continuous monitoring:** Integrate `scripts/comprehensive_health_check.py` into a weekly CI/CD or cron job.
- [ ] **Database Migration:** Prepare for migration from SQLite to PostgreSQL for better concurrency.
- [ ] **Dashboard:** Create a simple HTML/JSON dashboard to visualize the `HEALTH_CHECK_REPORT_2026.md` data dynamically.

## 🟢 Maintenance & Refinement
- [x] **Global Health Check:** Completed Jan 22, 2026 (87.2% Healthy).
- [ ] **Dependency Lock:** Freeze `requirements.txt` to known stable versions.
- [ ] **Logging:** Implement log rotation for `scheduler.log`.

---
*See [GLOBAL_HEALTH_AUDIT_2026.md](GLOBAL_HEALTH_AUDIT_2026.md) for the latest detailed breakdown.*
