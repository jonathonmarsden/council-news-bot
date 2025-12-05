# LGA Coverage Audit Report

**Date**: 2025-12-04
**Reference**: `_archived_old_code/LGA_2025_AUST.csv`

## Summary
The project configuration has been audited against the 2025 LGA list.
- **Total LGAs in CSV**: 541
- **Project Coverage**: 538 / 541 (99.4%)
- **Missing**: 3 (Special Administrative Areas)

## Detailed Findings

### Fully Covered States
The following states have 100% coverage (accounting for naming variations):
- **New South Wales (NSW)**: 128/128
- **Victoria (VIC)**: 79/79
- **Queensland (QLD)**: 78/78
- **Western Australia (WA)**: 138/138
- **Tasmania (TAS)**: 29/29
- **Australian Capital Territory (ACT)**: Project includes `ACT Government` (not in LGA list, but covers the territory).

### Missing Areas

#### South Australia (SA)
**Missing (2):**
1.  **Anangu Pitjantjatjara Yankunytjatjara (APY)**
    - *Type*: Aboriginal Local Government Area.
    - *Status*: Excluded.
    - *Reason*: Land holding body/Administration. No active news feed found (likely static or internal).
2.  **Maralinga Tjarutja**
    - *Type*: Aboriginal Local Government Area.
    - *Status*: Excluded.
    - *Reason*: Land council. Website (`maralingatjarutja.com.au`) is static (e.g., displaying 2021-2022 reports) and lacks a regular news stream.

*Note: All other 68 SA councils are present.*

#### Northern Territory (NT)
**Missing (1):**
1.  **Darwin Waterfront Precinct**
    - *Type*: Corporation / Precinct (Statutory Authority).
    - *Status*: Excluded.
    - *Reason*: Statutory authority managing a specific precinct. Website (`corporate.waterfront.nt.gov.au`) focuses on corporate reporting and precinct management, not general community news.

## Conclusion
The project is effectively up-to-date. The 3 missing entries are special purpose administrative areas rather than standard municipal councils and have been verified as not having suitable news feeds for this project. No standard councils are missing.
