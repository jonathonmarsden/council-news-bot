import json

config_path = 'config/councils.json'

with open(config_path, 'r') as f:
    data = json.load(f)

enabled_count = 0
for council in data['councils']:
    if council.get('scraper') == 'curl_scraper' and council.get('enabled') == False:
        # Skip Hepburn and Yarriambiack for now as their URLs look weird
        if council['id'] in ['hepburn', 'yarriambiack']:
            continue
            
        council['enabled'] = True
        enabled_count += 1
        print(f"Enabling {council['name']}")

with open(config_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"\nEnabled {enabled_count} councils.")
