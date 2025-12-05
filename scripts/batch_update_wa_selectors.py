import json

# Example selector templates
TEMPLATES = {
    "OpenCities": {
        "item_selector": "article",
        "title_selector": "h2",
        "date_selector": ".date",
        "link_selector": "a"
    },
    "ASP.NET": {
        "item_selector": "div.news-item",
        "title_selector": "h2.title",
        "date_selector": "span.date",
        "link_selector": "a"
    },
    "CardScraper": {
        "item_selector": "div",
        "title_selector": "span",
        "date_selector": "span",
        "link_selector": "a"
    },
    "RSS": {}
}

# Example mapping (should be filled out for all flagged councils)
MAPPING = {
    "beverley": "OpenCities",
    "bruce-rock": "ASP.NET",
    "canning": "OpenCities",
    "capel": "CardScraper",
    "carnamah": "RSS",
    "carnarvon": "CardScraper",
    "chapman-valley": "CardScraper",
    "chittering": "CardScraper",
    "claremont": "OpenCities",
    "coolgardie": "CardScraper",
    "cuballing": "CardScraper",
    # ... continue for all flagged councils ...
}

with open('states/wa/councils.json') as f:
    data = json.load(f)

for council in data["councils"]:
    cid = council["id"]
    if cid in MAPPING:
        cms = MAPPING[cid]
        template = TEMPLATES.get(cms, {})
        for k, v in template.items():
            council[k] = v
        council["selector_source"] = f"Pattern from {cms} (see PHASE_3_STRATEGY.md)"

with open('states/wa/councils.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Batch update complete. Run health check to validate.")
