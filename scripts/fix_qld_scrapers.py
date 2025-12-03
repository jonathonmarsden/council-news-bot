import json
import os

def fix_qld_scrapers():
    filepath = 'states/qld/councils.json'
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    councils = data.get('councils', [])
    updated_count = 0
    
    ids_to_fix = [
        'aurukun',
        'cook',
        'douglas',
        'napranum',
        'north-burnett',
        'redland',
        'tablelands',
        'toowoomba',
        'yarrabah',
        'doomadgee',
        'kowanyama'
    ]
    
    for council in councils:
        if council['id'] in ids_to_fix:
            if council['scraper'] == 'curl_scraper':
                print(f"Updating {council['id']} scraper from curl_scraper to rss_scraper")
                council['scraper'] = 'rss_scraper'
                updated_count += 1
            
            # Also check if use_curl is true, maybe we should remove it or keep it?
            # rss_scraper doesn't usually use use_curl, but it might not hurt.
            # However, let's leave it for now.
            
    if updated_count > 0:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Updated {updated_count} councils.")
    else:
        print("No councils needed updating.")

if __name__ == "__main__":
    fix_qld_scrapers()
