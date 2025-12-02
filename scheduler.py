#!/usr/bin/env python3
"""
Scheduler for Council News Bot.

Schedules scraping and posting tasks:
- Scrape all councils every 3 hours.
- Publish to BlueSky every 15 minutes between 5am and 10pm.
"""

import subprocess
import time
import sys
import os
from datetime import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for older Python versions (though 3.9+ is recommended)
    ZoneInfo = None

# Set Timezone
TZ_NAME = "Australia/Sydney"
try:
    TZ = ZoneInfo(TZ_NAME) if ZoneInfo else None
except Exception:
    TZ = None

def log(msg):
    # Use timezone-aware time if available
    now = datetime.now(TZ) if TZ else datetime.now()
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

def run_scrape(state):
    log(f"Starting scrape for {state}...")
    # Use the same Python interpreter that is running this script
    main_script = os.path.join(os.path.dirname(__file__), 'main.py')
    try:
        subprocess.run([sys.executable, main_script, "--state", state, "--scrape-only"], check=True)
        log(f"Finished scrape for {state}")
    except subprocess.CalledProcessError as e:
        log(f"Error scraping {state}: {e}")

def run_post(state):
    log(f"Posting for {state}...")
    main_script = os.path.join(os.path.dirname(__file__), 'main.py')
    try:
        # Post 1 article
        subprocess.run([sys.executable, main_script, "--state", state, "--post-only", "--limit", "1"], check=True)
    except subprocess.CalledProcessError as e:
        log(f"Error posting for {state}: {e}")

def main():
    log(f"Starting Scheduler (Timezone: {TZ_NAME if TZ else 'System Default'})...")
    
    # State tracking
    # Initialize with a very old time
    last_scrape_time = datetime.min
    # If using timezone, make this timezone-aware to avoid comparison errors
    if TZ:
        last_scrape_time = last_scrape_time.replace(tzinfo=TZ)
    
    # States to manage
    STATES = ["vic", "nsw", "qld", "tas"]
    
    while True:
        now = datetime.now(TZ) if TZ else datetime.now()
        
        # 1. Scrape Check (Every 3 hours)
        # We check if 3 hours have passed since last scrape
        if (now - last_scrape_time).total_seconds() >= 3 * 3600:
            log("Executing scheduled scrape...")
            for state in STATES:
                run_scrape(state)
            last_scrape_time = now
            
        # 2. Post Check (Every 5 minutes, 5am - 10pm)
        if 5 <= now.hour < 22:
            # Check if we are at a 5-minute mark (0, 5, 10, 15, ...)
            # We allow a small window (e.g., first minute of the block)
            if now.minute % 5 == 0:
                log("Executing scheduled post...")
                for state in STATES:
                    run_post(state)
                
                # Sleep for 65 seconds to ensure we don't trigger again in the same minute
                time.sleep(65)
                continue
        
        # Sleep for 30 seconds before next check
        time.sleep(30)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Scheduler stopped by user.")
