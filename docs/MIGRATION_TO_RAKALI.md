# Migration Plan: DigitalOcean → Rakali (CT 104)

**Status**: Planned, not started.
**Target window**: TBD — schedule when ≥4 hours of focused time available.
**Owner**: Jonathon Marsden.

## Why migrate

- Reclaim DigitalOcean droplet ($X/month → $0).
- Consolidate infrastructure on Rakali (HP EliteDesk 800 G5 Mini running Proxmox VE 9.1.1) alongside the LimeSurvey LXC (CT 103) and the static site at https://lgnews.jonathonmarsden.com (served from CT 100).
- Same backup, snapshot, and SSH conventions as `limesurvey-rakali`.
- No public ingress required for the bot itself — it makes outbound connections to council websites and Bluesky only. Doesn't need to live in a DMZ.

## Current state (DigitalOcean, as of April 2026)

| Item | Detail |
|---|---|
| Host | DigitalOcean droplet, 4 GB RAM, IP `vps.example.com` |
| OS | Ubuntu (per droplet defaults) |
| Code path | `/opt/council-news-bot` |
| Runtime | Docker Compose (`bot` + `db` services) |
| Bot image | `mcr.microsoft.com/playwright/python:v1.58.0-jammy` (Python 3.10 + Playwright + Chrome/Firefox/Safari) |
| Database | Postgres 15 (`postgres:15-alpine`), volume `postgres_data` |
| Resource limits | bot 1.5 CPU / 3 GB RAM, db 0.5 CPU / 1 GB RAM |
| Secrets | `.env` file in `/opt/council-news-bot/.env` (Bluesky app passwords for 8 bots, optional proxy creds, Discord webhook) |
| Scheduling | Host crontab firing `docker compose exec` at scheduled times per state (twice-daily local timezone) |
| Deploy | GitHub Actions on push to `master` → SSH to droplet → `git pull` + rebuild |
| Logs | Docker JSON file driver, 10 MB × 3 rotation |
| Discord webhook | Run summaries + error alerts |

## Target state (Rakali CT 104)

| Item | Detail |
|---|---|
| Host | Rakali (Proxmox VE 9.1.1), Tailscale `100.122.222.91` |
| LXC | CT 104, hostname `council-bot`, Debian 13, **privileged or unprivileged TBD** (see Risk #1) |
| LAN IP | TBD — match the `192.168.86.x` series |
| Code path | `/opt/council-news-bot` (preserve, no need to change paths) |
| Runtime | Docker Compose (unchanged) |
| Resource limits | unchanged |
| Secrets | `/root/secrets/` (mode 600), mirrors LimeSurvey convention |
| Scheduling | host crontab in CT 104 (unchanged) |
| Deploy | GitHub Actions → SSH (via Proxmox jump host) → `git pull` + rebuild |
| Logs | unchanged |
| Discord webhook | unchanged |

## Risks (in order of severity)

### 1. Playwright + Chromium in an unprivileged LXC — GATING RISK
Playwright drives a real browser (Chromium, Firefox, Webkit) which uses Linux namespaces (user, mount, pid) for sandboxing. Unprivileged LXCs have restricted namespace access; this is the single most likely thing to break the migration.

**Mitigation**:
- Prove it works **before** migrating data. Provision CT 104, install Docker, pull the Playwright image, run a smoke test (`python3 main.py --state nt --limit 1 --dry-run`).
- If unprivileged fails, fall back to privileged LXC. Still safer than running on a bare VPS, but reduces isolation.
- If both fail (unlikely), fall back to passing `--cap-add=SYS_ADMIN --shm-size=2g` to the bot Docker container, or running with `--no-sandbox` for Chromium (last resort, weakens the browser sandbox but bot is the only thing in the container).

**Verdict**: don't proceed past Phase 2 without proving Playwright runs.

### 2. Postgres state migration without double-posting
The bot tracks "what we've already posted to Bluesky" in Postgres. If we cut over with stale state, we'll either re-post old stories (bad) or skip new ones (worse).

**Mitigation**:
- Stop the **cron** on DO (don't stop containers — let in-flight scrapes finish).
- Wait for the queue processor (`process_global_queue.py`) to drain (typically 10 min).
- `pg_dump --clean --create` from DO Postgres.
- Restore on CT 104.
- Bring up bot in CT 104 (cron disabled).
- Manually trigger one scrape per state with `--dry-run` to confirm no duplicate posts would fire.
- Enable cron on CT 104.
- Disable cron on DO permanently.

### 3. Outbound IP change — possible scraper rate-limiting / WAF blocks
Council websites have seen requests from DO's IP for months. Switching to Rakali's home IP could trigger:
- New rate-limit windows (effectively a fresh quota — neutral).
- Geo-blocking if any council restricts to Australian commercial IPs (unlikely but possible).
- WAF flags if Rakali's home IP is on any blacklist.

**Mitigation**:
- The bot already supports a proxy via `COUNCIL_BOT_PROXY` env var. If problems emerge, route problem-state scrapes through a proxy.
- Monitor the first few cron runs after cutover for elevated error rates.

### 4. Resource sizing
DO droplet was 4 GB RAM. The bot reserves 256 MB and limits to 3 GB; Postgres limits to 1 GB. **Total ceiling: 4 GB**. Plus base OS, Docker, headroom — call it 5 GB peak.

**Mitigation**:
- Check Rakali RAM headroom before allocating CT 104. If ≥6 GB free of unallocated RAM, proceed. If not, plan capacity changes.
- Provision CT 104 with 6 GB RAM, 4 vCPUs, 16 GB disk to start. Resize from Proxmox host if needed.

### 5. GitHub Actions deploy reconfiguration
Current workflow targets `vps.example.com` with an SSH key stored as a repo secret.

**Mitigation**:
- Generate a new SSH key for the deploy on CT 104.
- Add to CT 104's `~/.ssh/authorized_keys`.
- Update GitHub repo secrets:
  - `VPS_HOST` → CT 104's LAN IP (or a Tailscale name if CT 104 gets Tailscale)
  - `VPS_KEY` → new private key
  - `VPS_USER` → `jonathon` (per LimeSurvey convention)
  - Add `JUMP_HOST` if needed (CT 104 isn't directly reachable; deploy must go via Proxmox host)
- Test workflow with a no-op commit before relying on it.

### 6. Crontab regeneration
Current crontab on DO is generated by `scripts/deployment/generate_crontab.py --static` and accounts for state timezones + DST.

**Mitigation**:
- Regenerate crontab fresh on CT 104.
- Verify it accounts for Australia/Sydney timezone (the container's TZ env). Rakali's host tz may differ.

### 7. Secrets handling
8 Bluesky app passwords + optional proxy creds + Discord webhook URL currently in `.env` on DO.

**Mitigation**:
- `scp` `.env` from DO → local → CT 104's `/root/secrets/.env` (mode 600).
- Symlink or copy into `/opt/council-news-bot/.env` per docker-compose `env_file:` config.
- **Do not** copy via Slack/email/etc.
- Rotate any secrets that touched untrusted machines during the move (consider rotating Bluesky app passwords post-migration as belt-and-braces).

## Phased plan

### Phase 0 — Preparation (no infrastructure changes)
- [ ] Audit `.env` and document every secret currently used.
- [ ] Confirm Rakali RAM headroom (target: ≥6 GB free).
- [ ] Pick a CT 104 LAN IP (e.g. `192.168.86.14`) and confirm not in use.
- [ ] Decide privileged vs unprivileged LXC after spike (Phase 2).
- [ ] Snapshot DO droplet (DigitalOcean console) for rollback safety.

### Phase 1 — Provision CT 104 base OS
- [ ] Run `proxmox/create-lxc.sh` adapted from `limesurvey-rakali`. Adjust:
  - CT ID: 104
  - Hostname: `council-bot`
  - LAN IP: chosen above
  - Disk: 16 GB
  - RAM: 6 GB
- [ ] Run `lxc/01-base-setup.sh` from `limesurvey-rakali` (jonathon sudo user, UFW, fail2ban, UTC).
- [ ] Snapshot: `s01-fresh-lxc`, `s02-os-ready`.

### Phase 2 — Install Docker + Playwright spike (GATING)
- [ ] `apt install docker.io docker-compose-plugin`
- [ ] `docker pull mcr.microsoft.com/playwright/python:v1.58.0-jammy`
- [ ] Run a one-shot Playwright smoke test:
  ```bash
  docker run --rm -it mcr.microsoft.com/playwright/python:v1.58.0-jammy \
    python3 -c "from playwright.sync_api import sync_playwright; \
                p = sync_playwright().start(); \
                b = p.chromium.launch(); \
                page = b.new_page(); \
                page.goto('https://example.com'); \
                print(page.title()); \
                b.close()"
  ```
- [ ] If it prints `Example Domain`, **proceed**. If it errors with sandbox/namespace messages, see Risk #1 mitigations.
- [ ] Snapshot: `s03-runtime-ready`.

### Phase 3 — Migrate code + secrets
- [ ] Clone repo into `/opt/council-news-bot` on CT 104.
- [ ] Create `/root/secrets/` (mode 700), copy `.env` from DO via local laptop, place at `/root/secrets/.env` (mode 600).
- [ ] Symlink: `ln -s /root/secrets/.env /opt/council-news-bot/.env`.
- [ ] `docker compose build` (don't start yet).
- [ ] Snapshot: `s04-code-ready`.

### Phase 4 — Migrate database
- [ ] On DO: stop cron (`crontab -r` or comment all bot lines). Wait 10 min for queue to drain.
- [ ] On DO: `docker exec council_db pg_dump -U councilbot -Fc council_news > /tmp/council_news.dump`
- [ ] `scp` dump to CT 104 (via laptop): DO → laptop → CT 104.
- [ ] On CT 104: `docker compose up -d db` (just the db).
- [ ] Wait for db healthy.
- [ ] `docker exec council_db pg_restore -U councilbot -d council_news --clean --if-exists /tmp/council_news.dump`
- [ ] Verify: `docker exec council_db psql -U councilbot -d council_news -c "SELECT COUNT(*) FROM posts;"` (or whichever main table).
- [ ] Snapshot: `s05-db-restored`.

### Phase 5 — Smoke test the bot
- [ ] `docker compose up -d bot` (idle container per docker-compose.yml).
- [ ] Run migrations: `docker compose exec bot python -m alembic current` then `python -m alembic upgrade head`.
- [ ] Dry-run: `docker compose exec bot python3 main.py --state nt --limit 1 --dry-run`.
- [ ] Live test (single post, low-traffic state): `docker compose exec bot python3 main.py --state nt --limit 1`.
- [ ] Verify on https://bsky.app/profile/roundupnewsbotnt.bsky.social that the post appeared exactly once.
- [ ] Snapshot: `s06-bot-live`.

### Phase 6 — Cutover
- [ ] On CT 104: install crontab from `python3 scripts/deployment/generate_crontab.py --static` output.
- [ ] On DO: confirm cron remains disabled.
- [ ] Watch logs for the next two scheduled scrape windows on CT 104 (24–48 hours).
- [ ] Verify Discord webhook fires from CT 104.
- [ ] Verify GitHub Actions deploys to CT 104, not DO (update workflow secrets first).
- [ ] Snapshot: `s07-running-prod`.

### Phase 7 — Decommission DO (after 48 hours of clean operation)
- [ ] Stop bot containers on DO: `docker compose down`.
- [ ] DigitalOcean console: take final snapshot of droplet.
- [ ] Destroy droplet.
- [ ] Cancel DO billing for this droplet.
- [ ] Update `DEPLOYMENT.md`, `README.md`, and `CLAUDE.md` in this repo to reflect Rakali as production.
- [ ] Update GitHub Actions workflow to remove DO references.

## Estimated time

| Phase | Time | Risk if rushed |
|---|---|---|
| Phase 0 | 30 min | Missing audit causes Phase 7 surprises |
| Phase 1 | 30 min | Low |
| Phase 2 | 30–120 min | **HIGH** — Playwright failure here means restart |
| Phase 3 | 30 min | Secret leakage if rushed |
| Phase 4 | 30–60 min | Data corruption / lost posts |
| Phase 5 | 30 min | Discovers Playwright/network issues missed in Phase 2 |
| Phase 6 | 30 min active + 48h passive | Double-posting if cron not properly disabled on DO |
| Phase 7 | 30 min | Premature destruction loses fallback |
| **Total active** | **~4–6 hours** | + 48h observation window |

## Rollback plan

At every snapshot point, rollback is possible:

```bash
# From Proxmox host
pct stop 104 && pct rollback 104 <snapshot-name> && pct start 104
```

If catastrophic failure during cutover (Phase 6 or 7):
1. Stop bot containers on CT 104 immediately.
2. Re-enable cron on DO (still has the original crontab).
3. Bring back DO droplet from DigitalOcean snapshot if already destroyed.
4. Investigate before re-attempting.

## Things to monitor for 7 days post-migration

- Discord webhook delivery rate.
- Per-state scrape success rate vs DO baseline.
- New error patterns in logs (especially network / WAF related).
- Postgres disk growth — Rakali disk is finite, DO had elastic storage.
- Bluesky API rate limits (no change expected — same accounts, different IP).
- LXC RAM/CPU utilisation in Proxmox.

## Companion repo

Following the `limesurvey-rakali` pattern, post-migration we should consider creating a `council-news-bot-rakali` repo containing:

- `proxmox/create-lxc.sh` — CT 104 provisioning
- `lxc/01-base-setup.sh` — adapted from limesurvey-rakali
- `lxc/02-docker-install.sh` — Docker setup
- `lxc/03-bot-deploy.sh` — clone + build + first run
- `caddy/` — only needed if we ever expose a status page or healthcheck endpoint
- `scripts/backup.sh` — Postgres dump + secrets, daily cron
- `scripts/restore.sh` — restore from backup
- `docs/` — operational runbooks

The bot's application code stays in this repo (`council-news-bot`); the Rakali-specific infrastructure lives in `council-news-bot-rakali`.
