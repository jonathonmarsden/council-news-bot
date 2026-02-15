# Deployment & Architecture Guide

## System Architecture

The Council News Bot operates on a **Local-to-Remote** deployment model.

### Docker Environment
The bot runs in Docker with the following base image:
- **Playwright Image**: `mcr.microsoft.com/playwright/python:v1.58.0-jammy`
  - Includes Python 3.10, pre-installed Playwright browsers (Chrome, Firefox, Safari), and system dependencies.
  - **Note**: Version is pinned to v1.58.0 for stability. Do not update without testing browser-based scrapers first.
- **Python Packages**: All dependencies in `requirements.txt` are pre-installed at build time.

### 1. Local Environment (Your Workspace)
- **Role**: Development, Testing, debugging specific scrapers.
- **Location**: Your local VS Code workspace (e.g., `/Users/jonathonmarsden/projects/council-news-bot`).
- **State**: The "source of truth" for code. All edits happen here.
- **Database**: Local SQLite (`data/bot.db`) is for testing only. It is NOT the production database.

### 2. Remote Production (VPS)
- **Role**: Running the live bot, scheduling posts, hosting the production database.
- **Location**: DigitalOcean Droplet (`170.64.186.16`).
- **User**: `root`.
- **Directory**: `/opt/council-news-bot`.
- **Database**: Production SQLite (`/opt/council-news-bot/data/bot.db`).
- **State**: A mirror of your local code, updated via deployment scripts.

---

## Deployment Process

**CRITICAL**: Modifications to code locally in VS Code DO NOT affect the live bot until you run the deployment script.

### How to Deploy
Run the following command in your local terminal:

```bash
python3 scripts/deployment/deploy_with_password.py
```

### What this script does:
1.  **Syncs Code**: Uses `rsync` to upload your local files to the VPS (excluding `venv`, `.git`, local DB).
2.  **Rebuilds Docker**: Runs `docker compose up -d --build` on the remote server to apply changes.
3.  **Runs Maintenance**: Executes `scripts/maintenance/cleanup_remote_db.py` to sanitize the remote DB post-deploy.

### When to Deploy
- After modifying any Python code (`core/`, `scrapers/`, `main.py`).
- After changing configuration files (`states/**/*.json`).
- After updating `requirements.txt` or `Dockerfile`.

### Validation & Testing
After deployment, verify the fix works by running a test scrape:

```bash
# Quick test of a specific state (limit 1 council to save time)
ssh root@170.64.186.16 'cd /opt/council-news-bot && docker compose run --rm bot python3 main.py --state vic --limit 1 --dry-run'

# Check Discord webhook delivery by monitoring logs
docker compose logs --tail=50 | grep -i discord
```

**Best Practice**: Always test a fix immediately after deployment (same day) before the scheduled cron job runs, to catch issues early.

---

## Troubleshooting

### Checking Remote Logs
To check if the live bot is healthy or seeing errors:

```bash
ssh root@170.64.186.16 'cd /opt/council-news-bot && docker compose logs -f --tail=100'
```

### Verifying Discord Webhook Delivery
Discord summaries are sent via webhook after each scrape. To verify this is working:

```bash
# Run a test scrape and check for Discord webhook calls
ssh root@170.64.186.16 'cd /opt/council-news-bot && docker compose run --rm bot python3 main.py --state nt --limit 1 2>&1 | grep -i "discord\|webhook\|summary"'

# Expected output: "Processing Summary: Found X total" and webhook fire confirmation in logs
```

**Note**: The `discord_logger.py` module includes robust error handling (retry logic, timeouts, 429 rate-limit handling). If a webhook fails, it will retry up to 3 times with exponential backoff before giving up.

### Emergency Operations & Debugging

We have established a suite of scripts in `scripts/deployment/` to help manage the VPS without needing full SSH sessions.

#### 1. Trigger Manual Run
If the scheduler misses a run (e.g., due to downtime), you can force a run for a specific state immediately.

```bash
# Triggers the bot for WA state on the VPS
python3 scripts/deployment/trigger_manual_run.py
```

*Note: This script currently defaults to `--state wa`. Edit the script or argument parsing if you need other states.*

#### 2. Run Remote SQL
To query the production database on the VPS without downloading it:

```bash
# Runs a SQL query against the remote Postgres DB
python3 scripts/deployment/run_sql.py
```

*Note: The actual SQL query is currently hardcoded in the script. Modify the `query` variable in `run_sql.py` to change it.*


### Emergency Stop
If the bot is spamming or misbehaving:

1.  **SSH into the box**: `ssh root@170.64.186.16`
2.  **Stop Docker**: `docker stop council_news_bot`

### Data Integrity
The production database is **persistent** on the VPS. 
- **DO NOT** delete `/opt/council-news-bot/data/bot.db` on the remote server unless you intend to wipe all history.
- The deployment script is configured to **preserve** the remote `data/` folder (it is excluded from rsync deletion).

## Scheduling Architecture: Twice-Daily Scraping (Feb 2026+)

As of February 2026, the bot runs on a **twice-daily schedule** (morning & evening, localized to each state's timezone) instead of continuous 3-hourly scrapes.

### 1. The Idle Container
The main `bot` container in `docker-compose.yml` runs in **idle mode** (`tail -f /dev/null`). This ensures:
- The container is always up.
- The database is accessible.
- We can `exec` into it for debugging.
- It **DOES NOT** run any scraping automatically.

### 2. External Cron (Source of Truth)
All scraping is triggered by the VPS host's `crontab`, which spawns ephemeral commands inside the container.

**New Schedule (Twice-Daily per State):**
```bash
# Morning run (06:00 local per state, reduced concurrency)
0 19 * * * cd /opt/council-news-bot && docker compose run --rm bot python3 main.py --state nsw --concurrency 4 --time-window morning

# Evening run (18:00 local per state, normal concurrency)
0 7 * * * cd /opt/council-news-bot && docker compose run --rm bot python3 main.py --state nsw --concurrency 8 --time-window evening

# Queue processor (every 10 minutes, down from 5)
*/10 * * * * cd /opt/council-news-bot && docker compose run --rm bot python3 scripts/cron/process_global_queue.py
```

### 3. Setting up the Schedule

**To Generate and Deploy the Crontab:**

1. Generate the crontab (accounts for DST and state timezones):
   ```bash
   python3 scripts/deployment/generate_crontab.py --static
   ```

2. SSH into production:
   ```bash
   ssh root@170.64.186.16
   crontab -e
   ```

3. Paste the generated output and save.

4. Verify:
   ```bash
   crontab -l | grep "council-news-bot" | head -5
   ```

**Why this model?**
-   **Reduced Load**: 2 scrapes/day instead of 8 → 75% fewer API calls.
-   **Localized Timing**: Each state scrapes at 06:00 and 18:00 local time (accounts for DST & timezones).
-   **Dynamic Concurrency**: Morning peak (06:00–08:30) uses reduced concurrency to avoid overloading proxies.
-   **Stability**: If NSW crashes, VIC & other states continue unaffected.
-   **Visibility**: `crontab -l` shows exactly when each state runs.

### 4. Key Features

| Feature | Details |
|---------|---------|
| **Time Windows** | Morning 06:00 ± 2h, Evening 18:00 ± 2h (local per state) |
| **State Grouping** | 4 groups of 2 states, staggered to avoid thundering herd |
| **DST Awareness** | Automatically recalculates UTC offsets per state (regen crontab after Oct/Apr) |
| **Dynamic Concurrency** | Morning: 2–4 threads (reduced), Evening: 4–8 threads (normal) |
| **Queue Frequency** | Every 10 minutes (down from 5) to conserve resources |

**For detailed information, see [SCHEDULING_GUIDE.md](SCHEDULING_GUIDE.md).**

### 5. When to Regenerate Crontab

Regenerate and redeploy the crontab **after DST transitions** (first Sunday in April & October):

```bash
# After DST change on VPS (April/October)
python3 scripts/deployment/generate_crontab.py --static
# Then update crontab -e on VPS with new times
```
