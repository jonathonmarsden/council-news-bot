# Phase 3: Western Expansion (The Final Frontier)

## Mission
Achieve 100% coverage of Western Australia's 137 Local Governments. Currently, ~28 councils are missing or failing. This phase focuses on closing that gap.

## Strategy
1.  **Audit**: Identify the missing LGAs.
2.  **Triage**: Categorize them:
    *   **Low Hanging Fruit**: Simple selector fixes.
    *   **WAF Blocks**: Apply Phase 2 "WAF Key" (Chrome124 + Proxy).
    *   **Difficult**: PDF-only sites, SPAs, or malformed HTML.
3.  **Execute**: Implement fixes in batches of 5.

## Tools
- `scripts/audit_lga_coverage.py`: The map.
- `scripts/debug/research_waf_bypass.py`: The hammer.
- `scripts/auto_discover_selectors.py`: The scalpel.

## Progress Tracking
| Batch | Status | Notes |
| :--- | :--- | :--- |
| **Batch 1 (Major Metros)** | 🟡 Planned | Albany, Armadale, Bayswater, Belmont, Cambridge |
| **Batch 2 (Regional Hubs)** | ⚪ Pending | Broome, Collie, Karratha, Mosman Park, Augusta-Margaret River |
| **Batch 3 (Rural)** | ⚪ Pending | Remaining Shires |

## Target List (Batch 1 Candidates)
Based on `docs/WA_GAP_ANALYSIS.csv`:
1.  **City of Albany**
2.  **City of Armadale**
3.  **City of Bayswater**
4.  **City of Belmont**
5.  **Town of Cambridge**
