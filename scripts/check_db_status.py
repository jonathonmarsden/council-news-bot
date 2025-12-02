import sqlite3
import os
import sys

def check_status():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'bot.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Count total articles
    c.execute("SELECT COUNT(*) FROM articles")
    total = c.fetchone()[0]
    
    # Count unposted articles
    c.execute("SELECT COUNT(*) FROM articles WHERE posted_at IS NULL")
    unposted = c.fetchone()[0]
    
    # Get breakdown by council for unposted
    c.execute("""
        SELECT council_id, COUNT(*) 
        FROM articles 
        WHERE posted_at IS NULL 
        GROUP BY council_id 
        ORDER BY COUNT(*) DESC
    """)
    breakdown = c.fetchall()
    
    print(f"Total Articles: {total}")
    print(f"Unposted (Backlog): {unposted}")
    print("\nBacklog by Council:")
    for council, count in breakdown:
        print(f"  {council}: {count}")

if __name__ == "__main__":
    check_status()
