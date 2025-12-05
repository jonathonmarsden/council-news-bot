# Final Report: WA Date Fixes & Zero-Yield Audit
**Date:** 2025-12-05

## 1. Western Australia (WA) Date Fixes

The following 5 WA councils were identified as having date parsing failures. All have been fixed and verified.

| Council | Issue | Fix Applied | Status |
|---------|-------|-------------|--------|
| **Bunbury** | Next.js frontend made HTML parsing difficult. | **Rewrote scraper** to use WordPress API (`wp-json/wp/v2/posts`). | ✅ Fixed |
| **Carnamah** | Date selector was incorrect. | Updated CSS selector in `councils.json`. | ✅ Fixed |
| **Donnybrook-Balingup** | Date selector was incorrect. | Updated CSS selector in `councils.json`. | ✅ Fixed |
| **Kent** | Date selector was incorrect. | Updated CSS selector in `councils.json`. | ✅ Fixed |
| **Mingenew** | Date not in body text. | Updated to extract `article:published_time` from meta tags. | ✅ Fixed |

**Verification:**
A debug script `debug_wa_dates.py` was created and executed, confirming that all 5 councils now successfully extract dates.

## 2. Zero-Yield Audit

A comprehensive audit was performed to identify all **enabled** councils that have **0 articles** in the database. This indicates a likely failure in the scraper (broken selector, blocked IP, changed URL, or empty feed).

**Summary:**
- **Total Enabled Councils:** ~539
- **Zero-Yield Councils:** 257
- **Failure Rate:** ~47%

**Key Findings:**
- A significant number of councils in NSW, SA, and WA are returning 0 articles.
- Many of these sites likely share common platforms (e.g., OpenCities, WordPress) where a single fix pattern could resolve multiple issues.

**Detailed List:**
The full list of 257 zero-yield councils has been saved to:
`ZERO_YIELD_COUNCILS.md`

## 3. Recommendations

1.  **Batch Fixes:** Group the zero-yield councils by platform (e.g., all WordPress sites) and apply fixes in batches.
2.  **Bunbury Pattern:** The WordPress API approach used for Bunbury should be tested on other WordPress-based councils in the zero-yield list.
3.  **Disable Dead Scrapers:** If a council has no news or is permanently broken, it should be disabled in `councils.json` to save resources.
