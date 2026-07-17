# Broken Councils Repair Plan — 2026-07-17

**Ground truth** (all-councils harness, residential IP = production egress, 2026-07-17):
**510/532 ok. 22 broken.** The June backlog of 27 is fully healed (residential IP + the
July config fixes) — `docs/broken_councils.json` is stale and gets rewritten in R4.
These 22 fail identically with/without proxy and from both the old droplet and Rakali:
they are content-side rot (dead feeds, changed markup, path-specific blocks), not
infrastructure. Every fix is config-first; code changes only if a platform genuinely
changed shape.

## The 22, bucketed by failure mode

### Bucket B — selector rot on plain-fetch pages (10) — *easiest, highest yield*
Page fetches fine (HTTP 200), configured `item_selector` matches 0 elements → markup changed.

| Council | Scraper | Note |
|---|---|---|
| vic/bayside, vic/buloke, vic/greater-geelong, vic/mansfield, vic/wyndham | curl | 5 VIC councils at once — check for a shared re-platforming (possible NEW cascade) |
| nt/barkly | card | |
| qld/pormpuraaw, qld/south-burnett | curl | pormpuraaw is tiny; may have near-zero news volume — verify content exists at all |
| sa/burnside | card | |
| tas/glenorchy | card | |

**Method per council:** fetch the live page → fingerprint platform (meta generator,
known CMS markers) → re-derive selectors (`scripts/analysis/suggest_selectors.py`
assists) → if re-platformed, switch scraper type to the matching engine →
verify `python3 main.py --council <id> --dry-run`.

### Bucket E — LGASA-variant empties (2)
| sa/yankalilla, tas/kentish | lgasa | fetches OK, 0 items — LGASA template variant drift |

Same method as B but inside `lgasa_scraper`'s selector assumptions; if only these two
variants diverge, prefer per-council selector overrides in config over code changes.

### Bucket A — dead or blocked feed URLs (3)
| Council | Symptom | First moves |
|---|---|---|
| nsw/bogan-shire-council | feed URL fetch fails | RSS autodiscovery on site; else scrape the HTML notices page (card/curl) |
| qld/yarrabah | /feed/ 404 — historically PDF-only news | if still PDF-only: `enabled: false` + reason (see R4) |
| vic/cardinia | /rss/news 403 — WAF blocks the feed path only | try `use_curl`+impersonation on the feed; else scrape the HTML news page |

### Bucket C — browser scrapers finding 0 items post-JS (3)
| wa/harvey, wa/mandurah, wa/subiaco | browser | page loads, hydrated DOM no longer matches selector |

**Method:** fingerprint first — sites that needed Playwright in 2025 may have
re-platformed to server-rendered CMSes (downgrade to card/curl = faster + lighter),
else re-derive selectors from the rendered DOM (`page.content()` dump).

### Bucket D — hard 403s that impersonation doesn't clear (4) — *hardest*
| Council | Symptom |
|---|---|
| wa/laverton, wa/murray | Catalyst platform, 403 on /news/ — both Catalyst: likely one platform-side rule |
| sa/berri-barmera, sa/mount-barker-district | lgasa listing URLs refuse fetch |

**Method:** establish exactly what's blocked (curl -v status/headers; page vs path;
GET vs HEAD): try the Catalyst JSON endpoint (`catalyst_browser_scraper`'s API route)
instead of the HTML listing; try `mobile_mode`, `safari15_5`, slower request pacing;
check whether the news page URL simply moved (fetch nav/sitemap). Last resort:
browser_scraper. If a site demonstrably blocks all automated access: R4 disable.

## Process

**R0 — ground truth: DONE** (this doc). Re-run `scripts/analysis/test_all_councils_noproxy.py`
before starting work if >1 week has elapsed — this set drifts (2 self-healed, 1 appeared
in the last 10 days alone).

**R1 — evidence dossiers (automated, read-only).** For each of the 22, gather in one pass:
HTTP status + headers of news_url, platform fingerprint, RSS autodiscovery links,
sitemap news paths, saved HTML/rendered-DOM snapshot. Fan out to subagents by bucket;
each returns a per-council diagnosis + proposed config.

**R2 — fixes in three PR batches**, each fix verified live (`--council <id> --dry-run`)
before commit:
- **PR batch 1:** Buckets B + E (12 councils, selector/config-only) — highest yield, lowest risk.
- **PR batch 2:** Bucket A (3) — feed replacements / scraper-type switches.
- **PR batch 3:** Buckets C + D (7) — browser re-derives and the hard 403s, plus any
  `enabled: false` decisions.

**R3 — end-to-end verification per batch.** Merge → pull-deploy (≤10 min) → reset the
fixed councils' breaker rows → confirm articles queue at the next staggered slot →
confirm posts on the state feeds within 24–48h (`triage_coverage.py` reconciles feeds
vs configs). Success criterion: **≥525/532 ok** on the harness, and every enabled
council either present in its feed's 7-day window or explainably quiet.

**R4 — closeout.** Rewrite `docs/broken_councils.json` from the post-repair harness run
(it currently lists 27 healed councils and none of the real 22). For genuinely
unfixable sites (PDF-only, hard-blocked): set `enabled: false` with a
`"disabled_reason"` note in councils.json (extra keys are ignored by the loader) so
they stop cycling the circuit breaker, and add them to a quarterly re-check list in
`docs/SCRAPER_REPAIR_PLAYBOOK.md`. Update the playbook with any new cascade recipes
(the 5-VIC cluster is a candidate).

## Effort & sequencing

- **~2 working sessions.** Session 1: R1 dossiers + PR batch 1 (B/E are mechanical with
  the dossier in hand, ~15–30 min/council with agent fan-out). Session 2: batches 2–3
  (the 403 forensics is the long pole) + R3/R4 closeout.
- **User involvement:** merging 3 PRs; nothing else.
- **When:** dossiers (read-only) can run any time; land batch 1 after the migration's
  48h observation window closes (2026-07-19) so scraper-config changes don't confound
  the migration soak. Batches 2–3 in the following days.
- **Expected end state:** ~525–529/532 scraping (98–99%), the remainder explicitly
  disabled-with-reason instead of silently cycling the breaker.

## Guardrails

- Every fix is verified against the live site before commit, from a residential IP
  (Mac or Rakali — same egress).
- No code changes to shared scrapers without checking blast radius (a selector change
  in `lgasa_scraper` touches 56 councils — prefer config overrides).
- Batches are small and independently revertable; pull-deploy makes rollout and
  rollback a merge/revert each.
- Post-batch, the existing watchdogs are the regression net — any council a fix
  accidentally breaks resurfaces as a failure alert, not silence.
