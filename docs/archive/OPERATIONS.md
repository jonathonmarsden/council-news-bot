# Operations Guide

This guide covers the day-to-day operations, maintenance, and troubleshooting of the Council News Bot.

## 1. Debugging Scrapers

When a council scraper is failing or returning 0 articles, follow these steps.

### Using `debug_batch.py`
This is the primary tool for debugging. It fetches the HTML, saves it for inspection, and runs the scraper logic.

```bash
# Debug specific councils
python3 scripts/maintenance/debug_batch.py --councils warrnambool ballarat

# Debug a specific state's empty councils
python3 scripts/maintenance/debug_batch.py --state vic --empty-only
```

**Output:**
- HTML files are saved to `debug_html/` (e.g., `debug_html/warrnambool.html`).
- The script prints whether it found articles, and if so, how many.

### Using `debug_warrnambool.py` (WAF Testing)
If a site is returning 403 Forbidden, use this script to test different `curl_cffi` impersonation profiles.

```bash
python3 scripts/maintenance/debug_warrnambool.py
```
*Note: You may need to modify this script to target a different URL.*

### Common Issues & Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| **WAF Block** | Status 403, "Access Denied" in HTML | Set `"use_curl": true` and `"impersonate": "chrome120"` in `councils.json`. |
| **Broken Selectors** | Status 200, but 0 articles found | Inspect `debug_html/council.html`. Update `item_selector`, `title_selector`, etc. |
| **Changed URL** | Status 404 | Find the new news URL and update `news_url` in `councils.json`. |

## 2. Maintenance

### Identifying "Empty" Councils
The bot now uses a "Record Everything" strategy. It logs stats to the `scraper_stats` table.

To find councils that are consistently returning 0 articles:

```bash
# Run the daily health check
python3 scripts/maintenance/daily_health_check.py
```

This will generate `HEALTH_REPORT.md` with a list of broken/empty scrapers.

### Adding a New Council
1.  Add the entry to `states/{state}/councils.json`.
2.  Run a dry-run debug to verify:
    ```bash
    python3 main.py --council new-council-id --dry-run
    ```
3.  Commit and deploy.

## 3. Deployment

The bot runs on a DigitalOcean VPS. Deployment is automated via script.

### Prerequisites
- SSH access to the VPS (`root@170.64.186.16`).
- `deploy_secrets.py` configured (if updating secrets).

### Deploying Code Updates
```bash
# 1. Commit your changes
git add .
git commit -m "Fix: Updated selectors for X"
git push origin master

# 2. Run the deploy script
python3 scripts/deployment/deploy_with_password.py
```

This script will:
1.  SSH into the VPS.
2.  Pull the latest code.
3.  Rebuild the Docker image.
4.  Restart the container.

### Viewing Logs
To check the live logs on the VPS:

```bash
ssh root@170.64.186.16
cd /opt/council-news-bot
docker compose logs -f --tail=100
```

## 4. Database Management

The database is a SQLite file (`bot.db`) stored in a Docker volume on the VPS.

### Querying Stats
You can query the database directly on the VPS:

```bash
# SSH into VPS
ssh root@170.64.186.16

# Open Database
sqlite3 /opt/council-news-bot/bot.db

# Example: Check recent stats
SELECT council_id, articles_found, status, duration_ms 
FROM scraper_stats 
ORDER BY run_at DESC 
LIMIT 10;

# Example: Check for empty runs
SELECT council_id, count(*) as empty_runs 
FROM scraper_stats 
WHERE articles_found = 0 
GROUP BY council_id 
ORDER BY empty_runs DESC;
```

### Backups
The database is critical. To back it up locally:

```bash
scp root@170.64.186.16:/opt/council-news-bot/bot.db ./backup_bot.db
```
