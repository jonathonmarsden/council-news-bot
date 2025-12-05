from bs4 import BeautifulSoup

html = """
<div class="news-listing__item-wrapper">
 <a class="news-listing__item-link" href="https://lgasa-search.squiz.cloud/s/redirect?collection=northern-areas-council-news-push&amp;url=https%3A%2F%2Flgasa-web.squiz.cloud%2Fframework%2Ffunnelback%2Fpush-click-tracking-redirect%3FpushAsset%3D1907971&amp;index_url=https%3A%2F%2Flgasa-web.squiz.cloud%2F%3Fa%3D1907971&amp;auth=cRjb0Gt95CB5dI2kVAIZ%2Bg&amp;profile=_default&amp;rank=1&amp;query=%21FunDoesNotExist" rel="nofollow">       <h2 class="news-listing__item-title">
   Job Opportunity - Traineeship
  </h2>
 </a>
 <div class="news-listing__item-date">
  3rd December 2025
 </div>
 <ul class="news-listing__categories">
  <li class="news-listing__category">
   Public Notice
  </li>
 </ul>
 <div class="news-listing__item-teaser">
  We Are Hiring Traineeship - Certificate III in Horticulture· Full-time, 2 year contra
ct· 9 Day fortnight with flexible work arrangements· Based at JamestownWe are looking for a switched on, energic, community minded person...                                  </div>
</div>
"""

soup = BeautifulSoup(html, 'html.parser')
container = soup.select_one('div.news-listing__item-wrapper')

title_selector = "h2.news-listing__item-title"
link_selector = "a.news-listing__item-link"
date_selector = "div.news-listing__item-date"

title_elem = container.select_one(title_selector)
print(f"Title Elem: {title_elem}")
if title_elem:
    print(f"Title Text: {title_elem.get_text(strip=True)}")

link_elem = container.select_one(link_selector)
print(f"Link Elem: {link_elem}")
if link_elem:
    print(f"Link Href: {link_elem.get('href')}")

date_elem = container.select_one(date_selector)
print(f"Date Elem: {date_elem}")
if date_elem:
    print(f"Date Text: {date_elem.get_text(strip=True)}")
