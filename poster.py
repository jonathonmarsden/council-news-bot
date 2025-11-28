"""
BlueSky posting functionality for Council News Bot.

Handles authentication and posting news articles to BlueSky.
"""

import os
from typing import Optional

from atproto import Client


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
    
    def post_article(self, council_name: str, title: str, url: str) -> bool:
        """
        Post a news article to BlueSky.
        
        Args:
            council_name: Name of the council
            title: Article title
            url: Article URL
            
        Returns:
            True if posted successfully, False otherwise
        """
        if not self._authenticated:
            if not self.authenticate():
                return False
        
        # Format the post text
        post_text = self._format_post(council_name, title, url)
        
        try:
            self.client.send_post(text=post_text)
            print(f"Posted: {title[:50]}...")
            return True
        except Exception as e:
            print(f"Failed to post: {e}")
            return False
    
    def _format_post(self, council_name: str, title: str, url: str) -> str:
        """
        Format a post for BlueSky.
        
        Format: "📰 [Council Name]: [Title] [URL]"
        Truncates title if necessary to fit within character limit.
        
        Args:
            council_name: Name of the council
            title: Article title
            url: Article URL
            
        Returns:
            Formatted post text
        """
        # Base format with emoji and council name
        prefix = f"📰 {council_name}: "
        suffix = f" {url}"
        
        # Calculate available space for title
        available_length = self.MAX_POST_LENGTH - len(prefix) - len(suffix)
        
        # Truncate title if needed
        if len(title) > available_length:
            title = title[:available_length - 3] + "..."
        
        return f"{prefix}{title}{suffix}"
    
    def test_connection(self) -> bool:
        """
        Test the BlueSky connection without posting.
        
        Returns:
            True if connection successful, False otherwise
        """
        return self.authenticate()
