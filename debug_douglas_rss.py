from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser as date_parser

xml_content = """<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:atom="http://www.w3.org/2005/Atom"
	xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
	xmlns:slash="http://purl.org/rss/1.0/modules/slash/"
	>

<channel>
	<title>Douglas Shire Council</title>
	<item>
		<title>Tree Maintenance Works &#8211; Grant Street, Port Douglas</title>
		<link>https://douglas.qld.gov.au/tree-maintenance-works-grant-street-port-douglas/?utm_source=rss&#038;utm_medium=rss&#038;utm_campaign=tree-maintenance-works-grant-street-port-douglas</link>
		
		<dc:creator><![CDATA[Tarren Woodhams]]></dc:creator>
		<pubDate>Thu, 20 Nov 2025 01:18:25 +0000</pubDate>
				<category><![CDATA[Works Notice]]></category>
		<guid isPermaLink="false">https://douglas.qld.gov.au/?p=75707</guid>

					<description><![CDATA[<p>The post <a href="https://douglas.qld.gov.au/tree-maintenance-works-grant-street-port-douglas/">Tree Maintenance Works &#8211; Grant Street, Port Douglas</a> appeared first on <a href="https://douglas.qld.gov.au">Douglas Shire Council</a>.</p>
]]></description>
										<content:encoded><![CDATA[
		<div id="fws_692f8cebe6107"  data-column-margin="default" data-midnight="dark"  class="wpb_row vc_row-fluid vc_row"  style="padding-top: 0px; padding-bottom: 0px; "><div class="row-bg-wrap" data-bg-animation="none" data-bg-overlay="false"><div class="inner-wrap"><div class="row-bg viewport-desktop"  style=""></div></div></div><div class="row_col_wrap_12 col span_12 dark left">
	<div  class="vc_col-sm-12 wpb_column column_container vc_column_container col no-extra-padding inherit_tablet inherit_phone "  data-padding-pos="all" data-has-bg-color="false" data-bg-color="" data-bg-opacity="1" data-animation="" data-delay="0" >
		<div class="vc_column-inner" >
			<div class="wpb_wrapper">
				
<div class="wpb_text_column wpb_content_element " >
	<div class="wpb_wrapper">
		<h3><span style="color: #008080;"><strong>Public Notice: Tree Maintenance Works – Grant Street</strong></span></h3>
<p>Tree maintenance works will be carried out on Grant Street, in Port Douglas on Monday 1 December 2025 (weather permitting).</p>
	</div>
</div>
]]></content:encoded>
    </item>
</channel>
</rss>"""

soup = BeautifulSoup(xml_content, 'xml')
items = soup.find_all('item')

for item in items:
    title_elem = item.find('title')
    link_elem = item.find('link')
    desc_elem = item.find('description')
    date_elem = item.find('pubDate')
    
    title = title_elem.get_text(strip=True)
    link = link_elem.get_text(strip=True)
    
    print(f"Title: {title}")
    print(f"Link: {link}")
    
    if desc_elem:
        desc_text = desc_elem.get_text(strip=True)
        print(f"Raw Description: {desc_text}")
        desc_soup = BeautifulSoup(desc_text, 'html.parser')
        excerpt = desc_soup.get_text(strip=True)[:200] + "..."
        print(f"Excerpt: {excerpt}")
