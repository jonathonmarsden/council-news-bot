import json
import os

def fix_qld_scrapers_batch3():
    filepath = 'states/qld/councils.json'
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    councils = data.get('councils', [])
    updated_count = 0
    
    for council in councils:
        cid = council['id']
        
        if cid == 'cherbourg-aboriginal-shire':
            print(f"Reverting {cid} URL and scraper")
            council['news_url'] = 'https://cherbourg.qld.gov.au/news-events/'
            council['scraper'] = 'curl_scraper'
            updated_count += 1
            
    if updated_count > 0:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Updated {updated_count} councils.")
    else:
        print("No councils needed updating.")

if __name__ == "__main__":
    fix_qld_scrapers_batch3()
