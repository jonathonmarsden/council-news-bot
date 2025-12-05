#!/usr/bin/env python3
"""
Cleanup Duplicate Posts on BlueSky.

This script:
1. Connects to BlueSky for a specific state.
2. Fetches the user's recent posts (feed).
3. Identifies duplicates based on the external link (URI) in the post facets.
4. Deletes the older duplicates, keeping only the most recent one.
"""

import os
import sys
import argparse
import json
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv
from atproto import Client, models

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_state_config(state_code: str):
    """Load configuration for a specific state."""
    base_path = Path(__file__).parent.parent / 'states' / state_code.lower()
    config_file = base_path / 'config.json'
    
    if not config_file.exists():
        raise ValueError(f"State configuration not found: {state_code}")
        
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def get_post_link(post_record):
    """Extract the external link from a post record."""
    if not hasattr(post_record, 'facets') or not post_record.facets:
        return None
        
    for facet in post_record.facets:
        for feature in facet.features:
            if isinstance(feature, models.AppBskyRichtextFacet.Link):
                return feature.uri
            # Also check if it's a dict (sometimes happens with raw data)
            if hasattr(feature, 'uri'):
                return feature.uri
    return None

def cleanup_duplicates(state_code: str, dry_run: bool = True):
    """Fetch posts and delete duplicates."""
    print(f"=== Cleaning up duplicates for {state_code.upper()} ===")
    
    # Load Config
    config = load_state_config(state_code)
    handle = os.environ.get(config['bluesky_handle_env'])
    password = os.environ.get(config['bluesky_password_env'])
    
    if not handle or not password:
        print(f"Error: Credentials not found for {state_code}")
        return

    # Connect
    client = Client()
    try:
        client.login(handle, password)
        print(f"Authenticated as {handle}")
    except Exception as e:
        print(f"Authentication failed: {e}")
        return

    # Fetch Author Feed
    # We need to fetch enough posts to cover the period of instability
    # Let's fetch last 100 posts
    print("Fetching recent posts...")
    feed = client.get_author_feed(actor=handle, limit=100)
    
    posts_by_link = defaultdict(list)
    
    for feed_view in feed.feed:
        post = feed_view.post
        record = post.record
        uri = post.uri
        cid = post.cid
        
        # Extract the link (this is our unique key for the article)
        link = get_post_link(record)
        
        if link:
            # Store tuple of (indexed_at, uri, text)
            # indexed_at is a string, but ISO format sorts correctly
            posts_by_link[link].append({
                'uri': uri,
                'cid': cid,
                'indexed_at': post.indexed_at,
                'text': record.text[:50] + "..."
            })
    
    # Identify Duplicates
    duplicates_found = 0
    deleted_count = 0
    
    for link, posts in posts_by_link.items():
        if len(posts) > 1:
            duplicates_found += 1
            print(f"\nFound {len(posts)} copies of: {link}")
            
            # Sort by time (newest first)
            # We want to KEEP the newest one (or oldest? Usually newest is safer if we just posted it)
            # Actually, if we keep the newest, we delete the older ones.
            # Let's sort descending by indexed_at
            posts.sort(key=lambda x: x['indexed_at'], reverse=True)
            
            keep = posts[0]
            to_delete = posts[1:]
            
            print(f"  Keeping: {keep['indexed_at']} - {keep['text']}")
            
            for p in to_delete:
                print(f"  DELETING: {p['indexed_at']} - {p['text']}")
                if not dry_run:
                    try:
                        client.delete_post(post_uri=p['uri'])
                        print("    ✅ Deleted")
                        deleted_count += 1
                    except Exception as e:
                        print(f"    ❌ Failed to delete: {e}")
    
    print(f"\nSummary: Found {duplicates_found} duplicated articles.")
    if dry_run:
        print("Dry run complete. No posts were deleted.")
        print("Run with --execute to actually delete posts.")
    else:
        print(f"Deleted {deleted_count} duplicate posts.")

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description='Cleanup BlueSky Duplicates')
    parser.add_argument('--state', type=str, required=True, help='State code (vic, nsw, etc)')
    parser.add_argument('--execute', action='store_true', help='Actually delete posts')
    
    args = parser.parse_args()
    
    cleanup_duplicates(args.state, dry_run=not args.execute)
