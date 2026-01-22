# WAF Bypass Strategy & Research

## Overview
As of January 2026, many Australian Council websites (particularly those managed by large vendors or sophisticated IT teams like "City of Adelaide") utilize Cloudflare or similar Web Application Firewalls (WAFs) that actively block automated scrapers.

This document outlines the strategy, tools, and findings for bypassing these protections to ensure the public's right to access council news.

## Anti-Bot Defenses Encountered
- **IP Reputation Blocking**: Direct requests from data center IPs (DigitalOcean, AWS) are instantly blocked (403 Forbidden).
- **TLS Fingerprinting**: Standard Python `requests` or `aiohttp` libraries have easily identifiable TLS handshakes (JA3 fingerprints) that trigger WAFs.
- **Header Analysis**: Missing or malformed headers (User-Agent, Accept-Launguage, etc.) trigger blocks.
- **JavaScript Challenges**: Some sites require a JS engine to solve a challenge (Cloudflare Turnstile/Managed Challenge).

## Bypass Architecture

### 1. `curl_cffi` (The Impersonator)
We replaced standard requests with `curl_cffi` (a Python binding for `curl-impersonate`). This library mimics the TLS handshake and HTTP/2 behavior of real browsers.
- **Key Feature**: `impersonate="chrome124"` (or similar).
- **Usage**: Used inside `CardScraper` and `RSSScraper` when `use_curl: true` is set in config.

### 2. Residential/Rotating Proxies
For targets blocking Data Center IPs, we tunnel traffic through a rotating proxy service.
- **Environment Variable**: `COUNCIL_BOT_PROXY`
- **Config**: `use_rotating_proxy: true` in `councils.json`.

## Research Methodology
When a council is blocked, we use the `scripts/debug/research_waf_bypass.py` tool.

### Workflow
1. **Develop/Fix Tool**: Ensure `scripts/debug/research_waf_bypass.py` is up to date.
2. **Deploy to VPS**: The tool must be run **from the production environment** (VPS) because local IPs (residential ISPs) often bypass WAFs naturally, yielding false positives.
   ```bash
   scp scripts/debug/research_waf_bypass.py root@<VPS_IP>:/opt/council-news-bot/scripts/debug/
   ```
3. **Run Research**:
   ```bash
   docker exec -it council_news_bot python3 scripts/debug/research_waf_bypass.py --url <TARGET_URL>
   ```
4. **Analyze Results**:
   The tool tests a matrix of:
   - **Impersonations**: Chrome 110-124, Safari 15-17, Edge.
   - **Proxy Mode**: Direct vs. Proxy.
   
5. **Apply Configuration**: Update `councils.json` with the winning combination.

## Case Studies

### City of Adelaide (Jan 2026)
- **Problem**: 403 Forbidden on all requests from VPS.
- **Research Findings**:
  - `Direct + Any Browser`: **BLOCKED** (IP Reputation).
  - `Proxy + Chrome124`: **SUCCESS** (Status 200).
  - `Proxy + Safari15_5`: **SUCCESS** (Status 200).
- **Solution Applied**:
  ```json
  "use_curl": true,
  "use_rotating_proxy": true,
  "impersonate": "chrome124"
  ```
