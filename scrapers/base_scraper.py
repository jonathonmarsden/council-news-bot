"""
Base scraper class for council news pages.

Provides common functionality for scraping news articles from Victorian council websites.
"""

import re
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser


@dataclass
class NewsArticle:
    """Represents a news article from a council website."""
    
    council_id: str
    council_name: str
    title: str
    url: str
    date: Optional[datetime] = None
    excerpt: Optional[str] = None
    
    @property
    def unique_id(self) -> str:
        """Generate a unique identifier for this article."""
        return self.url
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'council_id': self.council_id,
            'council_name': self.council_name,
            'title': self.title,
            'url': self.url,
            'date': self.date.isoformat() if self.date else None,
            'excerpt': self.excerpt
        }


class BaseScraper(ABC):
    """Base class for council news scrapers."""
    
    # Common headers to mimic a browser
    # Note: Using 'gzip, deflate' only - 'br' (brotli) requires extra library
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-AU,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    def __init__(self, council_id: str, council_name: str, news_url: str, use_curl: bool = False):
        """
        Initialize the scraper.
        
        Args:
            council_id: Unique identifier for the council (kebab-case)
            council_name: Human-readable council name
            news_url: URL of the council's news page
            use_curl: Whether to use curl for WAF bypass
        """
        self.council_id = council_id
        self.council_name = council_name
        self.news_url = news_url
        self.use_curl = use_curl
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a web page, handling WAF protection if needed.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content as string, or None if fetch failed
        """
        if self.use_curl:
            return self._fetch_with_curl(url)
        return self._fetch_with_requests(url)
    
    def _fetch_with_requests(self, url: str) -> Optional[str]:
        """Fetch page using requests library."""
        try:
            response = self.session.get(url, timeout=30, allow_redirects=True)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def _fetch_with_curl(self, url: str) -> Optional[str]:
        """Fetch page using curl for WAF bypass."""
        try:
            result = subprocess.run(
                [
                    'curl', '-s', '-L',
                    '-A', self.HEADERS['User-Agent'],
                    '-H', f"Accept: {self.HEADERS['Accept']}",
                    '-H', f"Accept-Language: {self.HEADERS['Accept-Language']}",
                    '--connect-timeout', '30',
                    '--max-time', '60',
                    url
                ],
                capture_output=True,
                text=True,
                timeout=90
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout
            print(f"Curl error for {url}: {result.stderr}")
            return None
        except subprocess.TimeoutExpired:
            print(f"Curl timeout for {url}")
            return None
        except Exception as e:
            print(f"Curl exception for {url}: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content into BeautifulSoup object."""
        return BeautifulSoup(html, 'html.parser')
    
    def make_absolute_url(self, url: str) -> str:
        """Convert relative URL to absolute URL."""
        if url.startswith('http'):
            return url
        return urljoin(self.news_url, url)
    
    def parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse a date string into a datetime object.
        
        Handles various formats:
        - "28 Nov 2025"
        - "28 November 2025"
        - "Thu 28 Nov 2025"
        - "Published 28 Nov 2025"
        - "Updated Wed 26 Nov 2025"
        """
        if not date_str:
            return None
        
        # Clean up common prefixes
        date_str = re.sub(r'^(Published|Updated|Posted)\s*', '', date_str, flags=re.IGNORECASE)
        date_str = date_str.strip()
        
        try:
            return date_parser.parse(date_str, dayfirst=True)
        except (ValueError, TypeError):
            return None
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @abstractmethod
    def scrape(self) -> List[NewsArticle]:
        """
        Scrape news articles from the council website.
        
        Returns:
            List of NewsArticle objects
        """
        pass
    
    def create_article(
        self,
        title: str,
        url: str,
        date: Optional[datetime] = None,
        excerpt: Optional[str] = None
    ) -> NewsArticle:
        """
        Create a NewsArticle with this scraper's council info.
        
        Args:
            title: Article title
            url: Article URL (will be made absolute)
            date: Publication date
            excerpt: Article excerpt/summary
            
        Returns:
            NewsArticle object
        """
        return NewsArticle(
            council_id=self.council_id,
            council_name=self.council_name,
            title=self.clean_text(title),
            url=self.make_absolute_url(url),
            date=date,
            excerpt=self.clean_text(excerpt) if excerpt else None
        )


class CardScraper(BaseScraper):
    """
    Generic scraper for card-based news layouts.
    
    Most Victorian council websites use a similar pattern:
    - News items displayed as cards in a list/grid
    - Each card has title, date, excerpt, and link
    - Pagination via ?page=N query parameter
    
    This scraper can be configured for different HTML structures
    by overriding the selector methods.
    """
    
    # CSS selectors - override these in subclasses for different structures
    # Note: Some sites wrap entire cards in <a> tags (e.g., a.card--news, a.card__news-listing)
    # Note: div.card with a > .card__title is common GovCMS pattern (Golden Plains, etc)
    ARTICLE_SELECTOR = 'article, .news-item, .news-card, .listing-item, .views-row, .content-card, .article-container, .media-item, a.card--news, a.card__news-listing, a.card[href*="/news/"], div.card'
    TITLE_SELECTOR = 'h2 a, h3 a, .title a, a.title, .field--name-title a, .news-title a, a[href*="/news/"]'
    DATE_SELECTOR = '.date, .published, time, .meta-date, .field--name-created, .news-date'
    EXCERPT_SELECTOR = '.excerpt, .summary, .description, .field--name-body, .teaser, p'
    
    def scrape(self) -> List[NewsArticle]:
        """Scrape news articles from the news page."""
        articles = []
        
        html = self.fetch_page(self.news_url)
        if not html:
            return articles
        
        soup = self.parse_html(html)
        
        # First try structured article elements
        for item in soup.select(self.ARTICLE_SELECTOR):
            article = self._parse_article(item)
            if article:
                articles.append(article)
        
        # If no articles found, try finding news links directly
        if not articles:
            articles = self._scrape_links_directly(soup)
        
        return articles
    
    def _scrape_links_directly(self, soup) -> List[NewsArticle]:
        """
        Fallback scraper that looks for news links directly.
        
        Looks for links that match common news URL patterns.
        """
        articles = []
        seen_urls = set()
        
        # Common news URL patterns
        news_patterns = ['/news/', '/media-release', '/latest-news/', '/newsroom/']
        
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Skip if no text or too short (but allow longer titles)
            if not text or len(text) < 15:
                continue
            
            # Skip if text looks like a date only
            if re.match(r'^(Published|Updated)?\s*\d', text):
                continue
            
            # Check if URL matches news patterns
            if not any(pattern in href.lower() for pattern in news_patterns):
                continue
            
            # Skip pagination, category, and tag links
            if '?page=' in href or '/category/' in href or '/tag/' in href:
                continue
            
            # Skip links that are just the news index
            if href.rstrip('/').endswith('/news'):
                continue
            
            url = self.make_absolute_url(href)
            
            # Skip duplicates
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            # Try to find date near the link
            date = None
            parent = link.find_parent()
            if parent:
                # Look for date text in parent or siblings
                date_text = parent.get_text()
                date_match = re.search(
                    r'(\d{1,2}\s+\w+\s+\d{4}|\w+\s+\d{1,2},?\s+\d{4})',
                    date_text
                )
                if date_match:
                    date = self.parse_date(date_match.group(1))
            
            article = self.create_article(text, url, date)
            articles.append(article)
        
        return articles
    
    def _parse_article(self, item) -> Optional[NewsArticle]:
        """Parse a single article item from the page."""
        title = None
        url = None
        date = None
        excerpt = None
        
        # Strategy 0: Card div with link inside containing .card__title (Golden Plains/GovCMS pattern)
        # Structure: div.card > a > div.card__title > h2
        if item.name == 'div' and 'card' in item.get('class', []):
            card_link = item.select_one('a[href*="/news/"]')
            if card_link:
                url = card_link.get('href', '')
                # Look for title in card__title div
                title_elem = item.select_one('.card__title h2, .card__title h3, .card__title')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    # Get date from card__date or time element
                    date_elem = item.select_one('.card__date time, .card__date, time[datetime]')
                    if date_elem:
                        datetime_attr = date_elem.get('datetime')
                        if datetime_attr:
                            date = self.parse_date(datetime_attr)
                        else:
                            date = self.parse_date(date_elem.get_text(strip=True))
                    # Get excerpt if present (some card layouts have it)
                    excerpt_elem = item.select_one('.card__excerpt, .card__summary, .card__description')
                    if excerpt_elem:
                        excerpt = excerpt_elem.get_text(strip=True)
                    if title and url and len(title) >= 10:
                        return self.create_article(title, url, date, excerpt)
        
        # Strategy 0b: Check if the item itself is a link (whole card is clickable)
        if item.name == 'a' and item.get('href'):
            url = item.get('href', '')
            # Look for title inside
            title_elem = item.select_one('h2, h3, h4, .title')
            if title_elem:
                title = title_elem.get_text(strip=True)
            else:
                # Use aria-label if available
                title = item.get('aria-label', '')
            
            if title and url and len(title) >= 10:
                # Find date
                date_elem = item.select_one(self.DATE_SELECTOR)
                if date_elem:
                    date = self.parse_date(date_elem.get_text(strip=True))
                
                # Find excerpt
                excerpt_elem = item.select_one('.preview, .excerpt, .summary, .description, p')
                if excerpt_elem:
                    excerpt = excerpt_elem.get_text(strip=True)
                
                return self.create_article(title, url, date, excerpt)
        
        # Strategy 0.5: Title NOT in link, but separate "Read more" link exists
        # Common in GovCMS sites like Latrobe (.teaser__title + .read-more link)
        title_elem = item.select_one('.teaser__title, h3.teaser__title')
        if title_elem:
            title_text = title_elem.get_text(strip=True)
            # Look for read-more or similar link
            read_more = item.select_one('a.read-more-overlay-visible, a.read-more, a[href*="/news-and-media/"], a[href*="/media-release"]')
            if read_more and title_text and len(title_text) >= 10:
                url = read_more.get('href', '')
                if url:
                    title = title_text
                    # Find date
                    date_elem = item.select_one('.teaser__info, .node-post-date, ' + self.DATE_SELECTOR)
                    if date_elem:
                        date = self.parse_date(date_elem.get_text(strip=True))
                    # Find excerpt
                    excerpt_elem = item.select_one('.teaser__summary, .field--name-body')
                    if excerpt_elem:
                        excerpt = excerpt_elem.get_text(strip=True)
                    return self.create_article(title, url, date, excerpt)
        
        # Strategy 1: Look for specific title class patterns (most reliable)
        # First check for heading elements inside - Cardinia-style (listing__link wraps h2 + p)
        title_elem = item.select_one('h2.listing__heading, h3.listing__heading, .listing__heading')
        if title_elem:
            title = title_elem.get_text(strip=True)
            # URL is on the parent link
            parent_link = title_elem.find_parent('a')
            if parent_link and parent_link.get('href'):
                url = parent_link.get('href', '')
                # Get excerpt from sibling summary element
                excerpt_elem = item.select_one('p.listing__summary, .listing__summary')
                if excerpt_elem:
                    excerpt = excerpt_elem.get_text(strip=True)
                # Get date from listing__meta
                date_elem = item.select_one('.listing__meta--date, .listing__meta')
                if date_elem:
                    date = self.parse_date(date_elem.get_text(strip=True))
                if title and url and len(title) >= 10:
                    return self.create_article(title, url, date, excerpt)
        
        title_elem = item.select_one('a.views-field-title, .title a, a.title, h2 a, h3 a, .field--name-title a, .news-title a')
        
        # Strategy 2: If not found, look for link with longest text (usually the title)
        if not title_elem:
            links = item.find_all('a', href=True)
            best_link = None
            best_length = 0
            for link in links:
                text = link.get_text(strip=True)
                href = link.get('href', '')
                # Skip links that look like dates
                if re.match(r'^(Published|Updated)?\s*\d', text):
                    continue
                # Skip category/tag links
                if '/category/' in href or '/tag/' in href or '?category=' in href:
                    continue
                # Skip pagination
                if '?page=' in href:
                    continue
                # Prefer links with news URL pattern
                if ('/news/' in href or '/news-and-media/' in href) and len(text) > best_length:
                    best_link = link
                    best_length = len(text)
                elif not best_link and len(text) > best_length:
                    best_link = link
                    best_length = len(text)
            title_elem = best_link
        
        if not title_elem:
            return None
        
        title = title_elem.get_text(strip=True)
        url = title_elem.get('href', '')
        
        if not title or not url or len(title) < 10:
            return None
        
        # Find date - look in various places
        # First check for time element (most accurate)
        time_elem = item.select_one('time[datetime]')
        if time_elem:
            datetime_attr = time_elem.get('datetime')
            if datetime_attr:
                date = self.parse_date(datetime_attr)
        
        # Fallback to date selectors
        if not date:
            date_elem = item.select_one(self.DATE_SELECTOR)
            if date_elem:
                date = self.parse_date(date_elem.get_text(strip=True))
        
        # Find excerpt
        excerpt_elem = item.select_one('a.views-field-body, .excerpt, .summary, .description, .field--name-body, .teaser')
        if excerpt_elem and excerpt_elem != title_elem:
            excerpt = excerpt_elem.get_text(strip=True)
        
        return self.create_article(title, url, date, excerpt)
