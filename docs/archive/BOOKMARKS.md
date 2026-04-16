# Bluesky Bookmark API & Maintenance Tool

## Overview

This document details the "off-protocol" Bluesky Bookmark API endpoints discovered and used in the `council-news-bot` project. These endpoints are not currently documented in the official `atproto` Python SDK or the main Bluesky API documentation, but they are essential for building tools that interact with a user's bookmarks.

We use these endpoints in `scripts/fix_and_repost.py` to create a maintenance workflow:
1.  **User Action**: The user bookmarks a broken or malformed post (e.g., duplicate, bad formatting, wrong link) in the Bluesky app.
2.  **Tool Action**: The script fetches these bookmarks.
3.  **Resolution**: The script identifies the original council and article, re-scrapes the data to fix the issue, reposts the corrected version, and deletes the old broken post and the bookmark.

## API Endpoints

These endpoints are accessed via XRPC. In the `atproto` Python library, we use `client.invoke_query` and `client.invoke_procedure`.

### 1. Get Bookmarks

*   **Type**: Query (`invoke_query`)
*   **NSID**: `app.bsky.bookmark.getBookmarks`
*   **Parameters**:
    *   `limit` (int): Number of bookmarks to fetch (default/max seems to be 100).
    *   `cursor` (string, optional): Pagination cursor returned from previous response.
*   **Response Structure**:
    ```json
    {
      "cursor": "...",
      "bookmarks": [
        {
          "uri": "at://did:plc:.../app.bsky.bookmark/...",
          "subject": {
            "uri": "at://did:plc:.../app.bsky.feed.post/...",
            "cid": "..."
          },
          "indexedAt": "...",
          "item": {
             // The full post view (record, author, embed, etc.)
             // If the post is deleted, this might be missing or contain "notFound": true
          }
        }
      ]
    }
    ```

### 2. Delete Bookmark

*   **Type**: Procedure (`invoke_procedure`)
*   **NSID**: `app.bsky.bookmark.deleteBookmark`
*   **Headers**: `Content-Type: application/json` (CRITICAL: The call will fail with `InvalidRequest` without this header).
*   **Input Data**:
    ```json
    {
      "uri": "at://did:plc:.../app.bsky.feed.post/..." 
    }
    ```
    *Note: The `uri` here is the **Post URI** (the subject), not the bookmark record URI.*

## Implementation Details (`scripts/fix_and_repost.py`)

### The `ParamsModel` Workaround

The `atproto` library's `_invoke` method expects input parameters to be Pydantic models (or objects with a `model_dump` method). Since we are calling undocumented endpoints, we don't have pre-generated models. We use a simple wrapper class to satisfy this requirement:

```python
class ParamsModel:
    def __init__(self, data):
        self.data = data
    def model_dump(self, exclude_none=True, by_alias=True):
        return self.data
    def model_dump_json(self, exclude_none=True, by_alias=True):
        import json
        return json.dumps(self.data)
```

### Workflow Logic

1.  **Authentication**: Logs in as the "Debug User" (the human operator) to fetch bookmarks, and initializes "Bot Users" (VIC/NSW/QLD) as needed to repost.
2.  **Fetching**: Iterates through bookmark pages using the cursor.
3.  **Orphan Detection**: Checks if `item.notFound` is true. If so, the post was already deleted. The script automatically deletes these "orphaned" bookmarks to clean up the list.
4.  **Council Identification**:
    *   Attempts to identify the council from the post text.
    *   Falls back to matching the domain of the linked article against the known council news URLs.
5.  **Re-scraping**:
    *   Initializes the specific scraper for that council.
    *   Fetches the current news feed.
    *   Matches the bookmarked article URL against the fresh scrape.
6.  **Fix & Repost**:
    *   If a match is found, uses the *fresh* data (correct title, excerpt, etc.) to create a new post via the appropriate Bot account.
    *   Deletes the old broken post.
    *   Deletes the bookmark.

## Usage

Run the script manually when you have bookmarked posts to fix:

```bash
python3 scripts/fix_and_repost.py
```
