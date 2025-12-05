
import json
from typing import List, Dict, Optional
from .base import BaseScraper, NewsArticle

class StirlingScraper(BaseScraper):
    """
    Scraper for City of Stirling (Kentico CMS with custom API).
    """
    
    def __init__(self, council_id: str, council_name: str, news_url: str, **kwargs):
        # Remove selectors if present, as BaseScraper doesn't accept it
        kwargs.pop('selectors', None)
        super().__init__(council_id, council_name, news_url, **kwargs)
        self.api_url = "https://www.stirling.wa.gov.au/ksearchnews/ksearchresult"

    def scrape(self) -> List[NewsArticle]:
        # SearchParam
        search_param = [
            {"key": "classname", "values": ["AWPT.News"], "or": "true", "operator": "eq"},
            {"key": "searchindexes", "values": ["News"], "or": "true", "operator": "eq"},
            {"key": "nodealiaspath", "values": ["/city-and-council/news"], "or": "true", "operator": "eq"}
        ]
        
        # SearchFilter
        search_filter = [
            {"key": "Sort", "values": ["ArticleReleaseDate DESC"], "or": False, "operator": ""}
        ]
        
        # Body
        body = {
            "take": self.limit or 20,
            "skip": 0,
            "page": 1,
            "pageSize": self.limit or 20
        }
        
        headers = {
            "Content-Type": "application/json",
            "SearchParam": json.dumps(search_param),
            "SearchFilter": json.dumps(search_filter),
            "Referer": "https://www.stirling.wa.gov.au/city-and-council/news",
            "Origin": "https://www.stirling.wa.gov.au"
        }
        
        # Use fetch_page but we need POST with JSON. 
        # BaseScraper.fetch_page is GET usually.
        # We need to use self.session or curl_cffi directly.
        
        # Since BaseScraper wraps curl_cffi/requests, let's see if we can use a helper.
        # BaseScraper doesn't expose a generic 'request' method easily, but we can use self.session if available.
        
        # However, BaseScraper uses `self.impersonate` which suggests curl_cffi.
        
        try:
            # We'll use curl_cffi directly as in the debug script, 
            # but we should respect the proxy/impersonate settings from BaseScraper if possible.
            # Actually, BaseScraper has `self.get_session()`? No.
            
            # Let's just import requests from curl_cffi here.
            from curl_cffi import requests
            
            response = requests.post(
                self.api_url, 
                json=body, 
                headers=headers, 
                impersonate=self.impersonate or "chrome110",
                proxies={"http": self.proxy, "https": self.proxy} if self.proxy else None,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Stirling API failed with status {response.status_code}")
                return []
                
            data = response.json()
            articles = []
            
            for item in data.get('Data', []):
                title = item.get('ArticleTitle')
                date_str = item.get('ArticleReleaseDate')
                summary = item.get('ArticleSummary')
                page_url = item.get('PageUrl')
                
                if not title or not page_url:
                    continue
                    
                url = self.make_absolute_url(page_url)
                date = self.parse_date(date_str)
                
                article = self.create_article(title, url, date, summary)
                articles.append(article)
                
            return articles
            
        except Exception as e:
            print(f"Error scraping Stirling: {e}")
            return []
