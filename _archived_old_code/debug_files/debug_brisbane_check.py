from curl_cffi import requests
from bs4 import BeautifulSoup

url = "https://www.brisbane.qld.gov.au/about-council/council-information-and-rates/news-and-publications/living-in-brisbane-newsletter"
print(f"Fetching {url}...")

try:
    response = requests.get(url, impersonate="chrome110", timeout=30)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save HTML for inspection
        with open("debug_brisbane.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        print("Saved HTML to debug_brisbane.html")
        
        # Check configured selectors
        items = soup.select("div.cmp-download")
        print(f"Found {len(items)} items with selector 'div.cmp-download'")

except Exception as e:
    print(f"Error: {e}")
