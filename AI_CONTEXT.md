# AI Context & Handover Guide

## 🚩 Mission Statement
To create a comprehensive, automated news aggregation service for every Local Government Area (LGA) in Australia (~540 councils). The bot scrapes news, normalizes it, and publishes it to the BlueSky social network to ensure democratic transparency.

## 🧠 System Context
This project is a Python-based scraping pipeline running on a DigitalOcean VPS (Dockerized).

### Key Components
- **Orchestrator**: `scheduler.py` runs the main loop (scrapes all states, then posts updates).
- **Configuration**: JSON files in `states/{state_code}/councils.json` define the rules for each council.
- **Engine**: `core/scrapers/` contains the logic. `CardScraper` is the workhorse.
- **WAF Defense**: We use `curl_cffi` and rotating proxies to bypass Cloudflare/Incapsula.

## 🛡️ The "WAF War" (Phase 2 Complete)
We have successfully developed a methodology to bypass sophisticated Anti-Bot protections found on major council sites (e.g., Adelaide, Vincent, Ballarat).

### The Recipe
If a council returns 403 Forbidden or 0 articles (Silent Block):
1.  **Tool**: Use `scripts/debug/research_waf_bypass.py` on the VPS.
2.  **Config**: The winning combo is usually:
    ```json
    "use_curl": true,
    "use_rotating_proxy": true,
    "impersonate": "chrome124"
    ```
3.  **Deployment**: Update `councils.json` locally -> `deploy_to_vps.sh` (or manual SCP) -> `docker restart council_news_bot`.

## 🗺️ Current Status (Jan 2026)
- **Coverage**: 8/8 States & Territories active.
- **Health**: Phase 1 (Stability) & Phase 2 (WAF) are complete.
- **Focus**: Phase 3 "Western Expansion" (Filling gaps in WA).

## 📂 Key Files for AI Agents
- `docs/ARCHITECTURE.md`: Technical system design.
- `docs/WAF_STRATEGY.md`: Detailed WAF bypass protocols.
- `docs/reports/INCIDENT_MALFORMED_TITLES_2026_01_22.md`: Incident analysis of WA malformed posts.
- `TODO.md`: Priority queue.
- `states/wa/recovery_plan.md`: The roadmap for Western Australia.

## 🔄 Deployment Cheatsheet
- **Deploy Code**: `scp ...` to `root@170.64.186.16:/opt/council-news-bot/...`
- **Restart Scraper**: `ssh root@170.64.186.16 "docker restart council_news_bot"`
- **Check Logs**: `ssh root@170.64.186.16 "docker logs --tail 100 council_news_bot"`
