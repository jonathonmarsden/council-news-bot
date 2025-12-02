import sys
import os
sys.path.append('/root/council-news-bot')
from core.scraper import CardScraper

def test_scrape():
    selectors = {
        "item_selector": ".blog-post",
        "title_selector": "h4",
        "link_selector": "a.post-top",
        "date_selector": ".full-date",
        "content_selector": ".text-container p"
    }
    
    scraper = CardScraper(
        "central-highlands",
        "Central Highlands Council",
        "https://www.chrc.qld.gov.au/about-council/news/",
        use_curl=True,
        selectors=selectors
    )
    
    articles = scraper.scrape()
    for article in articles:
        if "Gemfields" in article.title:
            print(f"Title: '{article.title}'")
            print(f"Excerpt: '{article.excerpt}'")
            print(f"Date: {article.date}")

if __name__ == "__main__":
    test_scrape()
