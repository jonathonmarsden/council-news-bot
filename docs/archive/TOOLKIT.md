# Developer Toolkit

This project includes a suite of maintenance and analysis scripts in the `scripts/` directory.

## Health Auditing
*   `scripts/analysis/audit_config_health.py` - **The Master Audit.** Generates the national coverage table (Enabled/Disabled stats).
*   `scripts/audit_configs.py` - Validates JSON syntax of all `councils.json` files.
*   `scripts/audit_wa_scrapers.py` - Specific deep-dive into WA council health.

## Debugging
*   `scripts/maintenance/health_check.py` - Runs a check against the local `bot.db`.
*   `scripts/maintenance/check_vps_logs.py` - Pulls logs from the remote VPS (requires SSH access).

## Scraper Development
*   `scripts/analysis/find_rss_feeds.py` - Scans council websites for hidden RSS feeds. Use this to "downgrade" fragile card scrapers to robust RSS scrapers.
*   `scripts/test_scraper.py` (or similar) - Use `main.py --council <id> --dry-run` for testing single scrapers.

## Maintenance
*   `scripts/deployment/deploy_to_vps.sh` - The authoritative deployment script.
