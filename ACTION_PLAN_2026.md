# Action Plan 2026: "Operation Fortification"

Based on the January 22, 2026 Health Check (85.9% Health Score, 464 Active, 76 Warnings), the following plan operationalizes the recovery of the remaining 14% of the network.

## 🎯 Strategic Goal
Achieve **95% Active Health** (>513 active councils) by moving fragile scrapers to robust patterns (Curl/Vendor-specific).

## 🛠 Workstreams

### W1. The "Zero-Article" Triage (The 76)
**Objective**: Recover the 76 councils currently returning 0 articles.
- **Hypothesis**: Most are blocked by WAFs (Cloudflare/Incapsula) or have had DOM structure changes.
- **Action 1.1 (VIC/NSW/QLD)**: Bulk toggle `use_curl: true` for the failing councils in these states. VIC's 97.5% success rate proves this works.
- **Action 1.2 (WA/NT)**: These are likely custom site structure issues. Audit manually.

### W2. WA Standardization ("West Coast Recovery")
**Objective**: Fix WA's low 76% health score.
- **Problem**: 33 WA councils are failing. WA uses many custom generic scrapers.
- **Action 2.1**: Check if any of the 33 failing WA councils are actually *Catalyst* sites that were missed or are slightly non-standard.
- **Action 2.2**: Check if any are *Alyka* sites (another WA vendor).
- **Action 2.3**: Build generic fallback for WA small shires (often basic HTML).

### W3. Vendor consolidation
**Objective**: Reduce maintenance overhead by grouping generic scrapers into Vendor Classes.
- **Action 3.1**: Run a signature scan on the 74 VIC `curl_scrapers`. If >50% are one vendor (e.g. Squiz Matrix), subclass `SquizScraper`.
- **Action 3.2**: Migrate identified WordPress sites in NSW from `card_scraper` to `wordpress_scraper` (better metadata).

## 📋 Operational Tasks

### Phase 1: Immediate Triage (Next 24 Hours)
1.  **Diagnose the Zeros**: Create `scripts/diagnosis_tool.py` to inspect the HTML of failing councils to determine *why* they fail (Cloudflare challenge vs. Empty Selector).
2.  **The "Curl" Batches**: Update `states/{state}/councils.json` for NSW/QLD failures to use `curl_scraper` and re-test.

### Phase 2: Code Fortification (Next Week)
3.  **Refine Catalyst**: Ensure `catalyst_scraper` isn't missing items due to date filtering (some councils might have old dates on "new" items on the homepage).
4.  **Bot Hygiene**: Ensure user-agents are rotated in `curl_scraper` to avoid long-term banning.

### Phase 3: Infrastructure (Long Term)
5.  **Alerting**: Hook the `Health Check` script into the Discord Logger to post "Zero Article" warnings weekly.
6.  **Dashboard**: Simple static HTML report generated daily (already started with `HEALTH_CHECK_REPORT_2026.md`).

## 📊 Success Metrics
- **Green**: > 500 Councils returning news (Currently 464).
- **Yellow**: < 20 Councils with "Zero Articles" (Currently 76).
- **Red**: Any exceptions/crashes (Currently 0 - PASSED).
