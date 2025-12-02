from curl_cffi import requests
from bs4 import BeautifulSoup

url = "https://www.ballarat.vic.gov.au/news"
print(f"Fetching {url}...")

try:
    response = requests.get(url, impersonate="chrome110", timeout=30)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save HTML for inspection
        with open("debug_ballarat.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        print("Saved HTML to debug_ballarat.html")
        
        # Try to find articles
        articles = soup.find_all('article')
        print(f"Found {len(articles)} <article> tags")
        
        # Try to find common news classes
        news_items = soup.select('.view-news .views-row')
        print(f"Found {len(news_items)} items with selector '.view-news .views-row'")
        
        # Try another common pattern
        cards = soup.select('.card')
        print(f"Found {len(cards)} items with selector '.card'")

except Exception as e:
    print(f"Error: {e}")
