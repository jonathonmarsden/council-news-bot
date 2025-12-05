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
    "kojonup", "kulin", "kwinana", "lake-grace", "laverton", "leonora", "mandurah", "manjimup", "melville", "merredin", "moora", "morawa", "mount-magnet", "nannup", "narembeen", "narrogin", "ngaanyatjarraku", "northam", "northampton", "nungarin", "perenjori", "pingelly", "plantagenet", "port-hedland", "quairading", "ravensthorpe", "rockingham", "sandstone", "serpentine-jarrahdale", "shark-bay", "south-perth", "subiaco", "swan", "tammin", "toodyay", "upper-gascoyne", "victoria-plains", "wagin", "wandering", "waroona", "west-arthur", "wickepin", "williams", "wiluna", "wongan-ballidu", "woodanilling", "wyndham-east-kimberley", "york"
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

print("Batch update (final batch) complete. Run health check to validate.")
