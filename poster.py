"""
BlueSky posting functionality for Council News Bot.

Handles authentication and posting news articles to BlueSky.
"""

import os
import re
from datetime import datetime
from typing import Optional, List, Dict, Any

from atproto import Client, models


class BlueSkyPoster:
    """Posts council news articles to BlueSky."""
    
    # Maximum post length for BlueSky
    MAX_POST_LENGTH = 300
    
    def __init__(self, handle: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the BlueSky poster.
        
        Args:
            handle: BlueSky handle (defaults to BLUESKY_HANDLE env var)
            password: BlueSky app password (defaults to BLUESKY_PASSWORD env var)
        """
        self.handle = handle or os.environ.get('BLUESKY_HANDLE')
        self.password = password or os.environ.get('BLUESKY_PASSWORD')
        self.client = None
        self._authenticated = False
    
    def authenticate(self) -> bool:
        """
        Authenticate with BlueSky.
        
        Returns:
            True if authentication successful, False otherwise
        """
        if not self.handle or not self.password:
            print("Error: BlueSky credentials not configured")
            return False
        
        try:
            self.client = Client()
            self.client.login(self.handle, self.password)
            self._authenticated = True
            print(f"Authenticated as {self.handle}")
            return True
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def post_article(self, council_name: str, title: str, url: str, 
                     date: Optional[datetime] = None, excerpt: Optional[str] = None) -> bool:
        """
        Post a news article to BlueSky.
        
        Args:
            council_name: Name of the council
            title: Article title
            url: Article URL
            date: Publication date (optional)
            excerpt: Article excerpt/subtitle (optional)
            
        Returns:
            True if posted successfully, False otherwise
        """
        if not self._authenticated:
            if not self.authenticate():
                return False
        
        # Format the post text and get facets for clickable links
        post_text, facets = self._format_post_with_facets(council_name, title, url, date, excerpt)
        
        try:
            self.client.send_post(text=post_text, facets=facets)
            print(f"Posted: {title[:50]}...")
            return True
        except Exception as e:
            print(f"Failed to post: {e}")
            return False
    
    def _council_to_hashtag(self, council_name: str) -> str:
        """
        Convert council name to hashtag format.
        
        E.g., "Cardinia Shire Council" -> "#CardiniaShireCouncil"
        """
        # Remove special characters and spaces, keep alphanumeric
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', council_name)
        # Convert to PascalCase by capitalizing each word and joining
        words = cleaned.split()
        hashtag = ''.join(word.capitalize() for word in words)
        return f"#{hashtag}"
    
    def _format_post_with_facets(self, council_name: str, title: str, url: str,
                                  date: Optional[datetime] = None, 
                                  excerpt: Optional[str] = None) -> tuple:
        """
        Format a post for BlueSky with clickable link facets.
        
        The title on the first line will be clickable, linking to the article URL.
        
        Format:
        [Title - clickable link to article]
        [Excerpt if exists]
        [Council Name]
        Published: [Date]
        #LGNewsRoundup #VLGA #VicCouncils #CouncilHashtag
        
        Args:
            council_name: Name of the council
            title: Article title
            url: Article URL
            date: Publication date (optional)
            excerpt: Article excerpt/subtitle (optional)
            
        Returns:
            Tuple of (post_text, facets_list)
        """
        # Build hashtags - new order: #LGNewsRoundup #VLGA #VicCouncils #CouncilName
        council_hashtag = self._council_to_hashtag(council_name)
        hashtags = f"#LGNewsRoundup #VLGA #VicCouncils {council_hashtag}"
        
        # Format date
        if date:
            date_str = date.strftime("%d %B %Y")
        else:
            date_str = datetime.now().strftime("%d %B %Y")
        
        # Start with title - we'll track its position for the link facet
        working_title = title
        
        # Build post parts in new order:
        # 1. Title (clickable)
        # 2. Excerpt (optional)
        # 3. Council Name
        # 4. Published date
        # 5. Hashtags
        
        parts = [working_title]
        
        # Add excerpt if it exists and is meaningful
        include_excerpt = excerpt and len(excerpt) > 10
        if include_excerpt:
            parts.append(excerpt)
        
        parts.append(council_name)
        parts.append(f"Published: {date_str}")
        parts.append(hashtags)
        
        # Join with newlines
        post = "\n".join(parts)
        
        # If too long, truncate excerpt first, then title
        if len(post) > self.MAX_POST_LENGTH:
            # Try without excerpt
            include_excerpt = False
            parts_no_excerpt = [
                working_title,
                council_name,
                f"Published: {date_str}",
                hashtags,
            ]
            post = "\n".join(parts_no_excerpt)
        
        if len(post) > self.MAX_POST_LENGTH:
            # Truncate title
            overhead = len(post) - len(working_title)
            available = self.MAX_POST_LENGTH - overhead - 3
            working_title = title[:available] + "..."
            parts_truncated = [
                working_title,
                council_name,
                f"Published: {date_str}",
                hashtags,
            ]
            post = "\n".join(parts_truncated)
        
        # Create facet for the title link (first line)
        # Byte positions are needed for facets
        title_bytes = working_title.encode('utf-8')
        title_byte_end = len(title_bytes)
        
        facets = [
            models.AppBskyRichtextFacet.Main(
                index=models.AppBskyRichtextFacet.ByteSlice(
                    byte_start=0,
                    byte_end=title_byte_end,
                ),
                features=[
                    models.AppBskyRichtextFacet.Link(uri=url)
                ],
            )
        ]
        
        return post, facets
    
    def _format_post(self, council_name: str, title: str, url: str,
                     date: Optional[datetime] = None, excerpt: Optional[str] = None) -> str:
        """
        Format a post for BlueSky (plain text, no facets).
        
        Used for previewing posts.
        """
        post, _ = self._format_post_with_facets(council_name, title, url, date, excerpt)
        return post
    
    def test_connection(self) -> bool:
        """
        Test the BlueSky connection without posting.
        
        Returns:
            True if connection successful, False otherwise
        """
        return self.authenticate()
