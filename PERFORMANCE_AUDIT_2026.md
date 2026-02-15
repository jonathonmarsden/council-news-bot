# Performance Audit Report - Jan 23 2026

## Executive Summary
A comprehensive audit of the production database was conducted to assess the performance of all 537 council scrapers.

**System Health**: ✅ Excellent
- **Failing Scrapers**: 0 (No runtime errors)
- **Stale Scrapers**: 0 (All scrapers have run successfully within 48h)
- **Active Coverage**: 527 Councils tracked in DB.

## Critical Issues: Silent "Empty" Failures
The following 11 councils are running successfully but returning **0 articles** consistently (20+ consecutive empty runs). This indicates broken selectors or changed website layouts. All detected issues are in **NSW**.

| State | Council | Consecutive Empty Runs | Likely Cause |
|-------|---------|------------------------|--------------|
| NSW | Wollondilly Shire Council | 24 | Broken Selector / Layout Change |
| NSW | Lithgow City Council | 23 | Broken Selector / Layout Change |
| NSW | Lockhart Shire Council | 23 | Broken Selector / Layout Change |
| NSW | Murray River Council | 23 | Broken Selector / Layout Change |
| NSW | Murrumbidgee Council | 23 | Broken Selector / Layout Change |
| NSW | Shellharbour City Council | 23 | Broken Selector / Layout Change |
| NSW | Snowy Valleys Council | 23 | Broken Selector / Layout Change |
| NSW | Upper Lachlan Shire Council | 23 | Broken Selector / Layout Change |
| NSW | Lake Macquarie City Council | 22 | Broken Selector / Layout Change |
| NSW | Bogan Shire Council | 22 | Broken Selector / Layout Change |
| NSW | Narrandera Shire Council | 22 | Broken Selector / Layout Change |

## Technical Debt: ID Matching
A significant mismatch was detected between the Canonical Name list (JSON) and the Database Keys (Slug).
- **Impact**: ~400 councils could not be automatically cross-referenced in the report (reported as "Missing" despite likely being present).
- **Root Cause**: Inconsistent slug logic between `ScraperFactory` (legacy) and the reporting script.
- **Action**: Standardize DB ID generation to be robust against name formatting changes.

## Next Steps
1. **Targeted Fixes**: Inspect and repair the 11 NSW councils listed above.
2. **ID Unification**: Run a one-off database migration or update the report map to link JSON Configs to DB Records accurately.
