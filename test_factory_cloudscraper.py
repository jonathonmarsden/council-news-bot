
import json
import os
import sys
from core.scrapers.factory import ScraperFactory

def test_factory():
    # Load the config
    with open('states/sa/councils.json', 'r') as f:
        config = json.load(f)
    
    # Find Northern Areas
    council_config = next(c for c in config['councils'] if c['id'] == 'northern-areas')
    
    print(f"Testing config for: {council_config['name']}")
    print(f"use_cloudscraper in config: {council_config.get('use_cloudscraper')}")
    
    # Create scraper
    scraper = ScraperFactory.create_scraper(council_config)
    
    print(f"Scraper class: {type(scraper).__name__}")
    print(f"Scraper use_cloudscraper: {scraper.use_cloudscraper}")
    
    if not scraper.use_cloudscraper:
        print("ERROR: Scraper instance does not have use_cloudscraper=True")
        return
        
    print("Scraper instance correctly configured. Attempting fetch...")
    
    # Try to fetch
    # Manually fetch to inspect content
    content = scraper.fetch_page(scraper.news_url)
    if content:
        with open('debug_northern_areas_factory.html', 'w') as f:
            f.write(content)
        print("Saved HTML to debug_northern_areas_factory.html")
    
    articles = scraper.scrape()
    print(f"Found {len(articles)} articles")
    if len(articles) > 0:
        print("First article:", articles[0].title)
        print("SUCCESS")
    else:
        print("FAILURE: No articles found")

if __name__ == "__main__":
    test_factory()
