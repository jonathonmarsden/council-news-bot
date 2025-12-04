import re

title = "Council Meeting Highlights February 202429 February 2024"
date_pattern = r'\d{1,2}\s+[A-Za-z]+\s+\d{4}$'
new_title = re.sub(date_pattern, '', title).strip()

print(f"Original: '{title}'")
print(f"New:      '{new_title}'")
