import json
import sqlite3
from pathlib import Path

def migrate():
    json_path = Path('data/posted_articles.json')
    db_path = 'bot.db'
    
    if not json_path.exists():
        print("No JSON data found to migrate")
        return

    print(f"Migrating {json_path} to {db_path}...")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    posted_urls = data.get('posted_urls', [])
    known_urls = data.get('known_urls', [])
    
    # Combine all URLs
    all_urls = set(posted_urls) | set(known_urls)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Ensure table exists (in case main_v2 hasn't run yet)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            council_id TEXT NOT NULL,
            title TEXT,
            date TEXT,
            excerpt TEXT,
            state TEXT NOT NULL,
            first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            posted_at TIMESTAMP,
            posted_to_handle TEXT
        )
    """)
    
    count = 0
    for url in all_urls:
        is_posted = url in posted_urls
        
        # We don't have title/council_id for these legacy URLs easily available
        # unless we re-scrape or parse the URL. 
        # For migration, we'll insert placeholders to prevent re-posting.
        
        try:
            cursor.execute(
                """
                INSERT INTO articles (url, council_id, state, posted_at, title)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    url, 
                    'legacy-migration', 
                    'VIC', # Assuming all current data is VIC
                    datetime.now() if is_posted else None,
                    'Legacy Article'
                )
            )
            count += 1
        except sqlite3.IntegrityError:
            pass # Skip duplicates
            
    conn.commit()
    conn.close()
    print(f"Migrated {count} URLs to database")

from datetime import datetime
if __name__ == "__main__":
    migrate()
