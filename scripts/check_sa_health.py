
import json
import os
import subprocess
import sys
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_sa_councils():
    with open('states/sa/councils.json', 'r') as f:
        data = json.load(f)
    return [c for c in data['councils'] if c.get('enabled', True)]

def check_council(council):
    c_id = council['id']
    c_name = council['name']
    print(f"Checking {c_name} ({c_id})...")
    
    try:
        # Run main.py for this specific council
        result = subprocess.run(
            [sys.executable, 'main.py', '--state', 'sa', '--council', c_id, '--scrape-only'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout + result.stderr
        
        # Look for "Found X articles"
        match = re.search(r'Found (\d+) articles', output)
        if match:
            count = int(match.group(1))
            return {
                'id': c_id,
                'name': c_name,
                'status': 'OK' if count > 0 else 'ZERO',
                'count': count,
                'error': None
            }
        else:
            # Check for errors
            if "Error" in output or "Exception" in output:
                return {
                    'id': c_id,
                    'name': c_name,
                    'status': 'ERROR',
                    'count': 0,
                    'error': "Script error"
                }
            return {
                'id': c_id,
                'name': c_name,
                'status': 'UNKNOWN',
                'count': 0,
                'error': "No count found"
            }
            
    except subprocess.TimeoutExpired:
        return {
            'id': c_id,
            'name': c_name,
            'status': 'TIMEOUT',
            'count': 0,
            'error': "Timed out"
        }
    except Exception as e:
        return {
            'id': c_id,
            'name': c_name,
            'status': 'ERROR',
            'count': 0,
            'error': str(e)
        }

def main():
    councils = get_sa_councils()
    print(f"Found {len(councils)} enabled SA councils.")
    
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_council = {executor.submit(check_council, c): c for c in councils}
        for future in as_completed(future_to_council):
            results.append(future.result())
            
    print("\n" + "="*60)
    print(f"{'Council':<30} | {'Status':<10} | {'Count':<5} | {'Notes'}")
    print("-" * 60)
    
    ok_count = 0
    zero_count = 0
    error_count = 0
    
    for r in sorted(results, key=lambda x: x['name']):
        status = r['status']
        notes = r['error'] if r['error'] else ""
        print(f"{r['name'][:30]:<30} | {status:<10} | {r['count']:<5} | {notes}")
        
        if status == 'OK':
            ok_count += 1
        elif status == 'ZERO':
            zero_count += 1
        else:
            error_count += 1
            
    print("-" * 60)
    print(f"Total: {len(councils)}")
    print(f"OK: {ok_count}")
    print(f"ZERO: {zero_count}")
    print(f"ERROR/TIMEOUT: {error_count}")

if __name__ == "__main__":
    main()
