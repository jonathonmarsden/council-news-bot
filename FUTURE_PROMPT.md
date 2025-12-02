# Future Development Prompt

**Role:** Senior Python Architect & DevOps Engineer
**Project:** Council News Bot (National Scale-Up)
**Current State:** Dockerized, VPS-hosted. Covers VIC/NSW/QLD. **Tasmania (TAS) has been initialized but requires scraper tuning.**

**Objective:** 
Transform the current MVP into a robust, national-scale news aggregation platform covering all ~537 Australian Local Government Areas (LGAs).

**Key Directives:**

1.  **National Expansion (The "Gap Fill"):**
    *   **IMMEDIATE PRIORITY:** Fix the broken scrapers in `states/tas/councils.json`. 9/10 are currently failing (403 Forbidden or 0 items). See `states/tas/README.md` for details.
    *   Complete the Tasmania rollout (remaining 19 councils).
    *   Proceed to **South Australia (68)**, **Western Australia (137)**, and **Northern Territory (17)**.

2.  **Architecture Hardening:**
    *   **Database Migration:** Design a migration plan from SQLite to PostgreSQL to handle concurrent writes from 10+ workers and 500+ councils.
    *   **Config Validation:** Implement a JSON Schema validator for `councils.json` files to prevent typos breaking the bot.
    *   **Error Recovery:** Implement a "Circuit Breaker" for scrapers. If a council fails 5 times in a row, auto-disable it and alert, rather than wasting resources.

3.  **Monitoring & Alerts:**
    *   Convert `health_check.py` into a service that runs daily.
    *   Implement a notification system (Discord Webhook or Email) to alert the admin when:
        *   A scraper finds 0 articles for >30 days.
        *   The VPS disk space is low.
        *   The BlueSky authentication fails.

4.  **Content Intelligence:**
    *   Implement NLP (Natural Language Processing) or simple keyword matching to auto-tag posts with relevant hashtags (e.g., `#RoadWorks`, `#Community`, `#Arts`).
    *   Implement a "Deduplication Fingerprint" to prevent reposting articles if the URL changes slightly but the content is identical.

5.  **Documentation:**
    *   Maintain `AI_CONTEXT.md` as the single source of truth.
    *   Create a `CONTRIBUTING.md` specifically for open-source contributors to add their local council.

**Execution Strategy:**
Work state-by-state, starting with Tasmania (smallest) to validate the new patterns, then moving to SA, WA, and NT.
