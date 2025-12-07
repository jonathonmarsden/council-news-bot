# Platform Templates (Optimized Scraper Traits)

Use these as first-choice patterns before ad-hoc selectors. Record quirks and reuse.

## OpenCities
- Container: `.row:has(.news-image-wrapper)` or `.news-item`
- Title: `span.h4.text-primary, span.h4, h2, .h4`
- Date: `span.h5, .date`, prefer top-level meta if available
- Link: `a.btn.btn-primary[href*='/news/']` or anchor within card
- Notes: Strip menus/CTAs; watch for pagination params; dates often plain text.

## ASP.NET (classic)
- Container: `article`, `.news-item`, `.row:has(.news-image-wrapper)`
- Title: `h2`, `.title`
- Date: `.date`, `.entry-meta`
- Link: `a` within the item
- Notes: Beware viewstate pages; prefer server-rendered listings; avoid form links.

## WordPress
- Container: `article`, `.post`, `.entry-card`
- Title: `h2.entry-title a`, `a.entry-title`
- Date: `time`, `.entry-date`, `meta[property='article:published_time']`
- Link: the anchor on title
- Notes: Normalize smart quotes; check for lazy-loaded content; drop category tags.

## RSS
- Source: feed URL
- Title: `<title>`
- Date: `<pubDate>` or `<updated>`
- Link: `<link>`
- Notes: Trim whitespace; decode HTML entities; respect feed timezone.

## Generic Card Scraper
- Container: minimal card wrapper; avoid page-wide rows
- Title: heading within card; avoid excerpts and buttons
- Date: sibling small-text; avoid relative dates
- Link: primary anchor in card
- Notes: Blocklist menu/footer cards; require absolute/valid URLs.

## Patterns and Pitfalls
- Prefer `text_content` over `inner_html` to avoid HTML artifacts in titles/excerpts.
- Resolve relative URLs; reject mailto/tel/login/tracking-heavy URLs.
- Date priority: meta published > explicit date node > skip (unless undated fresh-by-discovery after first scrape).
- Excerpt: optional; drop if it contains links, hashtags, or CTAs.
- Pagination: capture next-page selectors where applicable; avoid infinite-scroll without automation.

## Recording Improvements
When fixing a council:
- Note platform used and selectors chosen.
- Add quirks (e.g., meta dates only, needs `.text_content()`, remove “Read more”).
- Feed improvements back into this list and the council’s config.
