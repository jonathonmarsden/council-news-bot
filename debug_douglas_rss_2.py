from bs4 import BeautifulSoup

xml_content = """<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	>
<channel>
	<item>
		<title>Test</title>
		<content:encoded><![CDATA[
		<div class="wpb_wrapper">
		<h3><span style="color: #008080;"><strong>Public Notice: Tree Maintenance Works – Grant Street</strong></span></h3>
<p>Tree maintenance works will be carried out on Grant Street, in Port Douglas on Monday 1 December 2025 (weather permitting).</p>
	</div>
]]></content:encoded>
    </item>
</channel>
</rss>"""

soup = BeautifulSoup(xml_content, 'xml')
item = soup.find('item')
content_encoded = item.find('content:encoded')

if content_encoded:
    print("Found content:encoded")
    content_text = content_encoded.get_text(strip=True)
    content_soup = BeautifulSoup(content_text, 'html.parser')
    
    # Try to find the first meaningful paragraph
    for p in content_soup.find_all('p'):
        text = p.get_text(strip=True)
        if len(text) > 20:
            print(f"Content Excerpt: {text}")
            break
else:
    print("No content:encoded found")
