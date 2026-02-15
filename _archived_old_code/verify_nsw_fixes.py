import json
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from core.scrapers.factory import ScraperFactory

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

TARGET_IDS = [
    "bogan-shire-council",
    "lake-macquarie-city-council",
    "snowy-valleys-council",
    "wollondilly-shire-council",
    "lithgow-city-council",
    "lockhart-shire-council",
    "murray-river-council",
    "murrumbidgee-council",
    "narrandera-shire-council",
    "shellharbour-city-council",
    "upper-lachlan-shire-council"
]

def verify_fixes():
    config_path = Path("states/nsw/councils.json")
    with open(config_path, "r") as f:
        data = json.load(f)
    
    councils = {c["id"]: c for c in data["councils"]}
    
    print(f"--- Verifying Fixes for {len(TARGET_IDS)} Councils ---")
    
    for council_id in TARGET_IDS:
        if council_id not in councils:
            print(f"❌ {council_id}: Not found in config!")
            continue
            
        config = councils[council_id]
        print(f"\nTesting {config['name']} ({council_id})...")
        print(f"  URL: {config.get('news_url')}")
        print(f"  Scraper: {config.get('scraper')}")
        
        try:
            scraper = ScraperFactory.create_scraper(config)
            articles = scraper.scrape()
            count = len(articles)
            
            if count > 0:
                print(f"  ✅ SUCCESS: Found {count} articles.")
                print(f"     Latest: {articles[0].title}")
            else:
                print(f"  ⚠️ FAILURE: Found 0 articles.")
                # Optional: print debug info if scraper supports it
                
        except Exception as e:
            print(f"  ❌ ERROR: {e}")

if __name__ == "__main__":
    verify_fixes()
