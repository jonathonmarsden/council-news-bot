# Malformed Posts Remediation & Continuous Scraper Improvement

## Goals
- For each malformed/low-quality post: diagnose, fix the source scraper/config, delete the bad post, requeue/repost correctly, and harden scrapers over time.
- Continuously codify "what good looks like" and reuse proven patterns across similar councils/platforms.

## Inputs
- Malformed posts list (URI, handle, external_url, original text).
- Scraper configs per council (`states/<state>/councils.json`) plus platform hints (OpenCities, ASP.NET, WordPress, RSS, etc.).
- Well-formed examples:
  - https://bsky.app/profile/roundupnewsbotact.bsky.social/post/3m7ad5sqyml2p
  - https://bsky.app/profile/roundupnewsbottas.bsky.social/post/3m7b7xqemmu25
  - https://bsky.app/profile/roundupnewsbotnsw.bsky.social/post/3m7bgwfurqp2a
  - https://bsky.app/profile/roundupnewsbotqld.bsky.social/post/3m7blp2z6722f
  - https://bsky.app/profile/roundupnewsbotqld.bsky.social/post/3m7c3mjdxxb2u

## Target Post Structure (no emojis)
- Line 1: Title (≤120 chars ideally; no body bleed; trimmed; sentence case unless proper noun). Title is clickable and links to the article URL.
- Line 2: Excerpt (optional; ≤120 chars ideally; drop if noisy/CTA/menu).
- Line 3: Date in human-readable form (e.g., 7 December 2025). If no reliable date, skip posting—except newly discovered undated items after the initial scrape (see freshness rule).
- Line 4: Council name as published (e.g., "City of Whittlesea").
- Line 5: Hashtags, max 4–6, ordered:
  1. #LGNewsRoundup
  2. State peak body (e.g., #VLGA, #LGNSW, #LGAQ, #WALGA, #LGASA, #LGANT, #LGAT, #ALGA/#LGACT)
  3. State councils tag (e.g., #VicCouncils, #NSWCouncils, #QLDCouncils, #WACouncils, #SACouncils, #NTCouncils, #TASCouncils, #ACTCouncils)
  4. Full council hashtag (e.g., #CityOfWhittlesea), plus any remaining agreed tags (distinct; no extras).

## Freshness Rule (queueing undated after first scrape)
- Initial scrape can be strict, but on second and subsequent scrapes: queue every newly seen post even if undated. Treat newly discovered undated items as fresh-by-discovery. Dated items post only if within the freshness window (currently 7 days). Never fabricate dates.

## Facet Rules
- Facets only on hashtags and the URL; byte ranges must match exact substring spans.
- Do not facet hashtags embedded inside titles.
- Titles must not exceed ~150 chars and must not include body/summary.

## Diagnostics Checklist per Malformed Post
1. Title too long or merged with body? Tighten title selector/scope; drop body nodes; ensure node text only.
2. Missing/garbled date? Adjust date selector; parse; if absent and newly discovered after initial scrape, allow undated-fresh; otherwise skip posting.
3. Wrong council name? Map from config; avoid scraping names from unstable elements.
4. Bad facets (overlap/length)? Rebuild facets from clean text; ensure spans match hashtags/URL only.
5. Noisy content (forms/menus/CTA)? Narrow container; filter non-article cards.

## Remediation Steps
- Inspect malformed text and external_url; open page to confirm title/date/council/excerpt.
- Reuse platform templates (OpenCities/ASP.NET/WP/RSS) from the Optimized Scraper Traits library before ad-hoc selectors.
- Update scraper config/code (container/title/date/link selectors, excerpt hygiene). If date unreliable, still allow newly discovered undated items after initial scrape; otherwise skip.
- Validate composition before posting: lengths, facets, hashtags ordering, URL sanity (no mailto/tel/login/tracking junk).
- Re-run scraper (scrape-only) to repopulate DB; post-only run to publish corrected items (respect per-council caps).
- Delete malformed post via full URI with the admin bot.
- Verify final post matches structure; facets valid; title/excerpt clean.
- Log changes (selectors/CMS pattern), councils cloned for patterns, and any disables.

## Edge Rules
- Never invent dates. Undated is allowed only when newly discovered after the first scrape; old undated items are skipped.
- Strip whitespace, collapse spaces, remove control chars.
- No emojis.
- Keep hashtags to the agreed set and order; no random tags.
- If site blocks scraping or is too dynamic, disable council and document reason.

## Optimized Scraper Traits (source of truth)
- Maintain per-platform templates: selectors for title/date/link/container, date formats, excerpt strategy, pagination, blocklists/allowlists, known pitfalls.
- Keep a state→hashtags map and council→canonical-name map; scrapers should not guess tags/names.
- Record council-specific quirks (meta dates, text_content vs inner_html, pagination rules, dynamic sections to ignore).
- When fixing a council, add any improvements back to this library.

## Guardrails and Validation
- Compose-then-validate locally: enforce title/hashtag/URL lengths, facet spans, and hashtag order before posting.
- URL hygiene: reject mailto/tel/login/query-heavy/tracking URLs; ensure same-host unless whitelisted.
- Excerpt hygiene: no links/hashtags/CTAs; drop if noisy.
- Regression guard: when fixing, test against multiple archived pages if available; note before/after.
- Safe mode: use dry-run/preview when uncertain; auto-disable on repeated failures with a logged reason.
- Queue policy clarity: log "fresh-by-discovery undated" vs "stale-undated skip" for auditability.
- Cleanup: always delete malformed originals after successful repost; if repost fails, leave queued and flag.
