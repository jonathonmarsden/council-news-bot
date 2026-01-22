#!/usr/bin/env python3
"""
Async Scheduler for Council News Bot.

Schedules scraping and posting tasks:
- Scrape all councils every 3 hours.
- Publish to BlueSky every 5 minutes between 5am and 10pm.

Uses asyncio to ensure long-running scrape jobs do not block posting jobs.
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for older Python versions
    ZoneInfo = None

# Set Timezone
TZ_NAME = "Australia/Sydney"
try:
    TZ = ZoneInfo(TZ_NAME) if ZoneInfo else None
except Exception:
    TZ = None

def get_now():
    """Get current timezone-aware time."""
    return datetime.now(TZ) if TZ else datetime.now()

def log(msg):
    print(f"[{get_now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)

def get_available_states():
    """Discover available states from the states/ directory."""
    states_dir = os.path.join(os.path.dirname(__file__), 'states')
    if not os.path.exists(states_dir):
        return []
    
    states = []
    for item in os.listdir(states_dir):
        item_path = os.path.join(states_dir, item)
        if os.path.isdir(item_path):
            # Check if it has a councils.json
            if os.path.exists(os.path.join(item_path, 'councils.json')):
                states.append(item)
    return sorted(states)

async def run_process(args, description, timeout=600):
    """Run a subprocess asynchronously with timeout."""
    try:
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            process.kill()
            log(f"Timeout running {description} (killed after {timeout}s)")
            return

        if process.returncode != 0:
            log(f"Error in {description}: {stderr.decode().strip()}")
            # Also log stdout as it might contain the actual python exception if stderr is empty
            stdout_str = stdout.decode().strip()
            if stdout_str:
                log(f"Stdout for {description}: {stdout_str}")
        else:
            # Log summary lines from stdout for visibility
            stdout_str = stdout.decode().strip()
            if stdout_str:
                for line in stdout_str.split('\n'):
                    # Capture critical info, warnings, and error messages
                    if any(key in line for key in ["Processing Summary", "Posted", "Warning", "Error", "Exception", "Critical", "Skipping", "DISABLED"]):
                        log(f"[{description}] {line.strip()}")
            
    except Exception as e:
        log(f"Exception running {description}: {e}")

async def scrape_state(state):
    """Scrape a single state."""
    log(f"Starting scrape for {state}...")
    main_script = os.path.join(os.path.dirname(__file__), 'main.py')
    # Limit concurrency to 2 workers to prevent VPS overload
    await run_process(
        [sys.executable, main_script, "--state", state, "--scrape-only", "--concurrency", "2"],
        f"scrape for {state}",
        timeout=3600  # 1 hour timeout for scraping
    )
    log(f"Finished scrape for {state}")

async def post_state(state):
    """Post for a single state."""
    log(f"Posting for {state}...")
    main_script = os.path.join(os.path.dirname(__file__), 'main.py')
    await run_process(
        [sys.executable, main_script, "--state", state, "--post-only", "--limit", "10", "--max-per-council", "10"],
        f"post for {state}",
        timeout=300  # 5 minutes timeout for posting
    )

async def scrape_job():
    """The main scraping loop."""
    log("Starting Scrape Loop...")
    
    while True:
        start_time = get_now()
        states = get_available_states()
        
        log(f"Executing scheduled scrape for states: {states}")
        
        # Run states sequentially to avoid overloading the VPS CPU/RAM
        for state in states:
            await scrape_state(state)
            
        duration = (get_now() - start_time).total_seconds()
        log(f"Full scrape cycle completed in {int(duration)} seconds.")
        
        # Wait for 3 hours before next run
        await asyncio.sleep(3 * 3600)

async def post_job():
    """The main posting loop."""
    log("Starting Post Loop...")
    
    while True:
        now = get_now()
        
        # Check window: 5am - 10pm
        if 5 <= now.hour < 22:
            states = get_available_states()
            log(f"Executing scheduled post for states: {states}")
            
            # Run posts sequentially to avoid RAM spikes (spawning 5 python processes at once)
            for state in states:
                await post_state(state)
            
        # Calculate time until next 5-minute mark
        now = get_now()
        minutes_to_next = 5 - (now.minute % 5)
        seconds_to_next = (minutes_to_next * 60) - now.second
        
        # Ensure we don't sleep 0 or negative if we are right on the mark
        if seconds_to_next <= 0:
            seconds_to_next += 300
            
        # Add a small buffer to ensure we land just after the minute
        await asyncio.sleep(seconds_to_next + 1)

async def health_check_job():
    """Daily health check loop."""
    log("Starting Health Check Loop...")
    while True:
        # Run once every 24 hours
        await asyncio.sleep(24 * 3600)
        
        log("Executing Daily Health Check & Zombie Audit...")
        try:
             # Run the audit script
             audit_script = os.path.join(os.path.dirname(__file__), 'scripts', 'maintenance', 'audit_silent_failures.py')
             if os.path.exists(audit_script):
                 await run_process([sys.executable, audit_script], "Daily Zombie Audit", timeout=300)
             else:
                 log(f"Warning: Audit script not found at {audit_script}")
        except Exception as e:
            log(f"Error running health check: {e}")

async def main():
    log(f"Starting Async Scheduler (Timezone: {TZ_NAME if TZ else 'System Default'})...")
    
    # Run loops concurrently
    await asyncio.gather(
        scrape_job(),
        post_job(),
        health_check_job()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log("Scheduler stopped by user.")
