from curl_cffi import requests
from bs4 import BeautifulSoup

url = "https://www.brisbane.qld.gov.au/about-council/news-and-community-updates"
print(f"Fetching {url}...")

try:
    response = requests.get(url, impersonate="chrome110", timeout=30)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save HTML for inspection
        with open("debug_brisbane_updates.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        print("Saved HTML to debug_brisbane_updates.html")
        
        # Look for links
        links = soup.find_all('a')
        print(f"Found {len(links)} links")
        
        # Check for news-like links
        news_links = [l for l in links if '/news-' in l.get('href', '') or '/media-' in l.get('href', '')]
        print(f"Found {len(news_links)} potential news links")

except Exception as e:
    print(f"Error: {e}")
