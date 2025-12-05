# Project Consolidation and Codebase Cleanup Prompt

**Context:**
The Council News Bot project has reached a major milestone: 7 out of 8 Australian states/territories (ACT, NSW, NT, QLD, SA, TAS, VIC) are now fully supported and running in production. The codebase has evolved rapidly during this rollout, resulting in the accumulation of temporary debug scripts, HTML dumps, ad-hoc maintenance tools, and potential technical debt.

**Objective:**
Transition the project from "rapid development" mode to "stable production" mode. The goal is to consolidate the codebase, ensure it meets professional open-source standards, and prepare it for the final state (WA) implementation.

**Instructions for the AI Agent:**

Please perform a comprehensive consolidation of the workspace following these steps:

### 1. Workspace Cleanup (High Priority)
*   **Audit File Structure**: Scan the root directory and `scripts/` folder.
*   **Identify Temporary Files**: Locate files that appear to be one-off debug scripts (e.g., `debug_*.py`, `debug_*.html`, `fix_*.py`, `check_*.py` that aren't part of the core monitoring suite).
*   **Action**:
    *   Move confirmed obsolete scripts to an `_archived_old_code/` directory (or delete them if they are clearly junk like `temp.py`).
    *   Remove any `debug_*.html` files (these are just scraper artifacts).
    *   Ensure `council_news.db` and other runtime artifacts are properly ignored in `.gitignore`.

### 2. Documentation Standardization
*   **README.md**:
    *   Update the project status to reflect 7/8 states supported.
    *   Ensure the "Supported States" table is accurate.
    *   Verify that setup/installation instructions match the current Docker/VPS deployment process.
*   **ARCHITECTURE.md**:
    *   Update this document to accurately describe the current modular structure (the `states/` directory pattern, `ScraperFactory`, `CardScraper`, etc.).
*   **Code Documentation**:
    *   Review core files (`core/scrapers/*.py`, `core/database.py`, `main.py`, `scheduler.py`).
    *   Ensure all classes and public methods have clear, professional docstrings (Google or NumPy style).
    *   Add type hinting where missing.

### 3. Configuration & Code Consistency
*   **Config Audit**: Check all `states/*/councils.json` files.
    *   Ensure consistent formatting (indentation, key ordering).
    *   Verify that the `enabled` flag is present and correctly set for all councils.
*   **Code Review**:
    *   Look for duplicated logic between state-specific scripts or scrapers.
    *   Check for any hardcoded paths that should be relative or env-var driven.

### 4. Final Verification
*   After cleanup, run a "dry run" or a health check script to ensure that moving/deleting files hasn't broken the core application or the deployment scripts.
*   Verify that the Docker build process still works (check `Dockerfile` and `docker-compose.yml` against the cleaned file structure).

**Deliverable:**
A clean, well-documented repository ready for the final push (WA) and public release.
