# LG News Roundup Interview - Council News Bot Snippets

## The "Elevator Pitch" & Purpose
1.  **The "News Desert" Firehose:** "Local newspapers are closing, but council newsrooms are busier than ever. We built a machine that drinks from the firehose of 537 different council websites so you don't have to check them one by one."
2.  **Automating Democracy:** "Democracy dies in the dark, but it also dies behind bad user interfaces. This project is about dragging critical civic information out of obscure PDFs and nested menus and putting it right in front of the people."
3.  **The Great Leveller:** "Whether it’s the City of Brisbane with a massive media team or the Shire of Peppermint Grove with a single webpage, this bot treats them exactly the same. Every story gets the same platform."
4.  **Centralising the Decentralised:** "Australia has 537 separate local governments. That is 537 separate silos of information. This project is the first real attempt to federate that data into a single, query-able stream without asking the councils to do any extra work."

## The "Council as Publisher" Shift
5.  **The Empty Press Bench:** "In hundreds of council chambers across Australia, the press bench is physically empty. The local paper didn't send a reporter because they don't have one. The *only* record of what happened is now produced by the Council itself. We are aggregating the only surviving record."
6.  **Filling the Vacuum:** "Nature abhors a vacuum, and so does news. As commercial news outlets retreated to the cities, Councils didn't just step up; they were forced to become the primary distributors of local information."
7.  **The "Unfiltered" Era:** "For 100 years, local news was filtered through an editor's lens. Today, that filter is gone. Councils are speaking directly to ratepayers. It’s raw, it’s immediate, and it requires a tool like ours to manage the sheer volume of it."
8.  **From "Spin" to "Service":** "We've seen a shift in tone. Ten years ago, council news was 'Mayor cuts ribbon'. Today? It's 'Here is how to prepare for the bushfire season' or 'Why your rates paid for this drainage'. It’s moved from vanity PR to utility journalism."
9.  **The Hiring Spree:** "Ideally, we’d have independent papers. But in reality, the best journalists in town are often hired by the Council because they are the only ones offering stable media jobs. The quality of council writing has skyrocketed because ex-journos are writing it."
10. **The "Good News" Engine:** "Commercial news thrives on conflict—'Council Fails Again'. Councils are naturally publishing the counter-narrative—'Here is what we achieved'. Our bot captures the wins that a click-bait driven media model often ignores."

## The "News Desert" Reality
11. **The Regional Lifeline:** "In some remote Shires, the Council website isn't just a government portal; it is the *community noticeboard*. If the Council doesn't post about the road closure or the microchipping day, nobody knows. Our bot turns those static notices into an active news feed."
12. **The "Hyper-Local" Definition:** "State media cares about the highway; National media cares about the economy. Only the Council (and this bot) cares about the playground upgrade in *your* specific street. We are aggregating the hyper-local."
13. **Information Inequality:** "We've noticed a digital divide. Wealthy metro councils have newsrooms rivaling the ABC. Remote councils struggle to upload a PDF. This project highlights that disparity—we shine a light on the quiet councils too."
14. **The "Zombie" Newspaper:** "Many towns have a 'newspaper' that is just syndicated national news with a local masthead. The real local content—the DA approvals, the park openings—is actually living on the council domain, not the newspaper site."

## The Tech Stack & "Digital Archaeology"
15. **Under the Hood:** "It’s a Python-based beast running on a DigitalOcean virtual server, using Docker containers to keep it clean. It’s open-source engineering solving a civic problem."
16. **Digital Archaeology:** "Writing scrapers for Australian councils is like digital archaeology. We’re digging through 2024 Next.js React apps, but also 2005 ASP.NET sites and handcrafted HTML. The bot has to speak 500 different dialects of 'web'."
17. **The "Whac-A-Mole" War:** "Our biggest challenge? Cyber security. We constantly battle 'False Positive' blocks where a council firewall thinks our friendly newsletter bot is a Russian hacker. We use rotating proxies to politely knock on the door."
18. **The "Polite" Spider:** "We built the bot to be respectful. We aren't hammering council servers. We use 'conditional requests'—asking the server 'Has anything changed since 9am?' If the answer is no, we walk away. We are lightweight visitors."
19. **Selectors & Structures:** "Building this taught us that there is no 'Standard Australian Council Website'. Some use OpenCities, some use WordPress, some use proprietary systems from the 90s. We had to build a 'Strategy Pattern' scraper that adapts to the DNA of each specific site."
20. **Fail-Loud Architecture:** "When a Council updates their website, they break our scraper. In the old days, we wouldn't know. Now, the system sends an alert to Discord saying 'The pattern for City of Ryde just changed'. It turns maintenance into a game of whack-a-mole we can win."
21. **The "Headless" Future:** "We are seeing councils move to 'Headless CMS' systems—fancy React frontends. This makes scraping harder. We've had to evolve from simple HTML readers to using 'Headless Browsers' that actually render the JavaScript, just like a human eye would."
22. **Docker Containerisation:** "The whole system is containerised. I can spin up the entire 'Australian Local Government News Ecosystem' on a laptop, a server, or a cloud instance in minutes. It’s portable civic infrastructure."

## For The Readership (User Cases)
23. **For the General Managers & Mayors:** "This is the ultimate benchmarking tool. Want to know how 10 other councils are handling their Australia Day awards or waste management comms? It’s all in the feed."
24. **For Journalists:** "This is a lead-generation machine. Instead of waiting for a press release, a journalist can watch the feed and spot a trend—like five different councils launching 'Cat Curfews' in the same week."
25. **For the "Citizen Journalist":** "You don't need a press pass to hold power to account. With this bot, a local resident can be the first to know about a planning amendment or a budget meeting, often before the local paper prints it."
26. **For Researchers & Academics:** "We are building a massive, searchable dataset of Australian Local Government priorities. If you want to track the rise of 'Artificial Intelligence' policies in local govt over 3 years, the data is sitting right there."
27. **For State/Federal Admins:** "It’s a pulse check. If you sit in a state department, this feed gives you the ground truth of what is actually happening in the regions, unfiltered by middle management reports."
28. **The Grant Finder:** "Imagine you are a Federal policymaker. You can filter our feed for the word 'Grant'. Suddenly, you see exactly where federal money is landing on the ground across the entire nation in real-time. The feedback loop is instant."

## The BlueSky Advantage
29. **Why BlueSky?** "BlueSky is the new public square. Unlike X (Twitter) or Facebook, there’s no algorithm burying a 'boring' council announcement. If the council posted it, you see it. It’s chronological transparency."
30. **The "Custom Feed" Revolution:** "Because BlueSky is open, we can build custom feeds. Imagine a 'NSW Planning Feed' or a 'VIC Arts & Culture Feed' that pulls from hundreds of sources instantly. That’s the power of open protocol."
31. **The "State" Roundups:** "We’ve split the bots by state—`@roundupnewsbotvic.bsky.social`, `@roundupnewsbotnsw.bsky.social`, etc. It means you can follow your jurisdiction without getting noise from across the country."
32. **Crisis Communication:** "During floods or fires, Council websites are the source of truth. By aggregating them to BlueSky, we create a resilient, real-time emergency ticker that doesn't rely on Facebook's algorithm showing you the post 3 days late."

## Philosophy & Future
33. **Open Source/Open Data:** "The code is on GitHub. Anyone can look at it, improve it, or audit it. If a council changes their site, a local dev can submit a fix. It’s a community asset, not a proprietary black box."
34. **The "Unsung Story" Engine:** "We find the stories that don't go viral. The library upgrades, the road resurfacing, the community grant winners. These are the fabric of community life, and the bot ensures they have a permanent digital record."
35. **Future Tech - AI Summaries:** "Phase two? We want to plug in Large Language Models (LLMs) to not just link to the article, but summarize the 50-page agenda attachment that came with it. 'TL;DR for Council Meetings.'"
36. **Trend Spotting:** "We’re noticing language shifts. You can literally see buzzwords travel from metro councils to regional ones over the course of a month just by watching the headlines flow in."
37. **The Civic Memory:** "Websites change. Old news gets deleted. By scraping and storing this, we are creating an archive. In 2030, we will be able to look back at 2026 and see exactly what the priorities of Local Government were."
38. **Democratising Data:** "We’re stripping the friction out of staying informed. You shouldn't have to navigate a complex government menu to learn about your town. The news should come to you. That is the service we provide."
39. **The Call to Action:** "This is about respect for local government content. Councils are becoming publishers. We are just building the distribution network they deserve."
