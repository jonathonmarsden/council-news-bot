# Global Health Audit 2026

**Date:** January 22, 2026
**Scope:** All 540 configured councils
**Tool:** `scripts/comprehensive_health_check.py`

## Executive Summary

Following the targeted recovery of Western Australia councils, a project-wide health check was conducted to establish a new baseline. The system is currently achieving an **87.2% success rate** across all monitored councils.

- **Total Councils:** 540
- **Operational:** 471
- **At Risk (Zero Articles):** 69
- **Critical Failures:** 0

## State-by-State Performance

| State | Councils | Healthy | At Risk | Success Rate | Status |
|-------|----------|---------|---------|--------------|--------|
| TAS   | 29       | 29      | 0       | **100.0%**   | ✅ Exemplary |
| ACT   | 1        | 1       | 0       | **100.0%**   | ✅ Exemplary |
| VIC   | 79       | 77      | 2       | **97.5%**    | ✅ Exemplary |
| SA    | 69       | 62      | 7       | **89.9%**    | 🟢 Good |
| QLD   | 78       | 70      | 8       | **89.7%**    | 🟢 Good |
| NSW   | 128      | 112     | 16      | **87.5%**    | 🟢 Good |
| NT    | 18       | 15      | 3       | **83.3%**    | 🟡 Watch |
| WA    | 138      | 105     | 33      | **76.1%**    | 🔴 Attention Required |

## Analysis of "At Risk" Cohort (69 Councils)

The 69 councils returning zero articles likely fall into three categories:
1.  **Selector Drift:** The website layout has changed, breaking the CSS/XPath locators.
2.  **Anti-Bot Protection:** Implementation of stricter WAF rules (Cloudflare, etc.) blocking the scraper.
3.  **Dormant News Feeds:** Smaller regional councils (especially in WA/NT) may genuinely have no news in the scraped period.

### Western Australia (WA) - The Current Frontier
WA remains the lowest performing state (76.1%), with 33 councils in the "At Risk" category. This is the primary target for the next phase of optimization.
**Key Focus Areas:**
- **Armadale & Swan:** Known complex sites (React/API needed).
- **Regional Shires:** Many small shires (e.g., Dumbleyung, Nannup, Sandstone) likely suffer from "Dormant News" or simple selector tweaks.

### Eastern States
- **VIC & TAS:** Highly stable. The minimal failures in VIC (East Gippsland, Wellington) should be easy fixes.
- **NSW:** 16 failures is a manageable backlog. Large councils like Northern Beaches and Lake Macquarie likely have bot protection or complex DOMs.

## Recommendations & Next Steps

1.  **WA Consolidation (Phase 2):**
    - Address the 33 failing WA councils.
    - Differentiate between "Broken" and "Empty" (verify manually if news exists).
    - Implement `AlykaScraper` or custom handlers for the complex ones (Armadale/Swan).

2.  **Triage "Zero Article" Warnings:**
    - Run a secondary "Deep Scan" on the 69 warning councils with increased timeout or different user agents to rule out transient issues.
    - Manually inspect a sample of 5-10 from NSW/QLD to identify potential pattern breaks (e.g., a common CMS update).

3.  **Documentation Update:**
    - Update `README.md` with these fresh statistics.
    - Archive the raw `HEALTH_CHECK_REPORT_2026.md` for historical comparison.

## Conclusion
The system is robust and stable. The absence of critical exceptions (0%) indicates the error handling framework is working perfectly. The focus now shifts from "Crash Prevention" to "Coverage Expansion".
