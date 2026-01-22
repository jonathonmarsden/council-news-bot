# Hidden Risks & Assumptions Analysis
**Date:** 21 January 2026

## 1. The "Starvation" Risk (Confirmed)
*   **The Problem:** `scheduler.py` imposes a hard **600-second (10 minute)** timeout on each state's scraping job.
*   **The Math:** 
    *   NSW has 128 councils. 
    *   Concurrency is set to 2 to protect the small VPS.
    *   This results in ~64 serial batches.
    *   `600s / 64 batches` = **9.3 seconds per batch**.
*   **The Consequence:** If valid processing takes > 9.3s per batch (highly likely with rotating proxies, WAF challenges, or slow servers), the process is `killed` before it finishes.
*   **The Victim:** Councils starting with **S, T, U, V, W, Y, Z** in NSW and WA are at high risk of never being scraped ("Starvation"), while "A" councils are scraped every time.
*   **Fix Required**: Increase scheduler timeout to 1200s (20 mins) for large states, or shuffle the council list before processing.

## 2. The "Zombie Scraper" Risk
*   **The Problem:** We rely on `card_scraper` using generic CSS selectors.
*   **The Evidence:** 
    *   Inner West (NSW), Flinders (TAS), Wodonga (VIC) use `h2` as a title selector.
    *   If the site layout changes slightly (e.g., a new "Sidebar" with `<h2>Subscribe</h2>` appears), the scraper might start ingesting garbage titles.
*   **Detection**: We have no validation that the "Title" looks like a title (length check, ban list like "Subscribe", "Home").

## 3. Deployment Fragility
*   **The Problem:** Deployment is manual (`rsync` script).
*   **The Risk**: If the VPS is rebooted or rebuilt, we rely on the local developer having the "latest" version of the code *and* the `.env` file. There is no "source of truth" regarding the `.env` file configuration on the server.
*   **Mitigation**: The `.env` file should be documented or templated more rigorously.

## 4. Single-Point-of-Failure: OpenCities
*   **The Problem:** 42 councils use `OpenCitiesScraper`.
*   **The Risk**: A single global update by the vendor (Granicus) could break 8% of the national grid instantly.

## 5. Duplicate Configs
*   **Finding:** TAS has a redundant `config.json` alongside `councils.json`. This confuses the architecture (which file is the truth?).

## 6. Recommendations
1.  **Immediate**: Bump `scheduler.py` timeout to 1800s (30m).
2.  **Immediate**: Implement `random.shuffle(councils)` in `main.py` so starvation is distributed, not targeted at "Z-councils".
3.  **Maintenance**: Delete `states/tas/config.json`.
