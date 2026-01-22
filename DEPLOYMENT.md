# Deployment & Architecture Guide

## System Architecture

The Council News Bot operates on a **Local-to-Remote** deployment model.

### 1. Local Environment (Your Workspace)
- **Role**: Development, Testing, debugging specific scrapers.
- **Location**: Your local VS Code workspace (e.g., `/home/user/projects/council-news-bot`).
- **State**: The "source of truth" for code. All edits happen here.
- **Database**: Local SQLite (`data/bot.db`) is for testing only. It is NOT the production database.

### 3. Immediate Action Required (2026-01-22)
**CRITICAL**: Recent fixes for "Safe Mode" bookmark processing and tag duplication must be deployed.
Run this command from your local terminal now:
```bash
python3 scripts/deployment/deploy_with_password.py
```

### 2. Remote Production (VPS)
- **Role**: Running the live bot, scheduling posts, hosting the production database.
- **Location**: DigitalOcean Droplet (`vps.example.com`).
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
- After updating `requirements.txt`.

---

## Troubleshooting

### Checking Remote Logs
To check if the live bot is healthy or seeing errors:

```bash
ssh root@vps.example.com 'cd /opt/council-news-bot && docker compose logs -f --tail=100'
```

### Emergency Stop
If the bot is spamming or misbehaving:

1.  **SSH into the box**: `ssh root@vps.example.com`
2.  **Stop Docker**: `docker stop council_news_bot`

### Data Integrity
The production database is **persistent** on the VPS. 
- **DO NOT** delete `/opt/council-news-bot/data/bot.db` on the remote server unless you intend to wipe all history.
- The deployment script is configured to **preserve** the remote `data/` folder (it is excluded from rsync deletion).
