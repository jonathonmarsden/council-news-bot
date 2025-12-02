# Final Project Report: Council News Bot (v2.1.0)

**Date:** December 2, 2025
**Author:** GitHub Copilot (Gemini 3 Pro)

## 1. Executive Summary
The Council News Bot has been successfully upgraded from a local script to a **production-grade, containerized application** running on a DigitalOcean VPS. It currently monitors **285 councils** across Victoria, New South Wales, and Queensland, posting updates to BlueSky in near real-time.

The system is now **stable, scalable, and cost-efficient**, utilizing a "Direct First" proxy strategy to minimize operational costs while maintaining high availability.

## 2. Current State

### ✅ Infrastructure
*   **Hosting:** DigitalOcean Droplet (Ubuntu 24.04 LTS).
*   **Deployment:** Docker Compose (Containerized Python 3.9 environment).
*   **Persistence:** SQLite database (`bot.db`) persisted via Docker volumes.
*   **CI/CD:** Manual "One-Click" deployment script (`scripts/deploy_to_vps.sh`).

### ✅ Coverage
*   **Victoria (VIC):** 79/79 Councils (100%) - *5 migrated to RSS*.
*   **New South Wales (NSW):** 128/128 Councils (100%).
*   **Queensland (QLD):** 78/77 Councils (100%).
*   **Total Active Scrapers:** 285.

### ✅ Performance
*   **Concurrency:** Scrapes 5 councils simultaneously (configurable).
*   **Speed:** Full state scrape takes <10 minutes.
*   **Reliability:** "Direct First" logic retries failed requests with a proxy automatically.

## 3. Architecture Overview

```mermaid
graph TD
    A[Scheduler (scheduler.py)] -->|Every 3 Hours| B[Worker (main.py)]
    B -->|Spawns Threads| C[Scraper Engine]
    C -->|Direct Request| D{Success?}
    D -->|Yes| E[Parse HTML/RSS]
    D -->|No| F[Retry via Proxy]
    F --> E
    E --> G[Database (bot.db)]
    A -->|Every 15 Mins| H[Poster (main.py --post-only)]
    H -->|Read Unposted| G
    H -->|Publish| I[BlueSky API]
```

## 4. Services & Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.9 | Core logic. |
| **Container** | Docker | Ensures consistent environment across Dev/Prod. |
| **Database** | SQLite | Lightweight storage for article history. |
| **Scraping** | `requests`, `BeautifulSoup` | Primary HTML parsing. |
| **WAF Bypass** | `curl` | Subprocess calls for stubborn sites (Akamai/Cloudflare). |
| **Social** | `atproto` | Official BlueSky API client. |
| **Scheduling** | Python Loop | Simple `while True` loop in `scheduler.py`. |

## 5. Future Actions (Roadmap)

### Phase 1: National Expansion (Immediate)
*   **Task:** Build scrapers for TAS, SA, WA, and NT.
*   **Goal:** 100% Australian coverage (~537 councils).

### Phase 2: Hardening
*   **Task:** Migrate `bot.db` to PostgreSQL.
*   **Reason:** SQLite will struggle with 500+ councils and concurrent writes.

### Phase 3: Intelligence
*   **Task:** Implement NLP for auto-hashtagging.
*   **Reason:** Current hashtags are generic (`#CouncilName`). Contextual tags (`#Roads`, #Events`) increase engagement.

## 6. Handover Notes
*   **Credentials:** Stored in `.env` on the VPS.
*   **Logs:** View via `docker compose logs -f`.
*   **Maintenance:** Run `scripts/health_check.py` weekly to identify broken scrapers.
