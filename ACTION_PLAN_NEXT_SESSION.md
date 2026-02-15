# Action Plan - Next Session (Feb 15, 2026)

**Created:** 15 February 2026  
**Session Status:** Phase 1 & 2 complete, enterprise CI/CD deployed  
**Purpose:** Pick up where we left off after session ends  

---

## 🚀 What Was Accomplished This Session

### Phase 1: Foundation Hardening ✅
- Repository cleanup: 40+ loose files → organized structure
- Created `core/exceptions.py` with 9 custom exception types
- Fixed exception handling across codebase (no more bare `except`)
- Added modern type hints (`from __future__ import annotations`)
- Updated `.gitignore`

### Phase 2: Operational Hardening ✅
- Created 18,500+ words of documentation:
  - `docs/operations/RUNBOOK.md`
  - `docs/operations/MONITORING.md`
  - `docs/operations/TROUBLESHOOTING.md`
  - `docs/architecture/SYSTEM_DESIGN.md`
- Implemented enterprise CI/CD:
  - `.github/workflows/test.yml` - Automated testing
  - `.github/workflows/deploy.yml` - Auto-deploy (gated on tests)
  - `.github/workflows/rollback.yml` - 1-click rollback
  - `.github/workflows/ops_monitoring.yml` - Daily health + backups
- Created comprehensive guides:
  - `.github/CI_CD_GUIDE.md`
  - `SYSTEM_OVERVIEW.md` (480-line architecture doc)

### Critical Fixes ✅
- **Proxy Issue:** Fixed VPS using non-rotating proxy endpoint
- **Git SSH:** Configured SSH authentication for persistent operations
- **Auto-Deploy:** GitHub Actions now deploys on every push to master

### Git Commits (for reference)
```
87194df - docs: add comprehensive system overview one-pager  
8b317ae - CI/CD: add rollback workflow, health-check alerts, and operations guide
75a9501 - CI/CD: gate deploy on tests, add monitoring and backups
2220d41 - CI/CD: add SSH rsync deploy and include master in tests
8ccd646 - Phase 1 & 2: Professional standards with operational docs and CI/CD
```

---

## 🎯 Next Priorities (Tier 1 - Do Next Session)

### 1. External Uptime Monitoring ⚠️ CRITICAL
**Problem:** If VPS goes down, Discord can't alert you  
**Solution:** GitHub Actions uptime check (runs externally every 15min)  
**Time:** 15 minutes  

**File to create:** `.github/workflows/uptime_check.yml`
```yaml
name: Uptime Check
on:
  schedule:
    - cron: "*/15 * * * *"  # Every 15 minutes
  workflow_dispatch:

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Check VPS accessibility
        run: |
          if ! nc -zv ${{ secrets.VPS_HOST }} 22 -w 10 2>&1 | grep -q succeeded; then
            curl -X POST "${{ secrets.DISCORD_WEBHOOK_ALERTS }}" \
              -H "Content-Type: application/json" \
              -d "{\"embeds\":[{\"title\":\"🔴 VPS Down\",\"description\":\"VPS at ${{ secrets.VPS_HOST }} is unreachable on SSH port\",\"color\":15158332,\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}],\"username\":\"Uptime Monitor\"}"
            exit 1
          fi
          
      - name: Check Docker health
        run: |
          STATUS=$(ssh -i ~/.ssh/deploy_key -o StrictHostKeyChecking=no ${{ secrets.VPS_USER }}@${{ secrets.VPS_HOST }} \
            "cd /opt/council-news-bot && docker compose ps --format json | jq -r '.[].State' | grep -v running" || echo "ok")
          
          if [ "$STATUS" != "ok" ]; then
            curl -X POST "${{ secrets.DISCORD_WEBHOOK_ALERTS }}" \
              -H "Content-Type: application/json" \
              -d "{\"embeds\":[{\"title\":\"⚠️ Docker Unhealthy\",\"description\":\"One or more containers not running on VPS\",\"color\":15105570}]}"
          fi
```

**Why critical:** Currently your only monitoring depends on the VPS being up. Catch-22.

---

### 2. Dependency Vulnerability Scanning
**Problem:** Unknown CVEs in requirements.txt  
**Solution:** Add pip-audit to CI/CD  
**Time:** 10 minutes  

**File to edit:** `.github/workflows/test.yml`

Add this job after the existing test job:
```yaml
  security-deps:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install pip-audit
        run: pip install pip-audit
      
      - name: Scan dependencies
        run: pip-audit -r requirements.txt --desc
        continue-on-error: true  # Don't block builds initially
```

**Expected output:** List of known CVEs in dependencies

---

### 3. Test Coverage Report
**Problem:** Unknown how much code is tested  
**Solution:** Generate coverage report  
**Time:** 10 minutes  

**File to edit:** `.github/workflows/test.yml`

Modify the "Run unit tests" step:
```yaml
- name: Run unit tests
  run: |
    pytest tests/ -v --cov=core --cov=main --cov-report=term-missing --cov-report=xml
  env:
    DATABASE_URL: postgresql://postgres:postgres@localhost:5432/council_news_test

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
    fail_ci_if_error: false
```

**Target:** Aim for 80%+ coverage on core modules

---

### 4. Disaster Recovery Runbook
**Problem:** No documented VPS failure procedure  
**Solution:** Write step-by-step recovery guide  
**Time:** 20 minutes  

**File to create:** `docs/operations/DISASTER_RECOVERY.md`

**Must include:**
1. Restore from backup procedure
2. Spin up new VPS steps (DigitalOcean)
3. Docker setup commands
4. Secret restoration (.env file)
5. Crontab restoration
6. DNS/networking checks
7. Verification checklist
8. Expected time-to-recovery (estimate: 30-60 min)

**Template structure:**
```markdown
# Disaster Recovery Runbook

## Scenario 1: VPS Data Corruption
## Scenario 2: VPS Destroyed/Lost
## Scenario 3: Docker Completely Broken
## Scenario 4: Database Corruption
## Scenario 5: Git Repository Lost

Each scenario:
- Detection symptoms
- Recovery steps (numbered, exact commands)
- Verification tests
- Time estimate
```

---

## 📋 Tier 2 Priorities (Do This Month)

### 5. Content Quality Filters
**Problem:** Malformed articles sometimes get posted  
**Examples:** "Click here", dates in year 3000, broken URLs  

**File to edit:** `core/scrapers/base.py`

Add validation method:
```python
def _validate_article(self, article: Dict) -> bool:
    """Validate article quality before saving."""
    # Reject generic/useless titles
    generic_titles = ['read more', 'click here', 'more info', 'learn more', 'view']
    if article['title'].lower().strip() in generic_titles:
        logging.warning(f"Rejected generic title: {article['title']}")
        return False
    
    # Reject suspiciously short titles
    if len(article['title']) < 10:
        logging.warning(f"Rejected short title: {article['title']}")
        return False
    
    # Reject future dates
    if article.get('date'):
        try:
            date = parser.parse(article['date'], dayfirst=True)
            if date.year > datetime.now().year + 1:
                logging.warning(f"Rejected future date: {article['date']}")
                return False
        except Exception:
            pass  # Keep if unparseable (safer than rejecting)
    
    return True
```

Then call it in `scrape()` before saving articles.

---

### 6. robots.txt Compliance Audit
**Problem:** Unknown which councils forbid scraping  
**Risk:** Legal complaints, IP blocks  

**File to create:** `scripts/audit_robots_txt.py`

```python
#!/usr/bin/env python3
"""
Audit all councils' robots.txt files to check scraping compliance.
"""
from urllib.robotparser import RobotFileParser
import json
from pathlib import Path

def audit_council(council_url):
    """Check if council allows scraping."""
    rp = RobotFileParser()
    rp.set_url(f"{council_url}/robots.txt")
    try:
        rp.read()
        return rp.can_fetch("*", council_url)
    except:
        return None  # No robots.txt or error

# Load all councils
# Check each one
# Generate report: reports/ROBOTS_TXT_AUDIT.md
```

**Output:** List of councils that disallow scraping (so we can disable them)

---

### 7. Monthly Cost Tracking
**Problem:** No visibility into expenses  

**File to create:** `COST_ANALYSIS.md`

Document:
- VPS: $24/month (DigitalOcean 4GB)
- Proxy: $2.99/month (Webshare 250MB)
- GitHub: $0 (free tier)
- Domain (if applicable): $XX/year
- **Total: ~$27/month**

Track annually: ~$324/year

---

### 8. Simple Web Dashboard (Optional)
**Problem:** Stats buried in Discord and database  
**Solution:** Flask dashboard with charts  

**Files to create:**
- `dashboard.py` (Flask app)
- `templates/dashboard.html`
- `static/style.css`

**Features:**
- Success rate by state (chart)
- Articles posted per hour (graph)
- Queue depth (number)
- Top 10 councils by activity
- Recent errors

**Add to Docker Compose:**
```yaml
  dashboard:
    build: .
    command: python dashboard.py
    ports:
      - "8080:8080"
    env_file:
      - .env
```

---

## 🚫 What NOT to Do (Over-Engineering)

### Don't Build These (At Current Scale)
- ❌ **Staging environment** — Expensive, tests + rollback sufficient
- ❌ **Multi-region HA** — Overkill for news bot
- ❌ **Kubernetes** — Absurd for single VPS
- ❌ **Microservices** — Unnecessary complexity
- ❌ **GraphQL API** — No consumer

### Defer These Until Needed
- Database replication (daily backups OK for now)
- Horizontal scaling (560 councils fit on one VPS)
- Load balancer (not needed)
- Real-time monitoring dashboard (Discord sufficient)

---

## 📁 Current Repository State

### Branch: master (production)
All changes auto-deploy to VPS via GitHub Actions

### Recent Additions (This Session)
```
.github/
├── CI_CD_GUIDE.md ...................... NEW
├── workflows/
│   ├── deploy.yml ...................... UPDATED (gated on tests)
│   ├── test.yml ........................ UPDATED (includes master)
│   ├── rollback.yml .................... NEW
│   └── ops_monitoring.yml .............. NEW

docs/
├── operations/
│   ├── RUNBOOK.md ...................... NEW
│   ├── MONITORING.md ................... NEW
│   └── TROUBLESHOOTING.md .............. NEW
└── architecture/
    └── SYSTEM_DESIGN.md ................ NEW

core/
├── exceptions.py ....................... NEW (9 exception types)
├── constants.py ........................ NEW
├── timezone_utils.py ................... NEW
└── (all other files updated with type hints)

SYSTEM_OVERVIEW.md ...................... NEW (480 lines)
PHASE_1_COMPLETION.md ................... NEW
PHASE_2_COMPLETION.md ................... NEW
ACTION_PLAN_NEXT_SESSION.md ............. THIS FILE
```

### GitHub Secrets (Already Configured)
- ✅ `VPS_HOST` = 170.64.186.16
- ✅ `VPS_USER` = root
- ✅ `VPS_SSH_KEY` = (deployment key)
- ✅ `DISCORD_WEBHOOK_ALERTS` = (webhook URL)

---

## 🔄 How to Start Next Session

### 1. Navigate & Check Status
```bash
cd /Users/jonathonmarsden/projects/council-news-bot
git status
git log --oneline -10
```

### 2. Verify Production Health
```bash
# Check VPS
ssh root@170.64.186.16 "cd /opt/council-news-bot && docker compose ps"

# Check recent logs
ssh root@170.64.186.16 "cd /opt/council-news-bot && docker compose logs --tail=100 bot"

# Check GitHub Actions
open https://github.com/jonathonmarsden/council-news-bot/actions
```

### 3. Read This File
```bash
cat ACTION_PLAN_NEXT_SESSION.md
```

### 4. Start with Tier 1 Priorities
Follow the numbered tasks above, starting with External Uptime Monitoring.

---

## 📊 Current Metrics (As of Feb 15)

### Code Quality
- ✅ 9 custom exception types
- ✅ Modern type hints throughout
- ✅ No bare except blocks
- ✅ Organized repository structure
- ⚠️ Test coverage: Unknown (Tier 1 priority #3)

### CI/CD Maturity
- ✅ Automated testing on every push
- ✅ Auto-deploy after tests pass
- ✅ 1-click rollback available
- ✅ Daily monitoring + backups (21:00 UTC)
- ⚠️ External uptime check: Missing (Tier 1 priority #1)

### Production Health
- ✅ 95%+ scraper success rate
- ✅ Twice-daily scraping (06:00 & 18:00 local)
- ✅ Proxy issue resolved (rotating endpoint)
- ✅ Discord alerts working
- ✅ PostgreSQL backups (14-day retention)

### Documentation
- ✅ 18,500+ words operational docs
- ✅ 480-line system overview
- ✅ CI/CD operations guide
- ✅ Troubleshooting guide
- ⚠️ Disaster recovery: Missing (Tier 1 priority #4)

---

## 🎓 Lessons Learned This Session

### What Worked
1. **SSH Git push** — Persistent, no credential headaches
2. **GitHub Actions** — Reliable, free, well-documented
3. **Gated deploys** — Tests must pass before production
4. **Discord webhooks** — Simple, effective alerts
5. **Comprehensive docs** — Makes system resumable

### Pain Points Resolved
- ✅ Proxy 407 errors → Fixed rotating endpoint
- ✅ Manual deploys → Automated via GitHub Actions
- ✅ No rollback → 1-click rollback workflow
- ✅ Silent failures → Discord alerts + monitoring
- ✅ Poor documentation → 18,500+ words added

### Watch Out For
1. **Proxy stability** — Webshare critical dependency
2. **Disk space** — Logs/backups can fill VPS
3. **Rate limits** — BlueSky 24 posts/hour per account
4. **Config drift** — VPS manual edits vs git
5. **Dependency CVEs** — Need scanning (Tier 1 #2)

---

## 🔮 Long-Term Vision (Optional Future)

### Phase 3: Code Polish (If Desired)
- Refactor 580-line `main.py` into modules
- Config dataclasses (type-safe)
- Comprehensive docstrings
- Performance profiling
- More integration tests

### Phase 4: Product Features (If Growth)
- Web dashboard for stats
- Council partnership program
- Content tagging/categorization
- Duplicate detection (cross-council)
- Public API

### Phase 5: Scale (If Needed)
- Multi-council partnerships
- User subscription system
- Machine learning quality filters
- Real-time push notifications

---

## 📞 Context for Future AI Assistant

**Project:** Australian Local Government news aggregation bot  
**Scale:** 560 councils, 8 states, ~144 posts/day  
**Tech:** Python, PostgreSQL, Docker, GitHub Actions  
**VPS:** 170.64.186.16 (DigitalOcean 4GB)  
**User:** Solo dev, pragmatic, values reliability over features  

**Philosophy:**
- Documentation > complexity
- Reliability > features
- Solo-maintainable > enterprise-scale
- Good enough > perfect

**Current State:**
- ✅ Production-ready
- ✅ Enterprise CI/CD
- ✅ Comprehensive docs
- ⏭️ Ready for Tier 1 tasks

---

## 📚 Quick Reference

| Resource | Location |
|----------|----------|
| **Production VPS** | `ssh root@170.64.186.16` |
| **GitHub Repo** | https://github.com/jonathonmarsden/council-news-bot |
| **GitHub Actions** | /actions tab |
| **Main Docs** | `docs/operations/RUNBOOK.md` |
| **Troubleshooting** | `docs/operations/TROUBLESHOOTING.md` |
| **System Overview** | `SYSTEM_OVERVIEW.md` |
| **CI/CD Guide** | `.github/CI_CD_GUIDE.md` |

---

**Status:** ✅ Ready for next session  
**Next Action:** Implement Tier 1 priorities  
**Estimated Time:** 1-2 hours for all Tier 1 tasks

---

*This file persists across sessions. Update it as work progresses.*
