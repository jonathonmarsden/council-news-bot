from core.scraper import CardScraper
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_council(council_id, name, url):
    print(f"\nTesting scraper for {name}...")
    scraper = CardScraper(
        council_id, 
        name, 
        url, 
        use_curl=True
    )

    articles = scraper.scrape()
    print(f"Found {len(articles)} articles.")
    
    for i, article in enumerate(articles[:5]):
        print(f"\nArticle {i+1}:")
        print(f"Title: '{article.title}'")
        print(f"Date: {article.date}")
        print(f"URL: {article.url}")

if __name__ == "__main__":
    test_council(
        "warren-shire-council",
        "Warren Shire Council",
        "https://www.warren.nsw.gov.au/council/media-releases"
    )
    test_council(
        "narromine-shire-council",
        "Narromine Shire Council",
        "https://www.narromine.nsw.gov.au/council/media-releases"
    )
