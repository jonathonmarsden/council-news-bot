
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scrapers import InnerWestScraper

def test_inner_west():
    scraper = InnerWestScraper(
        council_id='inner-west-council',
        council_name='Inner West Council',
        news_url='https://www.innerwest.nsw.gov.au/about/news/media-releases',
        use_curl=False,
        selectors={'item_selector': 'article.block', 'title_selector': 'h2'}
    )
    
    print("Scraping Inner West Council...")
    articles = scraper.scrape()
    
    print(f"Found {len(articles)} articles")
    for article in articles[:5]:
        print(f"- {article.title}")
        print(f"  Date: {article.date}")
        print(f"  URL: {article.url}")
        print("")

if __name__ == "__main__":
    test_inner_west()
