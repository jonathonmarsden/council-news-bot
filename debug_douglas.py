from core.scrapers import RSSScraper
import json

council = {
    "id": "douglas",
    "name": "Douglas Council",
    "news_url": "https://douglas.qld.gov.au/feed/",
    "scraper": "rss_scraper",
    "enabled": True
}

scraper = RSSScraper(
    council_id=council['id'],
    council_name=council['name'],
    news_url=council['news_url']
)

articles = scraper.scrape()
print(f"Found {len(articles)} articles")
for article in articles:
    print(f"Title: '{article.title}'")
    print(f"Date: {article.date}")
    print(f"URL: {article.url}")
    print(f"Excerpt: {article.excerpt}")
    print("-" * 20)
