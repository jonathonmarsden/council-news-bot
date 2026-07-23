# SparkCMS / Catalyst Rollout Report (Jan 23, 2026)

## 📌 Executive Summary
Upon discovering the `.module-list .row` platform signature (tentatively "SparkCMS" or a specific "Catalyst" generic template), we conducted a full scan of all Western Australian councils.

**Result**: We identified ~70 councils using this platform.
**Action**: We immediately reactivated **13 previously disabled councils** by standardizing them to the `curl_scraper` with the identified selectors.

## 🛠 Technical Details

### The Platform Signature
The platform is identifiable by:
-   **List Container**: A `div` with class `module-list`.
-   **Item**: A `div` with class `row` inside the list.
-   **Title**: `span.h4` (often with `text-primary`).
-   **Date**: `span.h5` immediately preceding the title.
-   **Link**: `a.btn` (usually "Read More").

### Standard Configuration
The following configuration has been applied to all remedied councils:

```json
{
    "scraper": "curl_scraper",
    "item_selector": ".module-list .row",
    "title_selector": "span.h4",
    "date_selector": "span.h5",
    "link_selector": "a.btn",
    "use_curl": true,
    "enabled": true
}
```

## 📋 Remediation List (13 Councils Unlocked)
The following councils were previously disabled or broken and are now active:

1.  **City of Kalgoorlie-Boulder** (`kalgoorlie-boulder`)
2.  **City of Nedlands** (`nedlands`)
3.  **Shire of Bassendean** (`bassendean`)
4.  **Shire of Beverley** (`beverley`)
5.  **Shire of Bruce Rock** (`bruce-rock`)
6.  **Shire of Cunderdin** (`cunderdin`)
7.  **Shire of Derby-West Kimberley** (`derby-west-kimberley`)
8.  **Shire of Exmouth** (`exmouth`)
9.  **Shire of Kellerberrin** (`kellerberrin`)
10. **Shire of Koorda** (`koorda`)
11. **Shire of Menzies** (`menzies`)
12. **Shire of Mukinbudin** (`mukinbudin`)
13. **Shire of Mundaring** (`mundaring`)

## 🔍 Additional Findings
-   **Catalyst Scraper Redundancy**: The existing `catalyst_scraper` appears to target this exact platform. Eventually, `catalyst_scraper.py` could be deprecated in favor of this standardized configuration to reduce code maintenance.
-   **Coverage**: This platform accounts for ~50% of WA councils, making it the single largest target in the state.

## 🚀 Next Steps
-   **Monitor**: Watch the logs for these 13 councils over the next 24 hours.
-   **Expand**: Re-scan NT and other states specifically for this signature (although NT was mostly covered in Phase 1).
