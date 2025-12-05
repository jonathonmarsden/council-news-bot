import json

with open('states/nt/councils.json', 'r') as f:
    data = json.load(f)

for council in data['councils']:
    council['enabled'] = True

with open('states/nt/councils.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Updated states/nt/councils.json with enabled=True")
