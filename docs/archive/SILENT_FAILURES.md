# Silent Failures (Zombie Scrapers) Report

The following 61 councils are marked as "Active" but have returned **0 articles** in their last 5 scrape runs (past 3 days). This indicates a "silent failure" where the scraper runs without error but fails to extract content (likely due to selector changes or layout updates).

## List of Zombies
- adelaide
- adelaide-hills
- barossa
- bass-coast
- blackall-tambo
- boddington
- bogan-shire-council
- boroondara
- bundaberg
- cherbourg-aboriginal-shire
- cottesloe
- dandaragan
- dardanup
- dumbleyung
- east-fremantle
- east-gippsland
- east_arnhem
- etheridge
- goomalling
- halls-creek
- harvey
- holdfast-bay
- kojonup
- lockhart-river
- lockyer-valley
- mandurah
- manjimup
- marion
- meekatharra
- merredin
- moora
- moree-plains-shire-council
- mount-gambier
- mount-magnet
- nannup
- naracoorte-lucindale
- narembeen
- northam
- northern-areas
- nungarin
- orroroo-carrieton
- peterborough
- port-augusta-city
- quairading
- quilpie
- renmark-paringa
- richmond
- salisbury
- sandstone
- subiaco
- tammin
- tasman
- towong
- trayning
- unley
- vincent
- wagait
- warrnambool
- wellington
- west-torrens
- wujal-wujal

## Status
- **Assessed**: 61
- **Pilot Fixes**: 3 (Adelaide, Bogan, Bundaberg) - All Successful
- **Remaining**: 58

## Next Steps
1.  **Pilot Success**: The fixes for the first 3 were 100% effective.
    - Adelaide: 0 -> 200 articles (Fixed by switching to `browser_scraper`)
    - Bogan: 0 -> 10 articles (Fixed by correcting `news_url` to RSS feed)
    - Bundaberg: 0 -> 10 articles (Fixed by correcting `news_url` to RSS feed)
2.  **Rollout**: Apply similar fixes to the remaining 58 councils.
    - Check if they are RSS scrapers with wrong URLs.
    - Check if they are Cloudflare blocked (switch to Browser).
3.  **Monitor**: `scheduler.py` has been updated to log "Found X 'Zombie' scrapers" outputs, so this list will be visible in logs moving forward.
