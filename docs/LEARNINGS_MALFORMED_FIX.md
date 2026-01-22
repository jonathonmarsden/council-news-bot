# Malformed Bookmark Handling Learnings (2025-01-22)

## Incident Summary
We attempted to clean up "malformed" bookmarks (badly scraped titles/dates) but the initial "Fixer" script caused a regression by reposting content with guessed Council Names. This resulted in posts like "LGNewsRoundup VLGA NSWCouncils..." appearing as the Council Name.

## Key Findings

1.  **Pagination is Critical**: The initial monitoring script missed ~50 older bad bookmarks because it lacked pagination.
    *   *Fix*: All scripts now iterate through bookmark cursors until exhaustion.

2.  **Heuristics are Dangerous**: Guessing the "Council Name" from the malformed text (e.g., "Line before the hashtags") failed spectacularly when the text format varied.
    *   *Result*: It captured URLs or string fragments as names.
    *   *Pivot*: We moved to a **Safelist** approach.

3.  **Domain Mapping Limitations**: Rlying solely on the article URL domain to identify the Council fails when:
    *   Councils use third-party providers for media releases (e.g., `squiz.cloud`, `funnelback`).
    *   Scrapers pick up redirected or search-result links.
    *   *Result*: "Townsville" posts were unidentified because they linked to `tcc-search.funnelback.squiz.cloud`.

4.  **Hybrid Identification**: The robust solution combines:
    *   **Primary**: Domain Lookup (Safe).
    *   **Secondary**: Text scanning against a **Strict Safelist** of confirmed Council Names only.

5.  **Quality Gate Definition**: We formally defined a "Well-Formed Post":
    *   **Title**: Clean headline (no dates, no prefixes, clickable link).
    *   **Date**: Omitted if not strictly parseable.
    *   **Council**: Official Name only.
    *   **Tags**: `#PeakBody` `#State` `#Council`.

## Next Steps
- [ ] Implement the Hybrid Safelist in `process_bookmarks.py`.
- [ ] Add `tcc-search.funnelback.squiz.cloud` to the Domain Map alias for Townsville.
- [ ] Run the Fixer in "Safe Mode".
