import os
import sys
import re
import time
from datetime import datetime
from dotenv import load_dotenv
from atproto import Client, models

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import load_state_config, get_scraper
from core.poster import BlueSkyPoster

def get_council_from_text(text, councils):
    # Try to match council name in text
    for council in councils:
        if council['name'] in text:
            return council
    
    # Try hashtags
    hashtags = re.findall(r'#(\w+)', text)
    for tag in hashtags:
        # Convert PascalCase to space separated (approximate)
        # This is fuzzy, but might work.
        pass
        
    return None

def fix_and_repost():
    load_dotenv()
    
    # User credentials
    user_handle = os.environ.get('BLUESKY_HANDLE_DEBUG', "jonathonmarsden.com")
    user_password = os.environ.get('BLUESKY_PASSWORD_DEBUG', "gars-eqs3-ruay-ym35")
    
    # Bot credentials
    bots = {
        'VIC': {
            'handle': os.environ.get('BLUESKY_HANDLE_VIC'),
            'password': os.environ.get('BLUESKY_PASSWORD_VIC'),
            'poster': None
        },
        'NSW': {
            'handle': os.environ.get('BLUESKY_HANDLE_NSW'),
            'password': os.environ.get('BLUESKY_PASSWORD_NSW'),
            'poster': None
        },
        'QLD': {
            'handle': os.environ.get('BLUESKY_HANDLE_QLD'),
            'password': os.environ.get('BLUESKY_PASSWORD_QLD'),
            'poster': None
        }
    }
    
    # Load all councils
    all_councils = []
    for state in ['vic', 'nsw', 'qld']:
        data = load_state_config(state)
        for c in data['councils']:
            c['state'] = state.upper()
            all_councils.append(c)
            
    print(f"Loaded {len(all_councils)} councils.")
    
    # Authenticate User
    print(f"\n--- Authenticating as {user_handle} ---")
    user_client = Client()
    user_client.login(user_handle, user_password)
    print("Authenticated.")
    
    # Get Bookmarks
    response = user_client.app.bsky.bookmark.get_bookmarks()
    bookmarks = response.bookmarks
    
    if not bookmarks:
        print("No bookmarks found.")
        return

    print(f"Found {len(bookmarks)} bookmarks to process.")
    
    for i, bookmark in enumerate(bookmarks):
        print(f"\n--- Processing Bookmark {i+1} ---")
        uri = bookmark.subject.uri
        print(f"URI: {uri}")
        
        # Get post details
        item = bookmark.item
        if not hasattr(item, 'record'):
            print("Skipping: No record found.")
            continue
            
        text = item.record.text
        author_did = item.author.did
        author_handle = item.author.handle
        
        print(f"Author: {author_handle}")
        # print(f"Text: {text[:50]}...")
        
        # Determine State from Author
        state = None
        if 'vic' in author_handle.lower():
            state = 'VIC'
        elif 'nsw' in author_handle.lower():
            state = 'NSW'
        elif 'qld' in author_handle.lower():
            state = 'QLD'
            
        if not state:
            print(f"Could not determine state from handle {author_handle}")
            continue
            
        # Find Council
        council = get_council_from_text(text, [c for c in all_councils if c['state'] == state])
        
        if not council:
            print("Could not identify council from text.")
            # Try to extract URL and match against council news_urls
            # Extract URL from facets
            url = None
            if item.record.facets:
                for facet in item.record.facets:
                    for feature in facet.features:
                        if hasattr(feature, 'uri'):
                            url = feature.uri
                            break
            
            if url:
                print(f"Found URL: {url}")
                # Try to match domain
                for c in all_councils:
                    if c['state'] == state and c['news_url'] in url: # Very rough check
                         council = c
                         break
                    # Better: check if news_url domain matches
                    from urllib.parse import urlparse
                    if c['state'] == state:
                        c_domain = urlparse(c['news_url']).netloc
                        u_domain = urlparse(url).netloc
                        if c_domain == u_domain:
                            council = c
                            break
        
        if not council:
            print("Still could not identify council. Skipping.")
            continue
            
        print(f"Identified Council: {council['name']}")
        
        # Extract Article URL
        article_url = None
        if item.record.facets:
            for facet in item.record.facets:
                for feature in facet.features:
                    if hasattr(feature, 'uri'):
                        article_url = feature.uri
                        break
        
        if not article_url:
            print("No article URL found in facets. Skipping.")
            continue
            
        print(f"Article URL: {article_url}")
        
        # Re-scrape
        print("Re-scraping...")
        scraper = get_scraper(council)
        articles = scraper.scrape()
        
        # Find matching article
        found_article = None
        for art in articles:
            # Compare URLs (ignoring query params or slight differences)
            if art.url == article_url or art.url.rstrip('/') == article_url.rstrip('/'):
                found_article = art
                break
        
        if not found_article:
            print("Article not found on index page. Trying direct fetch (fallback)...")
            # Fallback: Create a dummy article and try to fetch details
            # But we need the Title and Excerpt which are on the page.
            # We can try to fetch the article page and parse it.
            # But CardScraper doesn't have a generic 'parse_article_page' method.
            # However, we can try to use the scraper's internal methods if we hack it.
            # Or just skip for now.
            print("Skipping re-post (not found on index).")
            continue
            
        print(f"Found Article: {found_article.title}")
        print(f"Date: {found_article.date}")
        print(f"Excerpt: {found_article.excerpt}")
        
        # Initialize Bot Poster if needed
        if not bots[state]['poster']:
            print(f"Initializing {state} poster...")
            poster = BlueSkyPoster(bots[state]['handle'], bots[state]['password'])
            if poster.authenticate():
                bots[state]['poster'] = poster
            else:
                print(f"Failed to authenticate {state} bot.")
                continue
                
        poster = bots[state]['poster']
        
        # Post
        print("Posting fixed article...")
        hashtags = load_state_config(state.lower())['config']['hashtags']
        # Add council specific hashtag
        council_tag = poster._council_to_hashtag(council['name'])
        if council_tag not in hashtags:
            hashtags.append(council_tag)
            
        success = poster.post_article(
            council_name=council['name'],
            title=found_article.title,
            url=found_article.url,
            date=found_article.date,
            excerpt=found_article.excerpt,
            hashtags=hashtags
        )
        
        if success:
            print("Post successful. Deleting bookmark...")
            # Find the bookmark record rkey
            # We have to list all bookmarks and find the one pointing to this URI
            try:
                # Fetch all bookmark records
                # Note: This might be paginated, but for 19 items it's fine
                records = user_client.com.atproto.repo.list_records(
                    collection='app.bsky.bookmark',
                    repo=user_client.me.did,
                    limit=100
                )
                
                bookmark_rkey = None
                for record in records.records:
                    # record.value is the record data
                    if record.value.subject.uri == uri:
                        bookmark_rkey = record.uri.split('/')[-1]
                        break
                
                if bookmark_rkey:
                    user_client.com.atproto.repo.delete_record(
                        collection='app.bsky.bookmark',
                        repo=user_client.me.did,
                        rkey=bookmark_rkey
                    )
                    print(f"Deleted bookmark {bookmark_rkey}")
                else:
                    print("Could not find bookmark record to delete.")
                    
            except Exception as e:
                print(f"Error deleting bookmark: {e}")
            
        else:
            print("Post failed.")
            
        # Sleep to avoid rate limits
        time.sleep(2)

if __name__ == "__main__":
    fix_and_repost()
