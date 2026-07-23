# Bluesky Brand & Growth Plan — LG News Roundup feeds

*Drafted 2026-07-19. Applies to the 8 state feed accounts. The accounts are owned
by Chris Eddy — everything here needs his sign-off before it's applied. Once
approved, all profile changes can be applied in minutes via the ATProto API
using the existing app passwords.*

---

## 1. Where we are

| Account | Display name today | Bio | Banner | Followers |
|---|---|---|---|---|
| VIC | "LG News Roundup Victoria Newsfeed" | one line | none | 24 |
| NSW | "LG News Roundup NSW Newsfeed" | one line | none | 31 |
| QLD | "LG News Roundup Queensland Newsfeed" | **empty** | none | 11 |
| SA | "LG News Roundup SA feed" | **empty** | none | 4 |
| WA | "LG News Roundup WA feed" | **empty** | none | 39 |
| TAS | "LG News Roundup TAS feed" | **empty** | none | 8 |
| NT | "LG News Roundup NT feed" | **empty** | none | 5 |
| ACT | "LG News Roundup ACT Newsfeed" | one line | none | 4 |

126 followers total, for the only complete real-time source of Australian
council news in existence. The product is finished; the shopfront is bare.

## 2. Brand foundation (from lgnews.jonathonmarsden.com)

- **Philosophy (use these words — they're already written):** "No editorial
  curation, no paywalls, and no tracking — just raw council news as it happens,
  offered as a public good in the spirit of open access to information that
  affects people's lives."
- **Origin story:** Chris Eddy (LG News Roundup — daily podcast + newsletter,
  sponsored by the Victorian Local Governance Association) asked; Jonathon
  Marsden — developer and former Mayor — built it.
- **Visual identity:** warm paper `#f7f4ef`, ink `#141414`, orange accent
  `#df842b`, deep teal `#28404d`; Georgia/serif display type over system sans.
  Dark-mode variants exist in the site CSS.
- **Numbers that impress:** 537 councils · 8 states/territories · every story,
  as it happens.

## 3. The profile system (per-account spec)

### Display names (consistent pattern, search-friendly)
People search "council news [state]" — lead with that, keep the LGNR brand:

> **`{State} Council News — LG News Roundup`**

e.g. "Victoria Council News — LG News Roundup", "NSW Council News — LG News
Roundup". (ACT: "Canberra & ACT News — LG News Roundup".)

### Bios (≤256 chars; identical skeleton, per-state numbers)
Four jobs in four lines: what it is, honesty about automation, the family it
belongs to, who built it (with the door open for work):

> 🤖 Every media release from all {N} {State} councils, as it happens.
> Automated, uncurated, free — news as a public good.
> Companion to LG News Roundup, Chris Eddy's daily podcast, sponsored by the Victorian Local Governance Association.
> Built & run by Jonathon Marsden 🔧 lgnews.jonathonmarsden.com/{state}

(VIC fills to ~240 chars. The 🤖 up front is Bluesky best practice for
automated accounts — transparency reads as competence, not weakness.)

### Banners (currently none — the biggest visual win)
1500×500. One template, eight renders: paper background, orange rule, Georgia
serif headline **"Every council. Every story."**, state name + council count in
teal, small "part of LG News Roundup · lgnews.jonathonmarsden.com" footer.
Optional: state silhouette in low-contrast teal. I can generate all eight as
SVG→PNG programmatically (same palette variables as the site) for approval.

### Avatars
Keep whatever LGNR equity exists, but unify: same mark, state abbreviation
badge in the corner (orange on teal). 1000×1000.

### Pinned post (one per account, ≤300 chars)
> Every media release from all {N} {State} councils — automated, free, and
> uncurated, straight from the source.
>
> One page for all 8 states: lgnews.jonathonmarsden.com
> The human context: Chris Eddy's LG News Roundup podcast — lgnewsroundup.com

### Cross-link architecture
- **Bios** → site state page (`/vic` etc. — these clean URLs already work).
- **Site** already links each account (verified in index.html).
- **Pinned posts** → hub site + podcast site.
- **Each account follows the other seven** (and the podcast's account, if
  Chris has one on Bluesky — worth creating if not: the podcast is the human
  voice this network is the data layer for).
- **Starter pack** (see §5) becomes the ninth link everyone shares.

## 4. Optional upgrade: custom-domain handles

Bluesky handles can be domain-verified. `@vic.lgnews.jonathonmarsden.com`
turns every handle into proof of ownership and a billboard for the site.
Followers and post history carry over (the DID is stable); only the name
changes. Cost: one DNS TXT record per state (`_atproto.vic.lgnews...`), and
three code touch-points that hardcode `roundupnewsbot*`:
`.env` handle vars (used for login — must match after change),
`scripts/monitoring/feed_watchdog.py` HANDLES map, and the site's
`index.html` feeds map. All trivial; the poster itself is already immune
(state is passed explicitly since the July fixes).

**Recommendation:** do it, but as a second step a few weeks after the profile
refresh — one brand change at a time, and it deserves its own announcement
post ("we moved to our own domain" is itself content). Decision belongs to
Chris (his accounts) + Jonathon (his domain).

## 5. Growth plan

### Positioning (the one-sentence versions)
- The network: **"Every Australian council's news, live on Bluesky — the data
  layer under LG News Roundup."**
- The builder: **"Built and maintained by Jonathon Marsden — developer, former
  Mayor, and civic-tech practitioner. I build open-data sites and services for
  the local government sector: get in touch."**
  ("Civic tech" / "govtech" is the recognised term — "local government
  technology" also reads fine and is more searchable in Australia.)

### Audiences, in order of value
1. **Council comms teams & CEOs** — their own councils are being amplified for
   free. Easiest follows on the platform.
2. **LG professionals** — planners, engineers, governance officers; LG
   Professionals associations, IPWEA.
3. **Councillors & mayors** (~5,000 nationally) — many are on Bluesky
   post-migration; a feed of their state's peers is professionally useful.
4. **Journalists** — state political reporters and regional mastheads; a
   real-time wire of every council's announcements is a working tool.
5. **Peak bodies** — VLGA first (existing relationship), then LGNSW, LGAQ,
   WALGA, LGASA, LGAT, LGANT, ALGA.
6. **The Bluesky civic/data community** — #auspol, #springst (VIC politics),
   open-data and civic-tech folk who repost infrastructure-as-public-good
   projects enthusiastically.

### Tactics (in rough order)
1. **Profile refresh first** (this doc §3) — nothing else works while five
   bios are empty. One evening's work after sign-off.
2. **A Starter Pack**: "Australian Local Government News — all 8 states", the
   8 accounts + LGNR's account. Starter packs are Bluesky's native growth
   machine — one click follows everything, and packs get shared. Created from
   Chris's or Jonathon's personal account.
3. **Launch thread** from Chris's podcast account + Jonathon's personal
   account, cross-reposted: the origin story ("Chris said 'you know what I
   really need…'"), the numbers (537 councils), the philosophy (public good),
   the invitation (follow your state; here's the starter pack). The podcast
   plug: Chris mentions the feeds on-air; the feeds' pinned posts return the
   favour permanently.
4. **VLGA amplification**: VLGA supports the podcast already — ask for one
   repost/newsletter mention. Their members ARE audience #1 and #3.
5. **Tag councils into their own coverage — carefully.** A monthly "most
   active councils this month" post per state (from Chris's or Jonathon's
   human account, not the bots) naming and tagging 3–5 councils. Councils
   repost praise; their followers discover the feed. Never spam-tag from the
   bot accounts themselves.
6. **Journalist outreach**: a dozen DMs/emails to state-round reporters:
   "every council media release in your state, one follow, free, no strings."
   One newsroom adoption is worth 500 passive followers.
7. **Monthly network post** ("June: 2,847 stories from 519 councils")
   — the transparency numbers double as content. Can be generated
   automatically from the DB (the daily-briefing machinery already computes
   most of it).
8. **Jonathon's shingle**: an /about or /services section on the site ("I
   build things like this — sites, data services, automation for the
   public-interest and local-government sector"), linked from every bio's
   "Built & run by" line. Plain English, one page, a contact address. The
   feeds then market the consultancy passively forever.
9. **Later, the product ladder** (per docs/monetisation-watchlists.md in the
   site repo): keyword watchlists and per-council custom feeds for peak
   bodies and comms teams — the free network is the demo; the paid layer is
   the natural upsell Chris and Jonathon can decide on together.

### Measurement
- Weekly follower counts per account (one API call each — could be appended
  to the existing daily briefing automatically).
- Starter-pack installs, pinned-post reposts, site referrer traffic
  (Cloudflare analytics already exists).
- Target: 126 → 1,000 total followers in 90 days is realistic with sign-off
  on tactics 1–5; a single newsroom or peak-body repost can beat that.

### 30 / 60 / 90
- **30**: profile refresh live; starter pack live; launch thread; VLGA ask.
- **60**: journalist outreach done; first monthly network post; services page
  live; council-tagging cadence started.
- **90**: custom-domain handles (if approved); assess follower curve; decide
  on watchlist/custom-feed pilot with one peak body.

## 6. Execution & approvals

| Step | Who decides | Who does it |
|---|---|---|
| Profile copy (names/bios/pins, §3) | **Chris** (his accounts) with Jonathon | Claude, via ATProto script, minutes |
| Banner/avatar images | Chris + Jonathon taste check | Claude generates for approval |
| Starter pack + launch thread | Chris + Jonathon | Human accounts (packs can't be made by the bots) |
| Custom-domain handles (§4) | Chris + Jonathon | Claude (DNS + API + 3 code touchpoints) |
| Services page on site | Jonathon | Claude drafts |
| Follower metrics in daily briefing | Jonathon | Claude, small PR |

*The one hard rule: nothing in §3 gets applied until Chris says yes — they're
his accounts, and the refresh is also simply better if he's excited about it.*
