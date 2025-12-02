# Project Handover - 1 Dec 2025 (VPS Migration)

## 🟢 Current Status
- **Bot Status**: ✅ **RUNNING ON VPS** (DigitalOcean, Sydney)
- **IP Address**: `vps.example.com`
- **Service**: Managed by `systemd` (auto-restarts on crash/reboot).
- **Timezone**: Fixed to `Australia/Sydney` (Server is UTC, but bot is timezone-aware).
- **Scheduler**: Active. Scrapes every 3 hours. Posts every 15 mins (05:00-22:00 AEDT).

## 🚀 VPS Deployment Details
The bot has been migrated from the local Mac to a cloud server for true autonomy.

### Access
```bash
ssh root@vps.example.com
```

### Management Commands (Run on Server)
- **View Logs**: `journalctl -u council-news-bot -f`
- **Check Status**: `systemctl status council-news-bot`
- **Restart Bot**: `systemctl restart council-news-bot`
- **Stop Bot**: `systemctl stop council-news-bot`

### File Locations
- **Code**: `/root/council-news-bot/`
- **Virtual Env**: `/root/council-news-bot/venv/`
- **Database**: `/root/council-news-bot/bot.db`
- **Logs**: Managed by systemd (journalctl).

## 🛠 Session Achievements (1 Dec)
1.  **Server Provisioning**: Set up Ubuntu 24.04 Droplet in Sydney.
2.  **Deployment**: Synced code and database to server.
3.  **Timezone Fix**: Updated `scheduler.py` to use `zoneinfo` for correct Australian time handling regardless of server time.
4.  **Autonomy**: Configured `systemd` service for 24/7 operation without local dependency.

## 📋 To-Do
1.  **Monitor**: Check logs occasionally to ensure stability.
2.  **Backups**: Consider setting up a cron job to backup `bot.db` to S3 or local machine.
3.  **Updates**: To update code, edit locally and run:
    ```bash
    rsync -avz --exclude 'venv' --exclude 'bot.db' --exclude '__pycache__' --exclude '.git' ./ root@vps.example.com:/root/council-news-bot/
    ssh root@vps.example.com "systemctl restart council-news-bot"
    ```

## 📧 Explanation for Chris Eddy
(See email draft below)
