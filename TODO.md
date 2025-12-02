# Council Bot TODO List

## High Priority (Broken Scrapers)

- [x] **Fix Cairns (QLD)**: Fixed via custom selectors and regex patch.
- [ ] **Fix Charters Towers (QLD)**: 2 articles found, 0 dated.
- [ ] **Fix Logan (QLD)**: 1 article found, 0 dated.
- [x] **Fix Central Coast (NSW)**: Fixed (added selectors).
- [x] **Fix Wollongong (NSW)**: Fixed (added selectors).
- [x] **Fix Northern Beaches (NSW)**: Fixed (updated URL).
- [x] **Fix Canterbury-Bankstown (NSW)**: Fixed (added selectors).

## Medium Priority (WAF / Access Issues)

- [ ] **Solve QLD WAF Blocking (Akamai)**:
  - **Impact**: ~40+ councils blocked (Access Denied), including Logan, Ipswich, Moreton Bay, Noosa, Barcaldine, Blackall-Tambo, etc.
  - **Current Status**: `curl` scraper is detected and blocked.
  - **Potential Solutions**:
    - Residential Proxies.
    - Browser Automation (Playwright/Selenium) to handle JS challenges.
    - Better header impersonation (TLS fingerprinting).

- [ ] **Investigate Lockyer Valley (QLD)**: Confirmed WAF blocked (requires JS/Captcha). Needs browser automation or RSS bypass (RSS also blocked).
- [x] **Fix Hinchinbrook (QLD)**: Fixed selectors. Now finding articles.
- [ ] **Investigate Empty QLD Councils**:
  - Aurukun, Banana, Blackall-Tambo, Brisbane, Bundaberg, Burke, Carpentaria, Cassowary Coast, Cherbourg, Cook, Doomadgee, Douglas, Etheridge, Hope Vale, Ipswich, Mackay, Quilpie, Redland, Richmond, South Burnett, Tablelands, Townsville, Wujal Wujal, Yarrabah.
  - Many of these likely need `curl_scraper` + `mobile_mode` or specific selectors.

## Low Priority (Partial / Minor Issues)

- [x] **Fix Barcoo (QLD)**: Switched to RSS scraper. Now finding articles.
- [x] **Fix Central Highlands (QLD)**: Fixed title/excerpt merging issue.
- [ ] **Fix Partial QLD Scrapers**: Kowanyama, Mareeba, Southern Downs, Sunshine Coast, Toowoomba, Torres Strait Island.
- [ ] **Fix Broken VIC Scrapers**: Buloke, Whitehorse, Brimbank, Manningham.

## Infrastructure

- [x] **Variety Logic**: Implemented round-robin selection in database.py.
- [ ] **Deduplication**: Consider adding title+date deduplication to handle URL changes.
- [ ] **Monitoring**: Set up automated weekly health checks.

## New Broken Scrapers (Dec 2025)

### VIC
- [ ] Buloke, Whitehorse, Wodonga, Brimbank, Manningham, Mitchell, Moonee Valley, Hindmarsh, Whittlesea.

### NSW
- [ ] Bayside, Blue Mountains, Camden, Campbelltown, Canada Bay, Cessnock, Coffs Harbour, Hornsby, Ku-ring-gai, Maitland, Mosman, Ryde, Shoalhaven, Strathfield, Willoughby, Woollahra.
- [ ] Orange, Snowy Monaro, Balranald, Blayney, Bourke, Byron, Cowra, Edward River, Forbes, Gilgandra, Greater Hume, Griffith, Wentworth, Wingecarribee.

### QLD
- [ ] Barcoo, Charters Towers, Logan, Moreton Bay, Mornington, Napranum, North Burnett, Pormpuraaw, Sunshine Coast, Torres Strait Island, Kowanyama.

