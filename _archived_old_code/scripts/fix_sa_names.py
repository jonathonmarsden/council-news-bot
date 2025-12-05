import json
import re

def fix_sa_names():
    file_path = 'states/sa/councils.json'
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    councils = data.get('councils', [])
    fixed_count = 0
    
    for council in councils:
        name = council.get('name', '')
        new_name = name
        
        if name.endswith(' (City of)'):
            base_name = name[:-10]
            new_name = f"City of {base_name}"
        elif name.endswith(' (District Council of)'):
            base_name = name[:-22]
            new_name = f"District Council of {base_name}"
        elif name.endswith(' (Town of)'):
            base_name = name[:-10]
            new_name = f"Town of {base_name}"
        elif name.endswith(' (Rural City of)'):
            base_name = name[:-16]
            new_name = f"Rural City of {base_name}"
            
        if new_name != name:
            print(f"Renaming: '{name}' -> '{new_name}'")
            council['name'] = new_name
            fixed_count += 1
            
    if fixed_count > 0:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Fixed {fixed_count} names in {file_path}")
    else:
        print("No names needed fixing.")

if __name__ == "__main__":
    fix_sa_names()
