# TODO

## Future Roadmap (Mid-2026)
- [ ] **Phase 3: Interactive Discord Console** (See 2026-01-25 Conversation)
    - [ ] Create persistent listener bot (`discord.py`) in Docker.
    - [ ] Implement commands: `/status`, `/check <council>`, `/deploy`.
    - [ ] Replace "Living Status Board" message instead of daily logs.

## High Priority
- [ ] **Implement Browser-Based Scraper (Playwright/Selenium)**
    - [ ] Create `core/scrapers/browser_scraper.py`.
    - [ ] Update `Dockerfile` to include browser binaries.
    - [ ] Test with Armadale (WA).
- [ ] **Audit for CSR Sites**
    - [ ] Run a script to check `debug_*.html` files for "BAILOUT_TO_CLIENT_SIDE_RENDERING".
    - [ ] Check `councils.json` for other "Contentful" or "Next.js" notes.

## Maintenance
- [ ] Refactor broken scrapers in `DEAD_SCRAPERS_REPORT.md`.
    - [x] Auto-Fix: Switched 35 councils to RSS.
    - [x] **NSW Silent Failures Phase**: Fixed 11/11 councils returning 0 articles (Lockhart, Bogan, etc.).
    - [x] **WA Silent Failures Phase**: Fixed Datascape (Manjimup/etc) and Alyka (Harvey/Mandurah) sites.
    - [ ] Investigation: WAF Blocked (403) - confirm if curl/browser needed.
    - [ ] Investigation: 404/Connection Errors.
- [ ] Complete "Risky Selector" remediation.
