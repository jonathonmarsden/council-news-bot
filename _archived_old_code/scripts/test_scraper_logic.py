from bs4 import BeautifulSoup

def get_clean_title(element):
    if not element:
        return ""
        
    if not hasattr(element, 'children'):
        return element.get_text(strip=True)
        
    text_parts = []
    for child in element.children:
        if child.name:
            # Check classes
            classes = child.get('class', [])
            if isinstance(classes, list):
                classes_str = ' '.join(classes)
            else:
                classes_str = str(classes)
            
            if any(c in classes_str for c in ['date', 'published', 'time', 'meta', 'label', 'right']):
                continue
            if child.name == 'time':
                continue
                
            text_parts.append(child.get_text(" ", strip=True))
        elif child.string:
            text_parts.append(child.string.strip())
            
    return " ".join(filter(None, text_parts))

html = """
<a href="#">
    <div class="title">Penrith Unites for 16 Days of Action: We Can All Be Heroes</div>
    <div class="datestart">26 November 2025</div>
    <div class="intro">Penrith City Council is proud to announce...</div>
</a>
"""

soup = BeautifulSoup(html, 'html.parser')
link = soup.find('a')
print(f"Clean Title: '{get_clean_title(link)}'")
