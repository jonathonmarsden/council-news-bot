import json
import os
import re
from urllib.parse import urlparse, urljoin
from curl_cffi import requests
from bs4 import BeautifulSoup

# Constants
AGGREGATION_URL = "https://www.lga.sa.gov.au/news-and-events/news/sacouncilsnews"
CONFIG_FILE = "states/sa/councils.json"

def get_soup(url):
    try:
        print(f"Fetching {url}...")
        response = requests.get(url, impersonate="chrome110", timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def infer_news_url(article_url):
    """
    Infers the news listing URL from an article URL.
    Removes the last segment of the path.
    """
    parsed = urlparse(article_url)
    path = parsed.path
    
    # Remove trailing slash if present
    if path.endswith('/'):
        path = path[:-1]
        
    # Split path
    parts = path.split('/')
    
    # Remove the last part (the article slug)
    if len(parts) > 1:
        parent_path = '/'.join(parts[:-1])
    else:
        parent_path = path
        
    return f"{parsed.scheme}://{parsed.netloc}{parent_path}"

def main():
    # 1. Load existing config
    if not os.path.exists(CONFIG_FILE):
        print(f"Config file {CONFIG_FILE} not found.")
        return
        
    with open(CONFIG_FILE, 'r') as f:
        data = json.load(f)
        
    councils = data.get('councils', [])
    council_map = {} # domain -> council object
    
    for c in councils:
        # Extract domain from current URL
        # Note: The key might be 'url' or 'news_url' depending on how it was generated.
        # The previous script used 'url', but the sed command might have messed things up or I misread the file.
        # Looking at the file content, it seems to be 'news_url' in the snippet provided by read_file?
        # Wait, the read_file output shows "news_url": "..."
        # But my add_sa_councils.py script used "url".
        # Ah, I see what happened. The previous script `add_sa_councils.py` used "url".
        # But the `read_file` output shows `news_url`. 
        # Did I edit it manually? No.
        # Let's check `add_sa_councils.py` again. It used `url`.
        # Wait, I see `news_url` in the read_file output above.
        # Let's handle both.
        
        current_url = c.get('url') or c.get('news_url')
        if not current_url:
            continue
            
        parsed = urlparse(current_url)
        domain = parsed.netloc.replace('www.', '')
        council_map[domain] = c
        
    print(f"Loaded {len(councils)} councils.")

    # 2. Fetch aggregation page
    soup = get_soup(AGGREGATION_URL)
    if not soup:
        return

    # 3. Find article links
    # The page structure seems to be a list of links.
    # We look for external links that match known council domains.
    
    links = soup.find_all('a', href=True)
    print(f"Found {len(links)} links on the page.")
    
    updates = 0
    
    for link in links:
        href = link['href']
        if not href.startswith('http'):
            continue
            
        parsed_href = urlparse(href)
        domain = parsed_href.netloc.replace('www.', '')
        
        # Check if this domain belongs to a known council
        if domain in council_map:
            council = council_map[domain]
            
            # Infer new URL
            new_url = infer_news_url(href)
            
            current_url = council.get('url') or council.get('news_url')
            
            # Update if different and looks like a valid news listing (not just root)
            if new_url != current_url and new_url != f"{parsed_href.scheme}://{parsed_href.netloc}":
                # Check if the new URL is actually better.
                # Current URL is often just /news (guessed).
                # If the inferred URL is longer/more specific, it's likely better.
                
                # Also avoid updating if we already have a specific path and this one is just different but not necessarily better?
                # Actually, the aggregation page links to ACTUAL articles, so the parent dir is almost certainly the correct news listing.
                
                print(f"Updating {council['name']}:")
                print(f"  Old: {current_url}")
                print(f"  New: {new_url}")
                print(f"  (Based on article: {href})")
                
                # Standardize on 'url' key if that's what the rest of the bot uses?
                # The bot uses 'url' in other states.
                # But the file I read has 'news_url'.
                # I should probably stick to what's in the file to avoid breaking things, OR standardize.
                # Let's check `main.py` or `core/scrapers/base.py`.
                # BaseScraper takes `news_url`.
                # But `main.py` loads config.
                # Let's just update whichever key exists.
                
                if 'url' in council:
                    council['url'] = new_url
                else:
                    council['news_url'] = new_url
                    
                updates += 1
                
                # Remove from map so we don't update it again with a potentially different link (first one is usually fine)
                # Or maybe we should keep looking to see if there's a pattern? 
                # For now, first match is good enough.
                del council_map[domain]

    # 4. Save config
    if updates > 0:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"\nUpdated {updates} councils in {CONFIG_FILE}")
    else:
        print("\nNo updates found.")

if __name__ == "__main__":
    main()
