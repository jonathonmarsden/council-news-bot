# System Robustness Upgrades (Jan 22, 2026)

## Executive Summary
Following a "Silent Failure" audit, the system has been upgraded to improve transparency, fault tolerance, and observability.

## 1. Transparency: Structured Logging
**Problem**: The application was using `print()` for errors, which were lost in the noise or filtered by the scheduler logger.
**Solution**: Implemented a JSON-ready logging infrastructure (`core.utils.get_logger`). All critical components now log structured events that cannot be accidentally swallowed.

## 2. Fault Tolerance: Zombie Detection
**Problem**: Over 150 scrapers were "Active" but returning 0 articles for days/weeks because of silent selector breakages. The system treated "0 articles" as "Success".
**Solution**:
-   **Schema Change**: Added `consecutive_empty_runs` column to `council_health` table.
-   **Logic Update**: `Database.record_success` now increments this counter on empty yields.
-   **Implication**: We can now programmatically identify scrapers that need attention based on this metric.

## 3. Observability: Automated Health Checks
**Problem**: Detecting these zombies required a manual audit script run via SSH.
**Solution**: Integrated a **Daily Health Check Loop** into `scheduler.py`.
-   Runs `scripts/maintenance/audit_silent_failures.py` every 24 hours.
-   Logs findings to the main system log, ensuring visibility.

## 4. Operational Capability: "Force Fresh"
**Problem**: Fixing a zombie scraper resulted in "0 Posted" because the articles were technically "old" (>7 days).
**Solution**: Added `--force-fresh` flag to `main.py`.
-   **Usage**: `python main.py --state vic --force-fresh`
-   **Result**: Bypasses the 7-day filter, allowing operators to flood the feed with "Backlog" news when a council is brought back online.

## Review of Changes
| Component | Change | Status |
| :--- | :--- | :--- |
| `core/utils.py` | Added `get_logger`, `JsonFormatter` | ✅ Deployed |
| `core/database.py` | Schema migration (`consecutive_empty_runs`) | ✅ Deployed |
| `main.py` | Added `--force-fresh`, `logging` integration | ✅ Deployed |
| `scheduler.py` | Added `health_check_job`, improved error capture | ✅ Deployed |
| `docs/` | Updated Architecture & Troubleshooting | ✅ Complete |
