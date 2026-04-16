# CSR & WAF Migration Plan 2026

## 🎯 Objective
Migrate "Dead" scrapers (specifically those blocked by WAFs or relying on CSR/React) to the new `BrowserScraper` infrastructure.

## 🏗️ Infrastructure Status
- **Class**: `BrowserScraper` (Playwright) ✅ Live
- **Host**: DigitalOcean VPS (Docker/Ubuntu) ✅ Live
- **Pilot**: City of Armadale (WA) ✅ Verified

## 📋 Target Candidates
We have ~84 councils currently marked as **WAF_BLOCK**. These likely fail because:
1.  **Javascript Challenges**: The site requires JS execution to verify the visitor (Cloudflare, Incapsula).
2.  **Client-Side Rendering (CSR)**: The content is hydrated via JS (React, Vue, Next.js).
3.  **Fingerprinting**: The site rejects Python/Requests headers.

### Priority Batch 1 (Sample)
We should test the `BrowserScraper` on these diverse WAF targets to validate the solution:

| Count | Council | State | Current Error |
|-------|---------|-------|---------------|
| 1 | Hindmarsh Shire | VIC | WAF 403 |
| 2 | Campbelltown City | NSW | WAF 403 / CSR |
| 3 | Lake Macquarie | NSW | WAF 403 |
| 4 | Randwick City | NSW | WAF 403 |
| 5 | City of Launceston | TAS | WAF 403 |

## ⚙️ Migration Workflow

### 1. Diagnosis
Check if the site is a redirect/CSR app.
```bash
# Check headers
curl -I [url]

# Check for React root or hidden content
curl [url] | grep -E "root|Next.js|hydration"
```

### 2. Configuration Update
Modify the council entry in `states/[state]/councils.json`:
```json
{
    "id": "council_id",
    ...,
    "scraper": "browser_scraper",
    "selectors": {
        "container": "current_selector",
        "title": "current_title_selector",
        // Optional: Wait for specific element (Critical for CSR)
        "wait_for": "selector_that_appears_last" 
    }
}
```

### 3. Validation
Run the scraper in isolation on the VPS (or local Docker):
```bash
docker compose run --rm bot python main.py --council [id] --scrape-only
```

### 4. Tuning
If it fails:
- **Timeouts**: Increase wait time.
- **Selectors**: Use `page.content()` debug dumps to see the rendered DOM.
- **Resources**: Ensure CSS is allowed if it affects visibility.

## 🧹 Housekeeping & Maintenance

### Immediate Tasks
1.  **Memory Management**: The `browser_scraper` is memory intensive (headless Chromium).
    - *Action*: Monitor VPS memory. If OOM occurs, reduce `MAX_WORKERS` for browser batches.
2.  **Cleanup**:
    - Remove temporary debug files (`debug_*.html`, `debug_*.py`).
    - Standardize logging in `browser.py`.
3.  **Selector Audit**:
    - Many WAF sites are OpenCities and share the same structure. Once one is fixed (e.g., Campbelltown), the pattern can be applied to many.

## 🚀 Execution Strategy
1.  **Phase 1**: Enable `browser_scraper` for 5 high-profile WAF councils.
2.  **Phase 2**: Analyze success rate.
3.  **Phase 3**: Roll out to remaining WAF list in batches of 10.
