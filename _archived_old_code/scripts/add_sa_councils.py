from curl_cffi import requests
from bs4 import BeautifulSoup
import json
import os
import time
import re
from urllib.parse import urljoin

# Constants
LISTING_URL = "https://www.lga.sa.gov.au/sa-councils/councils-listing"
OUTPUT_FILE = "states/sa/councils.json"

def get_soup(url):
    try:
        response = requests.get(url, impersonate="chrome110", timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def clean_name(name):
    # Remove (City of), (District Council of), etc for the ID
    name = name.strip()
    clean = re.sub(r'\s*\(.*?\)', '', name)
    clean = re.sub(r'Council', '', clean)
    clean = clean.strip()
    return clean.lower().replace(' ', '-')

def main():
    print(f"Fetching council list from {LISTING_URL}...")
    soup = get_soup(LISTING_URL)
    if not soup:
        return

    councils = []
    
    # Find the A-Z list
    # Based on the fetch_webpage output, links are like:
    # [Adelaide (City of )](https://www.lga.sa.gov.au/sa-councils/councils-listing/city-of-adelaide)
    
    # Look for the section "A-Z list of SA councils"
    # It seems to be a list of links.
    
    links = soup.find_all('a', href=True)
    council_links = []
    
    for link in links:
        href = link['href']
        text = link.get_text(strip=True)
        
        if '/sa-councils/councils-listing/' in href and 'accordion-items' not in href:
            # Filter out non-council links if any
            if text and text != "Read more":
                council_links.append((text, href))

    # Remove duplicates
    council_links = list(set(council_links))
    council_links.sort()
    
    print(f"Found {len(council_links)} potential councils.")
    
    for name, profile_url in council_links:
        print(f"Processing {name}...")
        
        # Handle relative URLs
        if not profile_url.startswith('http'):
            profile_url = urljoin(LISTING_URL, profile_url)
            
        profile_soup = get_soup(profile_url)
        if not profile_soup:
            continue
            
        # Extract Website
        # Look for a link with text "web" or similar, or just the first external link in the contact section
        website_url = None
        
        # Strategy 1: Look for 'web' text in link
        for a in profile_soup.find_all('a', href=True):
            text = a.get_text().lower()
            href = a['href'].lower()
            if 'web' in text or 'website' in text:
                website_url = a['href']
                break
        
        # Strategy 2: Look for any external link that looks like a council site
        if not website_url:
             for a in profile_soup.find_all('a', href=True):
                 href = a['href']
                 # Skip internal links and social media
                 if 'lga.sa.gov.au' in href or 'localcouncils.sa.gov.au' in href:
                     continue
                 if 'facebook' in href or 'instagram' in href or 'twitter' in href or 'linkedin' in href or 'google' in href or 'youtube' in href:
                     continue
                 if 'mailto:' in href:
                     # Handle mailto:http://... edge case
                     if 'http' in href:
                         website_url = href.split('mailto:')[-1]
                         break
                     continue
                     
                 # Must be http(s)
                 if not href.startswith('http'):
                     continue
                     
                 # If it ends in .sa.gov.au, it's a winner
                 if '.sa.gov.au' in href:
                     website_url = href
                     break
                     
                 # If it contains the council name (fuzzy)
                 clean_c_name = clean_name(name).replace('-','')
                 if clean_c_name in href.replace('-','').replace('.',''):
                     website_url = href
                     break

        if website_url:
            # Clean URL
            website_url = website_url.rstrip('/')
            
            council_id = clean_name(name)
            
            # Guess news URL
            news_url = f"{website_url}/news"
            
            council_entry = {
                "id": council_id,
                "name": name,
                "url": news_url,
                "parser": "html",
                "selectors": {
                    "container": "div.news-list, div.post-list, div.listing",
                    "title": "h2, h3, h4",
                    "date": "span.date, time",
                    "link": "a"
                }
            }
            councils.append(council_entry)
            print(f"  -> Found: {website_url}")
        else:
            print(f"  -> ⚠️ Could not find website for {name}")
            
        time.sleep(0.5) # Be nice

    # Save to file
    output_data = {"councils": councils}
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output_data, f, indent=4)
        
    print(f"\nSaved {len(councils)} councils to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
