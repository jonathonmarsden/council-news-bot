# WA Scraper Recovery Plan: "The Quality Reset"

## Context
The Western Australia (WA) scraper configuration has degraded into a game of "whack-a-mole". Unlike the mature VIC and NSW configurations, many WA entries rely on implicit defaults within `CardScraper` rather than explicit CSS selectors. This has led to:
- Truncated titles (grabbing "Read more..." text).
- Meaningless bodies (grabbing navigation text or "Click here").
- HTML tag leakage (fixed in code, but symptom of poor parsing).

## The "Prompt to Self" (Strategy)

**Objective**: Elevate WA to the reliability standard of VIC/NSW by enforcing explicit configuration and implementing content quality gates.

### Phase 1: The Audit (Immediate)
1.  **Identify "Naked" Configs**: Scan `states/wa/councils.json` for entries using `card_scraper` without `item_selector`, `title_selector`, or `link_selector`.
2.  **Analyze Failure Patterns**: The "bad posts" list provided by the user is the training set.
    - *Cranbrook*: Body is "Click link". -> Needs `content_selector` targeting the actual article text, not the summary.
    - *Fremantle*: HTML tags. -> Fixed by code, but needs verification.
    - *Irwin*: "Council Update" title. -> Likely grabbing a section header instead of article title.
    - *Trayning*: Truncated text. -> Selectors are grabbing UI elements.

### Phase 2: The Standardization (Execution)
1.  **Enforce Explicit Selectors**:
    - **Rule**: No WA scraper shall rely on defaults. Every active scraper must define:
        - `item_selector`: The container for the news card.
        - `title_selector`: The specific element containing the headline.
        - `link_selector`: The anchor tag pointing to the full article.
        - `date_selector`: (Where available) The date element.
2.  **Implement "Quality Gates" in Code**:
    - Update `BaseScraper` or `CardScraper` to reject/warn on:
        - Titles containing "Read more", "Click here", "...", or length < 10 chars.
        - Bodies containing raw HTML tags (regex check).
        - Bodies shorter than 50 chars (unless it's a pure link post).

### Phase 3: The Fix (Specifics)
Apply immediate fixes to the reported offenders:
- **Cranbrook**: Locate the actual news list container.
- **Fremantle**: Verify the new `create_article` fix works; ensure selectors aren't grabbing hidden metadata.
- **Irwin**: Find the specific news item selector to avoid generic headers.
- **Trayning**: (Already partially addressed, but needs review against new strict standard).

## Actionable Next Steps
1.  Run a script to list all "naked" WA scrapers.
2.  For each "naked" scraper, visit the `news_url`, inspect the DOM, and write specific selectors.
3.  Update `states/wa/councils.json` in batches.
