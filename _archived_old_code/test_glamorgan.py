from core.scrapers.rss import RSSScraper
import logging

logging.basicConfig(level=logging.DEBUG)

def test_glamorgan():
    scraper = RSSScraper(
        council_id="glamorgan-spring-bay",
        council_name="Glamorgan-Spring Bay Council",
        news_url="https://gsbc.tas.gov.au/feed/"
    )
    articles = scraper.scrape()
    print(f"Found {len(articles)} articles.")
    for a in articles:
        print(f"- {a.title} ({a.date})")

if __name__ == "__main__":
    test_glamorgan()
