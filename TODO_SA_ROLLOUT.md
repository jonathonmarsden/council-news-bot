# Outstanding Tasks for SA Rollout

## Current Status
- Identified 6 broken SA councils (Batch 5): Naracoorte, Northern Areas, Norwood, Onkaparinga, Orroroo, Peterborough.
- Implemented `cloudscraper` support in `BaseScraper` and `ScraperFactory`.
- Updated `states/sa/councils.json` to use `use_cloudscraper: true` for these councils.
- Created `test_factory_cloudscraper.py` to verify the fix.

## Issues
- `test_factory_cloudscraper.py` for Naracoorte is failing to extract articles.
- The HTML is being fetched successfully (saved to `debug_naracoorte_factory.html`).
- The scraper finds the items (`div.card-listing__item`) but fails to extract the title.
- Debugging revealed that `_get_clean_title` is returning empty strings or failing to find the title element, possibly due to the structure of the `a` tag or how `get_text` is handling the children.

## Next Steps
1.  **Fix Title Extraction**: Debug `CardScraper._parse_article` and `_get_clean_title` to correctly handle the Naracoorte HTML structure. The title seems to be inside a `div` inside the `a` tag, or the `a` tag text itself is being cleaned away aggressively.
2.  **Verify Other Councils**: Once Naracoorte is fixed, run the test script against the other 5 councils to ensure the fix works for them as well.
3.  **Finalize Config**: Ensure `states/sa/councils.json` is correct for all 6 councils.
