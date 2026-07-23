# roundupnewsbot v3.0 report

**Report date:** 19 July 2026
**System version:** 3.0 (Production)
**Status:** Fully operational — best health in the project's history
**Follows on from:** v2.0 report, 16 February 2026

---

## Executive summary

Since the February report, the bot has been through its biggest overhaul yet. Three headlines:

1. **Coverage is now 100%.** Every one of the 534 enabled Australian councils is being scraped successfully — up from 95% in February. The last holdouts (remote Cape York councils that publish newsletters as PDFs) are now on the feeds too.
2. **It moved off the cloud and into the home office.** The bot now runs on Rakali, a small home server, instead of a rented cloud server. The paid proxy service is gone too. Running costs went from ~$31.50/month to effectively zero.
3. **It's dramatically more trustworthy.** A deep engineering review in early July found and fixed ~50 defects — including several that had been silently losing articles or silently disabling councils for months. The system's whole philosophy changed from "looks fine" to "fails loudly": if something breaks now, we know within hours, automatically.

There's also a public face now: **[lgnews.jonathonmarsden.com](https://lgnews.jonathonmarsden.com)** — one page showing all eight state feeds live, no login, no tracking, no paywall.

---

## What changed since v2.0 — the short version

| | February (v2.0) | July (v3.0) |
|---|---|---|
| Councils scraping successfully | 512 of 537 (95%) | **534 of 535 enabled (100%)** ¹ |
| Where it runs | Rented cloud server ($20/mo) | Rakali home server ($0) |
| Proxy service | Webshare ($10/mo) | **Cancelled — proven unnecessary** |
| Total running cost | ~$31.50/month | **≈ $0/month** |
| Articles in the database | ~13,800 | **35,796** |
| Database size | ~500 MB | 104 MB (leaner after cleanup) |
| Monitoring | Hourly Discord messages | Quiet-by-default alerts + daily digest + an independent off-site watchdog |
| Deploying new code | Push → cloud scripts → server | **Merging approved code *is* deploying** (the server updates itself within 10 minutes) |
| Duplicate-post protection | Best effort | Guaranteed exactly-once posting |
| Public face | None | lgnews.jonathonmarsden.com |

¹ One council (Pormpuraaw, QLD) is deliberately switched off with documented evidence: it genuinely publishes no news anywhere on its website. It gets re-checked quarterly.

**A note on posting volume, in the interest of honesty:** the February report quoted ~900 posts/day. Today the steady rate is 100–250 genuinely new stories per weekday. The old figure was inflated — the review found bugs that re-posted old articles, counted rejected posts as published, and let one council flood the queue. Today every story posts exactly once, and quiet weekends are quiet. Fewer, better posts.

---

## The July engineering review

In early July the entire codebase went under the microscope: roughly 50 verified defects, from cosmetic to critical. The important families:

- **Silent article loss.** A temporary Bluesky outage used to permanently discard every article that tried to post during it. Fixed — articles now wait and retry, with a sensible cap.
- **Silent council loss.** The "circuit breaker" that switches off broken scrapers was a one-way door: once off, a council could never come back without manual surgery, and network failures were miscounted in a way that quietly disabled 85+ councils at once (twice!). Now failures are counted honestly, disabled councils automatically retry every few days, and mass-disable events page us immediately.
- **Garbled text.** The mojibake (â€™-style characters) that occasionally marred posts was traced to its root cause — a text-encoding bug at download time — and fixed at the source rather than patched after the fact.
- **Wrong dates.** Eight separate places parsed Australian dates the American way round. All routed through one correct parser.
- **The watchmen now have watchmen.** The monitoring scripts themselves used to be able to die silently. They now report their own failures, and a second, independent watchdog runs every six hours from GitHub's computers — so even if the entire home server loses power, something external notices and raises the alarm.

## The move home — and why it made the bot *better*

The migration to the home server was planned as a cost-saving exercise. It turned out to be a coverage breakthrough.

While testing, we discovered that many council websites' security systems (especially South Australia's shared platform) **block traffic from data-centre internet addresses outright** — the cloud server's address class, and the paid proxy's too. The proxy we'd been paying for was being blocked by the exact websites it was meant to help with. From a normal home internet connection, those same websites answer happily.

So the move recovered **50–90 councils that the cloud server could never reach**, made the proxy genuinely useless (cancelled), and cut costs to zero. The migration itself ran in a single evening — database copied and verified to the last row, posting confirmed exactly-once, and the old server kept as a safety net for 48 hours before being destroyed.

Home hosting done properly, for the sceptics: the bot lives in an isolated container with nightly full-machine backups, daily database backups, no inbound internet exposure at all, and that off-site watchdog keeping honest score from outside the house.

## Finishing the map: the last 25 councils

July also closed the long-standing repair backlog:

- **22 broken scrapers repaired in one day** — mostly councils that had rebuilt their websites (a wave of Victorian councils re-platformed almost simultaneously). Every fix was verified against the live site before shipping.
- **The three "PDF-only" Cape York and outback councils** are now on the feeds. The trick: don't read the PDFs — post the newsletter's title with a link to the PDF, dated from its name ("Waanta Newsletter October 2025"). And one of the three turned out to have quietly launched a proper news page two years ago; nobody had looked.
- Remote communities like Wujal Wujal and Lockhart River now appear on Bluesky alongside the capital cities — arguably the most meaningful coverage in the whole project.

## The February roadmap — scorecard

| v2.0 said | What happened |
|---|---|
| Improve silent-failure detection | Done, and then some (the failure/empty distinction, probation, dual watchdogs) |
| Performance dashboard | Delivered as a public website instead — lgnews.jonathonmarsden.com |
| More RSS support | Partly — several councils moved to cleaner API-based scraping instead |
| New Zealand expansion | Not yet — still attractive, easier now (no proxy cost scaling) |
| ML content filtering | Not yet — volume bugs fixed first; filtering matters less now |
| Multi-platform posting | Not yet — Bluesky remains bot-friendly |

## What's next

1. **A brand refresh for the eight Bluesky accounts** — consistent names, proper bios, banners matching the website — prepared and being finalised with LG News Roundup, followed by a starter pack and a proper launch push. The feeds have ~126 followers today; the growth plan targets 1,000+ in 90 days.
2. **Growing the readership**: council comms teams, LG professionals, journalists, and the peak bodies — with the VLGA connection through LG News Roundup as the first door to knock on.
3. **Possible products on top**: keyword watchlists and per-council custom feeds for organisations that need them — the free public network is the demonstration.
4. New Zealand, when the time is right.

## How the work gets done now

Worth saying plainly: much of the July overhaul — the review, the fixes, the migration, the repairs — was executed by AI engineering assistants (Anthropic's Claude), working under direction and review, with every change tested and human-approved before going live. That's not a gimmick; it's why a one-person public-interest project can now run at a standard — full audits, verified migrations, 100% coverage — that used to take a team. The same approach is available for other projects: if your organisation needs this kind of site, data service, or automation, talk to me.

## The same questions, updated answers

**Is this sustainable?** More than ever. Costs are ~zero, the code is documented to a standard a stranger could pick up, the system fixes and reports itself for everything routine, and the single-maintainer risk is softened by automation and thorough hand-over documentation.

**Is it legal?** Unchanged: public information, titles and links only, full attribution, traffic driven *to* councils. No complaints to date — councils get free reach out of it.

**What does it cost?** Electricity and a domain name. The February figure of $378/year is now roughly $18.

**Who's it for?** Everyone — that's the point. No paywall, no tracking, no editorial line. Raw council news as it happens, offered as a public good.

---

**Report prepared by:** Jonathon Marsden
**With:** Chris Eddy's LG News Roundup (lgnewsroundup.com) — sponsored by the Victorian Local Governance Association
**Live feeds:** lgnews.jonathonmarsden.com · **Code:** github.com/jonathonmarsden/council-news-bot
**Next review:** October 2026
