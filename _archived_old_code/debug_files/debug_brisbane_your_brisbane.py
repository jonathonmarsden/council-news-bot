
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.brisbane.qld.gov.au/about-council/your-brisbane"

print(f"Checking {url}...")
try:
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save HTML for inspection
        with open("debug_brisbane_your_brisbane.html", "w") as f:
            f.write(response.text)
        print("Saved HTML to debug_brisbane_your_brisbane.html")
        
        # Look for potential news items
        cards = soup.select(".card, .item, .cmp-list__item, article, .news-item, .tile")
        print(f"Found {len(cards)} potential item containers")
        
        for i, card in enumerate(cards[:10]):
            print(f"--- Card {i+1} ---")
            print(card.get_text(strip=True)[:100])
            link = card.find('a')
            if link:
                print(f"Link: {link.get('href')}")
                
except Exception as e:
    print(f"Error: {e}")
