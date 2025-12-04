import json
import glob
import re

def check_council_names():
    files = glob.glob('states/*/councils.json')
    pattern = re.compile(r'.+\s\((City of|District Council of|Shire of|Regional Council|Town of|Rural City of|Aboriginal Shire Council)\)$')
    
    for file_path in files:
        print(f"Checking {file_path}...")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                councils = data.get('councils', [])
                found = 0
                for council in councils:
                    name = council.get('name', '')
                    if pattern.match(name):
                        print(f"  Found malformed name: {name}")
                        found += 1
                if found == 0:
                    print("  No malformed names found.")
                else:
                    print(f"  Found {found} malformed names.")
        except Exception as e:
            print(f"  Error reading {file_path}: {e}")

if __name__ == "__main__":
    check_council_names()
