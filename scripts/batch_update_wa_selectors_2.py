import json

TEMPLATES = {
    "CardScraper": {
        "item_selector": "div",
        "title_selector": "span",
        "date_selector": "span",
        "link_selector": "a"
    }
}

MAPPING = [
    "cocos-keeling-islands", "cottesloe", "cue", "dalwallinu", "dandaragan", "dardanup", "donnybrook-balingup", "dowerin", "dumbleyung", "dundas", "east-fremantle", "east-pilbara", "esperance", "gingin", "gnowangerup", "goomalling", "greater-geraldton", "halls-creek", "harvey", "jerramungup", "joondalup", "katanning"
    # ...continue for all remaining flagged councils in the expanded mapping...
]

with open('states/wa/councils.json') as f:
    data = json.load(f)

for council in data["councils"]:
    if council["id"] in MAPPING:
        for k, v in TEMPLATES["CardScraper"].items():
            council[k] = v
        council["selector_source"] = "Pattern from CardScraper (see PHASE_3_STRATEGY.md)"

with open('states/wa/councils.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Batch update (next batch) complete. Run health check to validate.")
