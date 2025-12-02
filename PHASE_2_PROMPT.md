# Phase 2: Optimization, Cleanup & Robustness

**Role**: DevOps & Python Expert
**Goal**: Transition the `council-news-bot` from a "working prototype" to a "robust production system".

## Objectives

### 1. 🧹 Codebase Cleanup & Restructuring
- **Archive Clutter**: Move all `debug_*.py`, `debug_*.html`, and `test_*.py` files from the root to `_archived_old_code/` or a new `tests/manual/` directory.
- **Organize Scripts**: Categorize `scripts/` into subfolders (e.g., `scripts/maintenance`, `scripts/deployment`, `scripts/analysis`, `scripts/one_off`).
- **Standardize Config**: Ensure ALL scripts use `os.environ.get('DB_PATH')` and `dotenv` consistently. Fix the Local vs VPS `bot.db` path discrepancy.

### 2. 🛡️ Safety & Flood Control
- **Rate Limiting**: Implement a global or per-council "Max Posts Per Run" limit in `scheduler.py` or `poster.py` to prevent flooding (e.g., the Warren Shire 92-article backlog).
- **Backlog Management**: Create a script to "mark as posted" (skip) old backlog items without posting them to Bluesky.

### 3. 🩺 Scraper Diagnosis & Repair (The "145 Dead")
- **Automated Diagnosis**: Create a `diagnose_scrapers.py` tool that iterates through the "Dead" councils and checks:
    - Is the URL 404?
    - Do the selectors match 0 items?
    - Is it WAF blocked (403)?
- **RSS Migration**: Prioritize switching broken HTML scrapers to RSS feeds where available (using `find_rss_feeds.py` logic).

### 4. 📚 Documentation
- **Update README**: Reflect the new folder structure.
- **Developer Guide**: Document how to add a new council, how to debug a specific scraper, and how to deploy.

## Immediate Task
Start with **Objective 1 (Cleanup)** and **Objective 2 (Safety)**.
1. Clean up the root directory.
2. Implement the "Max Posts" safety valve.
