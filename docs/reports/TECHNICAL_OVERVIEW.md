# Australian Council News on Bluesky
## A technical overview of the LG News Roundup aggregation service

**Version 1.0 — July 2026 · Prepared by Jonathon Marsden**
**Live service:** lgnews.jonathonmarsden.com · **Crawler reference:** lgnews.jonathonmarsden.com/bot.html

---

### 1. Purpose

Most Australians never see news from their local council unless they go looking for it. Road closures, grant rounds, meeting notices, and community programs are published on 500+ separate council websites that few residents visit. This service closes that gap: it collects the headlines every Australian council publishes and republishes them — as links back to the council's own website — on free, public, state-by-state Bluesky feeds.

The service is operated as a public good. There is no paywall, no advertising, no tracking, no editorial curation, and no commercial use of the data. Every post drives readers to the council's own site. It is the companion data service to LG News Roundup, Chris Eddy's daily local government podcast, sponsored by the Victorian Local Governance Association.

**Coverage today: 534 of Australia's 537 local government areas, republishing 100–250 stories per weekday.**

### 2. What the service does — and deliberately does not do

| Does | Does not |
|---|---|
| Reads each council's public news listing once daily | Never accesses anything behind a login, form, or paywall |
| Collects headline, link, publication date, one-line excerpt | Never collects personal information of any kind |
| Posts headline + attributed link to a public Bluesky feed | Never republishes article bodies or images |
| Sends readers to the council's own website | Never crawls beyond the news section |
| Withdraws from any council on request, within a day | Never sells, syndicates, or monetises the data |

### 3. Architecture

The system is a single pipeline with four stages, deliberately simple:

1. **Scheduler** — each council is fetched once per day at a fixed off-peak time, with councils spread evenly across 24 hours so no shared platform ever sees a burst.
2. **Collectors** — per-council fetch logic (HTML, RSS, or public JSON endpoints, whichever the council offers) extracts headline, link, and date. A council's collector that fails does so loudly and independently; it cannot affect any other council.
3. **Store** — PostgreSQL holds every article seen, keyed by URL. This is what guarantees each story is posted exactly once, ever.
4. **Publisher** — a paced queue posts to the eight state Bluesky accounts at a fixed, conservative rate (at most 18 posts per hour per account), far below platform limits.

Everything runs in isolated containers on dedicated hardware in Australia, on a residential connection — relevant because the traffic profile is indistinguishable in scale from one interested resident checking the news page daily.

### 4. Crawling practices — the numbers

Per council, per day: one news-listing request, plus up to ten article-page requests only when the listing omits publication dates. Failed fetches retry at most twice with exponential backoff, then stand down until the next day. A council that fails repeatedly is automatically rested and re-checked every third day. Total load: typically 1–11 requests and well under one megabyte per council per day.

Councils that allow the crawler explicitly see an honest, verifiable User-Agent:

    LGNewsRoundupBot/1.0 (+https://lgnews.jonathonmarsden.com/bot.html)

That URL is a permanent reference page stating exactly what the crawler does, how to allow it, how to decline, and who to contact. Any council can opt out by email — removal within a day, no questions asked — or simply by blocking, which the system detects and respects by standing down automatically.

### 5. Security posture

Written for technical readers; every claim is verifiable in the source code.

- **Attack surface**: the system has no inbound network exposure at all — no listening ports, no web endpoints, no user input, no accounts, no stored personal data. It makes outbound requests to council websites and to Bluesky, and nothing else. The public website is a static page served through a CDN, with a locked-down Content-Security-Policy, HSTS, and no backend.
- **Data minimisation**: the entire data model is headline, URL, date, excerpt, and posting state. There is nothing in the system worth stealing.
- **Secrets**: publishing credentials are scoped app-passwords (revocable independently of the accounts), held only in a permission-restricted environment file on the host — never in code or version control, verified by automated checks.
- **Supply chain**: pinned dependency versions, automated dependency alerts, and a CI pipeline that tests every change on three Python versions before it can reach production.
- **Integrity**: posting uses an atomic claim protocol — each article is posted exactly once even if processes crash mid-operation or run concurrently.
- **Monitoring that assumes failure**: the design principle is "fail loudly." Every failure mode discovered in three years of operation now raises an alert: per-council failures, silent-empty results, missed schedules, stalled publishing, and monitor crashes themselves. A second, fully independent watchdog checks the public feeds every six hours from external infrastructure, so even total loss of the host is detected within hours.
- **Recovery**: daily database dumps with integrity checks, nightly whole-system snapshots with multi-week retention, and a written, tested restore procedure.

### 6. Reliability and governance

The service has operated continuously since 2025 and today runs at 100% collector coverage. Engineering is done in the open: the codebase is version-controlled with full history, every change is tested in CI, deployment is automated and reversible, and a substantial 2026 overhaul was conducted with AI engineering assistance under human direction and review — with the review findings and fixes documented in the repository.

It is built and operated by Jonathon Marsden — software developer, former Mayor, and postgraduate cyber security student — with editorial partnership from LG News Roundup. Being a former Mayor is not incidental: the operator understands council obligations, and the service is designed to make councils look good, not to burden them.

### 7. Verification checklist for IT departments

Claims are cheap; here is how to check ours.

1. **Identity**: fetch lgnews.jonathonmarsden.com/bot.html — the crawler's reference page, on the same domain as the public service.
2. **Traffic**: after allowing the User-Agent above, watch your logs — one visit per day to your news pages, from an Australian residential address.
3. **Behaviour**: the fetch logic is inspectable in the source repository; the code that runs is the code you can read.
4. **Output**: find your council on your state's feed via lgnews.jonathonmarsden.com — every post is your headline, your link, your traffic.
5. **Control**: email the contact below and watch your council disappear from the crawl within a day. That is the whole power dynamic: you hold the switch.

### 8. Contact

Jonathon Marsden · hello@jonathonmarsden.com
Service: lgnews.jonathonmarsden.com · Crawler reference: lgnews.jonathonmarsden.com/bot.html
Editorial partner: LG News Roundup (lgnewsroundup.com), sponsored by the Victorian Local Governance Association
