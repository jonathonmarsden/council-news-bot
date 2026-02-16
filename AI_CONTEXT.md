# AI Context & Operational Doctrine

## 🚩 Mission Statement
**"No Silent Failures. No Dark Councils."**

The Council News Bot exists to shine a light on local government by aggregating news from all ~540 LGAs in Australia. 
Our primary operational directive is **Robustness**. A scraper that fails silently is worse than no scraper at all, as it gives a false sense of coverage.

## 🧠 System Context
This project is a Python-based asynchronous scraping pipeline running on a DigitalOcean VPS (Dockerized).

### Key Components
- **Orchestrator**: VPS Host `cron` triggers `main.py` (Scraping) and `scripts/cron/process_global_queue.py` (Posting).
- **Configuration**: JSON files in `states/{state_code}/councils.json` define the rules for each council.
- **Engine**: `core/scrapers/` contains the logic. `CardScraper` is the workhorse.
- **WAF Defense**: We use `curl_cffi` and rotating proxies to bypass Cloudflare/Incapsula.

## 🛡️ Anti-Bot Strategy (The WAF War)
We bypass sophisticated protections (Cloudflare, Incapsula, SparkCMS) using a tiered approach:

1.  **Tier 1: Standard Requests** (Fastest) - Used for simple HTML sites (SA/NT).
2.  **Tier 2: Impersonation** - `use_curl: true` with `impersonate: chrome124`.
3.  **Tier 3: Rotating Proxies** - Added for IP-blocked sites.

**SparkCMS / Catalyst Pattern**:
Identified in Jan 2026. Dominant in NT and WA (Esperance, Albany, ~70 other councils). Note: Often labeled as "Catalyst" in legacy configs, but the `module-list .row` signature is the technical identifier.
*   **Signature**: `.module-list .row`
*   **Required Config**: `curl_scraper` + `use_curl: true` + `impersonate: chrome124` (or `chrome120`).

## 🔄 Deployment & Operations
### Infrastructure
- **VPS**: DigitalOcean Droplet (vps.example.com)
- **User**: `root`
- **Path**: `/opt/council-news-bot`
- **Persistence**: `logs/` and `data/` volumes.

### CI/CD Pipeline
- **Defined**: `.github/workflows/deploy.yml`
- **Trigger**: Push to `master` (passes checks) -> Auto-Deploy.
- **Process**: Rsync code -> Rebuild Docker -> Migrate DB.
- **Best Practice**: Commit to `master` rather than manual SSH edits.
- **Diagnostics**: `scripts/monitoring/diagnose.py`

### Scheduling
- **Method**: Local `cron` on VPS host (generated via `scripts/deployment/generate_crontab.py`).
- **Timing**: Twice daily per state (Morning/Evening windows).

## 🛠 Troubleshooting Guide

### 1. Proxy Errors (403/502/SSL)
- **Symptom**: "Tunnel connection failed" in logs.
- **Strategy**: Specific councils block the proxy IP.
- **Fix**: Add `"bypass_proxy": true` to council config (see Orange City Council).

### 2. Missing Articles
- **Diagnosis**: Scraper runs but finds 0 items.
- **Fix**: Check selectors in `councils.json`. Sites often redesign.
- **Tools**: Use `main.py --council {id} --dry-run` locally.

### 3. BlueSky Rate Limits
- **Symptom**: "RateLimitExceeded".
- **Fix**: Queue processor runs every 10 mins; ensure it doesn't overlap.

## Reference
- **Repo**: `jonathonmarsden/council-news-bot`
- **Documentation**: `STAKEHOLDER_REPORT_V2.0.md`

### Local-to-Remote Workflow
1.  **Develop Locally**: All changes to `councils.json` or scrapers happen in VS Code.
2.  **Verify**: Run `python3 scripts/debug/run_scraper.py <council_id>` to ensure it works.
3.  **Deploy**: 
    ```bash
    python3 scripts/deployment/deploy_with_password.py
    ```

### Monitoring & Maintenance
- **Logs**: `ssh root@vps.example.com 'cd /opt/council-news-bot && docker compose logs -f --tail=100'`
- **Health Checks**: The bot runs an internal health check daily.
- **Zero Article Warning**: Any council returning 0 articles is treated as a **P1 Issue**. It usually means a broken selector or WAF block.

## 📂 Key Files for AI Agents
- `docs/DEVELOPER_GUIDE.md`: Detailed architecture.
- `docs/reports/`: Historical audit reports and risky selector tracking.
- `PROJECT_LEARNINGS_2026.md`: Knowledge base of CMS patterns (Catalyst, OpenCities, SparkCMS).
- `states/`: The source of truth for council configurations.

## 🤖 Directives for Future Agents
1.  **Preserve the Config**: Do not change the structure of `councils.json` without validating the schema.
2.  **Safe Selectors**: Avoid generic classes like `.col-12` or `.row`. Prefer `article`, `.news-item`, or `h2`.
3.  **Check the Cookies**: If a site is failing, use `curl -I` to check cookies for CMS hints (e.g., `BNI_SparkCMSLB`).

## 🔑 Operational Access
**VPS Access**: The agent currently has SSH access to the production VPS (`vps.example.com`) via `scripts/deployment/deploy_secrets.py` (which contains `HOST`, `USER`, `PASS`).
- **Standard Protocol**: Use `sshpass` or the existing Python deployment scripts to execute remote commands.
- **Verification**: Always verify changes on the VPS after deployment (e.g., checking `crontab -l` or `docker ps`).

## 🤖 Agent Autonomy Protocol (Strict)
**Deployment Authority**: The agent processes unrestricted SSH access to the production VPS via `scripts/deployment/deploy_with_password.py`.
**Rule**: NEVER ask the user to run deployment scripts or SSH commands.
**Action**: If a code change requires deployment, the agent must:
1.  Make the code change.
2.  **IMMEDIATELY** execute the deployment script.
3.  Verify the result on the VPS.
4.  Report the completed action to the user.
