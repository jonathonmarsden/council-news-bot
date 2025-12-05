# Deployment Script - Quick Reference

## ✅ **YOU ARE READY TO DEPLOY!**

All critical pre-deployment checks have passed:
- ✅ 541 councils enabled (99.4% coverage)
- ✅ All JSON configs valid
- ✅ Python dependencies installed
- ✅ Core modules working
- ✅ `.env.example` sanitized
- ✅ VPS credentials configured

---

## 🚀 **Deploy Now**

### Option 1: Full Deployment (Recommended)
```bash
./scripts/deployment/deploy.sh
```

This will:
1. Run 10 pre-flight checks
2. Backup VPS database (timestamped)
3. Sync code to VPS (excludes .env, database, logs)
4. Rebuild and restart Docker containers
5. Verify deployment health
6. Show management commands

### Option 2: Dry Run (See What Would Deploy)
```bash
./scripts/deployment/deploy.sh --dry-run
```

Shows exactly what would be deployed without making changes.

### Option 3: Skip Checks (Fast Deploy)
```bash
./scripts/deployment/deploy.sh --skip-checks
```

⚠️ Not recommended - skips validation checks.

---

## 📋 **What Happens During Deployment**

### Phase 1: Pre-Flight Checks ✈️
- Git status
- Python dependencies
- JSON validation
- VPS connectivity
- Docker availability
- Council count
- Database size
- Credential safety
- Scraper test

### Phase 2: Backup 💾
- Creates timestamped backup on VPS
- Keeps last 10 backups
- Location: `/opt/council-news-bot/backups/`

### Phase 3: Deploy 📦
- Syncs code via rsync
- **Excludes:** `.git`, `.env`, `council_news.db`, logs, venv
- **Includes:** Python code, configs, Dockerfile, requirements

### Phase 4: Restart 🔄
- Stops existing containers
- Rebuilds Docker image
- Starts fresh containers
- Waits 5s for startup

### Phase 5: Verify ✓
- Checks container health
- Shows recent logs
- Confirms running state

---

## 🎯 **After Deployment**

### Immediate Actions (First 5 minutes)
```bash
# Watch live logs
ssh root@vps.example.com "cd /opt/council-news-bot && docker compose logs -f"

# Look for:
# ✓ "Starting scrape for..." (scraper active)
# ✓ "Posted: ..." (posting working)
# ✗ Python exceptions (errors)
```

### First Hour Checks
```bash
# Check container status
ssh root@vps.example.com "cd /opt/council-news-bot && docker compose ps"

# Should show: State=running

# Check BlueSky feeds
# - NSW: roundupnewsbotnsw.bsky.social
# - VIC: roundupnewsbotvic.bsky.social
# - QLD: roundupnewsbotqld.bsky.social
# - TAS: roundupnewsbottas.bsky.social
# (+ SA, WA, NT, ACT)
```

### Daily Monitoring
```bash
# Run health check
ssh root@vps.example.com
cd /opt/council-news-bot
python3 scripts/audit_lga_coverage.py
```

---

## 🔧 **Common Commands**

### View Logs
```bash
# Live tail
ssh root@vps.example.com "cd /opt/council-news-bot && docker compose logs -f"

# Last 100 lines
ssh root@vps.example.com "cd /opt/council-news-bot && docker compose logs --tail=100"
```

### Restart Bot
```bash
ssh root@vps.example.com "cd /opt/council-news-bot && docker compose restart"
```

### Stop Bot
```bash
ssh root@vps.example.com "cd /opt/council-news-bot && docker compose down"
```

### Start Bot
```bash
ssh root@vps.example.com "cd /opt/council-news-bot && docker compose up -d"
```

### Check Database Stats
```bash
ssh root@vps.example.com
cd /opt/council-news-bot
sqlite3 council_news.db "SELECT COUNT(*) FROM articles;"
sqlite3 council_news.db "SELECT COUNT(*) FROM articles WHERE posted_at IS NOT NULL;"
```

---

## 🆘 **Rollback Procedure**

If something goes wrong:

```bash
# 1. SSH to VPS
ssh root@vps.example.com

# 2. Stop current bot
cd /opt/council-news-bot
docker compose down

# 3. Restore database backup
cd backups
ls -lt  # Find latest backup
cp council_news_backup_YYYYMMDD_HHMMSS.db ../council_news.db

# 4. Restart
cd ..
docker compose up -d

# 5. Check logs
docker compose logs -f
```

---

## 📊 **Success Metrics**

### Healthy Deployment:
- ✅ Container shows "Up" status
- ✅ No Python exceptions in logs
- ✅ "Scraping X councils..." every 3 hours
- ✅ "Posted: ..." every 5 min (5am-10pm AEST)
- ✅ BlueSky feeds updating
- ✅ Database growing

### Warning Signs:
- ⚠️ Container restarts frequently
- ⚠️ Python exceptions
- ⚠️ No posts during active hours
- ⚠️ "Circuit breaker" messages (councils disabled)
- ⚠️ Database not growing

---

## 📖 **Full Documentation**

See: `scripts/deployment/DEPLOYMENT_GUIDE.md`

For comprehensive troubleshooting, rollback procedures, and advanced commands.

---

## 🎉 **Ready When You Are!**

Run this command to deploy:
```bash
./scripts/deployment/deploy.sh
```

The script will:
- ✓ Ask for confirmation before proceeding
- ✓ Show progress for each step
- ✓ Validate successful deployment
- ✓ Provide next steps

**Estimated time:** 2-3 minutes

Good luck! 🚀
