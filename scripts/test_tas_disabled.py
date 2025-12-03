import json
import os
import sys
import concurrent.futures
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scrapers import ScraperFactory

def test_council(council_config):
    """Test a single council scraper."""
    try:
        # Force enable for testing
        council_config['enabled'] = True
        
        # Create scraper
        scraper = ScraperFactory.create_scraper(council_config)
        
        # Run scrape
        print(f"Testing {council_config['name']} ({council_config['id']})...")
        articles = scraper.scrape()
        
        if articles:
            print(f"✅ {council_config['name']}: Found {len(articles)} articles")
            return True, council_config['id'], len(articles), None
        else:
            print(f"❌ {council_config['name']}: No articles found")
            return False, council_config['id'], 0, "No articles found"
            
    except Exception as e:
        print(f"❌ {council_config['name']}: Error - {str(e)}")
        return False, council_config['id'], 0, str(e)

def main():
    # Load TAS config
    config_path = Path("states/tas/councils.json")
    with open(config_path, 'r') as f:
        data = json.load(f)
        
    councils = data['councils']
    # Filter for disabled councils
    disabled_councils = [c for c in councils if not c.get('enabled', True)]
    
    print(f"Found {len(disabled_councils)} disabled TAS councils.")
    
    results = []
    
    # Run in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_council = {executor.submit(test_council, council): council for council in disabled_councils}
        
        for future in concurrent.futures.as_completed(future_to_council):
            results.append(future.result())
            
    # Summary
    print("\n=== SUMMARY ===")
    passed = [r for r in results if r[0]]
    failed = [r for r in results if not r[0]]
    
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print("\nFailures:")
        for _, id, _, error in failed:
            print(f"- {id}: {error}")

if __name__ == "__main__":
    main()
