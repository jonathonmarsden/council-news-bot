# Session Handover (2026-01-22)

## Crisis Response: Malformed Post Cleanup
We have successfully engineered a solution to fix the "Malformed Post" regression (where the fixer script was guessing names incorrectly).

### 1. The Fix mechanism
We replaced the "Heuristic" guessing (which failed on Townsville/Search URLs) with a **Hybrid Safelist**:
- **Layer 1: Domain Map**: Lookup `scripts/council_domain_map.json`. 
    - UPDATED: Now supports aliases (e.g., `townsville.qld.gov.au` maps from `squiz.cloud`).
- **Layer 2: Text Safelist**: If URL lookup fails, we scan the text for *exact* official Council Names defined in the database.
- **Fail Safe**: If neither matches, we SKIP the post rather than guessing.

### 2. Status
- **Scripts**: 
    - `scripts/build_council_map.py`: Updated to include cloud/alias support.
    - `scripts/process_bookmarks.py`: COMPLETELY REWRITTEN to use the safe logic.
    - `scripts/dry_run_audit.py`: Verified "Townsville" is now detected correctly in Safe Mode.
- **Environment**: Clean. Malformed posts were deleted earlier.
- **Documentation**: Added `docs/LEARNINGS_MALFORMED_FIX.md`.

### 3. Immediate Next Steps
1.  **Run the Fixer**: Execute `python3 scripts/process_bookmarks.py` to process the bookmark queue with the new safe logic. (User to trigger).
2.  **Monitor**: Watch the logs for "Retitle" actions.
3.  **Deployment**: Ensure these script changes are deployed to the VPS (`deploy_with_password.py`) if the fixer runs there (though the fixer is often run locally as Admin).

## Files Modified
- [`scripts/process_bookmarks.py`](scripts/process_bookmarks.py): The main fix logic.
- [`scripts/build_council_map.py`](scripts/build_council_map.py): Added overrides for cloud hosts.
- [`scripts/council_domain_map.json`](scripts/council_domain_map.json): Regenerated map.
- [`docs/LEARNINGS_MALFORMED_FIX.md`](docs/LEARNINGS_MALFORMED_FIX.md): Incident report.
- [`TODO.md`](TODO.md): Checked off tasks.

## Maintenance Tools (Added 2026-01-22)

We established a comprehensive health check workflow to audit the entire national network.

### 1. Full System Audit
Run the comprehensive health check to test every scraper in the system (dry-run, no database writes):
```bash
python3 scripts/comprehensive_health_check.py
```
This generates `HEALTH_CHECK_REPORT_2026.md`.

### 2. Architecture Analysis
To visualize the scraper distribution (Card vs Curl vs Custom) across states:
```bash
python3 scripts/analyze_state_scrapers.py
```

### 3. Key Findings (Jan 2026)
- **Health**: 85.9% of councils are active.
- **Victoria**: Best performing state (97.5%) due to standardization on `curl_scraper` (evading bot protections).
- **Western Australia**: Requires attention (76%) due to custom scraped fragmentation.
- See [`PROJECT_LEARNINGS_2026.md`](PROJECT_LEARNINGS_2026.md) for full strategic analysis.

## Critical Production Fix (2026-01-22)

**Issue**: A severe regression caused most scrapers to crash with `TypeError: __init__() got an unexpected keyword argument 'enabled'`.
**Cause**: The `ScraperFactory` passes all extra configuration keys (like `enabled`, `hashtags`, etc.) to the scraper constructor as `**kwargs`. Many scraper classes (CardScraper, RSSScraper, etc.) did not accept `**kwargs` in their `__init__` method, causing them to reject these extra keys.
**Resolution**: Updated ALL scraper classes (`CardScraper`, `RSSScraper`, `CatalystScraper`, `WannerooScraper`, etc.) to accept `**kwargs` and pass them to `super()`.
**Rule**: Any new scraper class MUST accept `**kwargs` in `__init__` to be compatible with the Factory's configuration injection.

