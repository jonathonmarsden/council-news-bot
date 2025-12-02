#!/usr/bin/env python3
"""
Health Check Script

Analyzes the database and configuration to identify:
1. Broken scrapers (no articles in > 30 days)
2. Silent failures (councils in config but not in DB)
3. Activity stats
"""

import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_db_connection():
    # Respect the DB_PATH env var, similar to main.py
    default_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bot.db')
    db_path = os.environ.get('DB_PATH', default_db_path)
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        sys.exit(1)
        
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def load_all_councils():
    """Load all configured councils from JSON files."""
    councils = {}
    states_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'states')
    
    for state in ['vic', 'nsw', 'qld']:
        config_path = os.path.join(states_dir, state, 'councils.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                data = json.load(f)
                for c in data.get('councils', []):
                    c['state'] = state
                    councils[c['id']] = c
    return councils

def generate_report():
    conn = get_db_connection()
    configured_councils = load_all_councils()
    
    print(f"Analyzing {len(configured_councils)} configured councils...")
    
    # Get last seen date for each council
    cursor = conn.execute("""
        SELECT council_id, state, MAX(first_seen_at) as last_seen, COUNT(*) as article_count
        FROM articles
        GROUP BY council_id
    """)
    
    db_stats = {row['council_id']: dict(row) for row in cursor.fetchall()}
    
    # Analysis
    healthy = []
    stale = [] # > 30 days
    dead = [] # Never seen
    
    now = datetime.now()
    
    for c_id, config in configured_councils.items():
        if not config.get('enabled', True):
            continue
            
        stats = db_stats.get(c_id)
        
        if not stats:
            dead.append(config)
            continue
            
        last_seen_str = stats['last_seen']
        # Handle potential different date formats in DB
        try:
            last_seen = datetime.fromisoformat(last_seen_str)
        except ValueError:
            # Fallback for simple string dates if any
            last_seen = datetime.strptime(last_seen_str.split('.')[0], "%Y-%m-%d %H:%M:%S")
            
        days_since = (now - last_seen).days
        
        info = {
            'name': config['name'],
            'state': config['state'],
            'days_since': days_since,
            'last_seen': last_seen_str,
            'count': stats['article_count']
        }
        
        if days_since > 30:
            stale.append(info)
        else:
            healthy.append(info)
            
    # Output Report
    report_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'HEALTH_REPORT.md')
    
    with open(report_file, 'w') as f:
        f.write(f"# 🏥 Bot Health Report ({now.strftime('%Y-%m-%d')})\n\n")
        
        f.write("## 📊 Summary\n")
        f.write(f"- **Total Configured**: {len(configured_councils)}\n")
        f.write(f"- **Healthy (<30 days)**: {len(healthy)} ✅\n")
        f.write(f"- **Stale (>30 days)**: {len(stale)} ⚠️\n")
        f.write(f"- **Dead (Never scraped)**: {len(dead)} ❌\n\n")
        
        f.write("## ⚠️ Stale Scrapers (>30 Days)\n")
        f.write("| State | Council | Days Since | Last Article |\n")
        f.write("|-------|---------|------------|--------------|\n")
        for item in sorted(stale, key=lambda x: x['days_since'], reverse=True):
            f.write(f"| {item['state'].upper()} | {item['name']} | {item['days_since']} | {item['last_seen']} |\n")
            
        f.write("\n## ❌ Dead Scrapers (Never found articles)\n")
        f.write("| State | Council | URL |\n")
        f.write("|-------|---------|-----|\n")
        for item in dead:
            f.write(f"| {item['state'].upper()} | {item['name']} | {item['news_url']} |\n")
            
    print(f"Report generated at {report_file}")
    print(f"Summary: {len(healthy)} Healthy, {len(stale)} Stale, {len(dead)} Dead")

if __name__ == "__main__":
    generate_report()
