import json
import os

def fix_qld_scrapers_batch2():
    filepath = 'states/qld/councils.json'
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    councils = data.get('councils', [])
    updated_count = 0
    
    for council in councils:
        cid = council['id']
        
        if cid == 'south-burnett':
            print(f"Updating {cid} URL")
            council['news_url'] = 'https://www.southburnett.qld.gov.au/News-Articles'
            updated_count += 1
            
        elif cid == 'hope-vale':
            print(f"Updating {cid} URL")
            council['news_url'] = 'https://www.hopevale.qld.gov.au/Council/News-and-Notices/Latest-News'
            updated_count += 1
            
        elif cid == 'burke':
            print(f"Updating {cid} URL")
            council['news_url'] = 'https://www.burke.qld.gov.au/News'
            updated_count += 1
            
        elif cid == 'cherbourg-aboriginal-shire':
            print(f"Updating {cid} URL and scraper")
            council['news_url'] = 'https://cherbourg.qld.gov.au/feed/'
            council['scraper'] = 'rss_scraper'
            updated_count += 1
            
    if updated_count > 0:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Updated {updated_count} councils.")
    else:
        print("No councils needed updating.")

if __name__ == "__main__":
    fix_qld_scrapers_batch2()
