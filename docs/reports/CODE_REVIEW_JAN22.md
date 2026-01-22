# Code Review & Recovery Plan (Jan 2026)

## 1. Production Runtime State
- **Core Logic**: Patched (`utils.py`) to strict date parsing.
- **Bot Behavior**: Safe. Malformed data is rejected (returns `None` for date).
- **Database**: Cleaned of ~60 malformed future-dated rows.
- **Active Threats**: 
  - `Mackay` (QLD) and `Narromine` (NSW) were identifying random text as dates.
  - While `utils.py` fix prevents the *date* coming through, these scrapers are likely still scraping garbage titles or "Links" that aren't news (e.g. Navigation items).
- **Status**: **STABLE**.

## 2. Risk Mitigation (Actioned)
To prevent "Ghost Articles" (valid title, no date -> archived) or further weirdness, the following councils have been **DISABLED**:
1.  **Mackay Regional Council** (`mackay`) - QLD
    - Reason: `date_selector: "p"` grabs random paragraphs.
    - Status: Disabled pending new scraper config.
2.  **Narromine Shire** (`narromine-shire-council`) - NSW
    - Reason: Scrapes "Lot 112 DP..." addresses as news items.
    - Status: Disabled.
3.  **City of Kwinana** (`kwinana`) - WA
    - Reason: Scrapes "6175" (postcode/counter) as date.
    - Status: Disabled (Alyka CMS).

## 3. Next Steps (Recovery)
The immediate focus changes from **Expansion** to **Stabilization**.

### Phase 1: Deep Clean (Done)
- [x] Fix `utils.parse_date` logic.
- [x] Purge bad data from DB.
- [x] Disable known offenders.

### Phase 2: Targeted Repairs (Next)
1.  **Re-enable WA**: Focus on `Bayswater` and `Vincent`. WA is the primary pilot region.
2.  **Alyka Scraper**: Build a dedicated scraper for Kwinana, Stirling, Swan, Rockingham.
    - These share the same CMS (Alyka).
    - Current `catalyst` or `curl` scrapers are failing on them.
3.  **Squiz Matrix Scraper**: Build/Config for Mackay/Narromine.

## 4. Learnings
- **"Fuzzy is Fatal"**: `dateutil.parse(fuzzy=True)` is too dangerous for unsupervised scraping.
- **"Selectors Matter"**: Default fallbacks in `CardScraper` can pick up navigation menus if not scoped by `item_selector`.
- **"Silence is Golden"**: It is better to have a silent bot than a hallucinating one.

## 5. Deployment
- Changes to `councils.json` must be deployed to VPS to take effect.
- Run: `python3 scripts/deployment/deploy_with_password.py`
