# Bluesky Bookmarks API Discovery

## Overview
The Bluesky/AT Protocol does not publicize a standard "Bookmarks" XRPC endpoint in its main documentation, as bookmarks are often treated as private client-side state or PDS-specific implementations. However, probing reveals a working endpoint on `bsky.social`.

## Authentication
Requires a standard Access Token (JWT) from `com.atproto.server.createSession`.

## Endpoint: Get Bookmarks
**URL**: `https://bsky.social/xrpc/app.bsky.bookmark.getBookmarks`
**Method**: `GET`
**Headers**: `Authorization: Bearer <access_jwt>`

### Response Structure
The response is a JSON object containing a list of bookmarked posts.

```json
{
  "cursor": "3mcy...", 
  "bookmarks": [
    {
      "createdAt": "2026-01-22T05:08:19.591Z",
      "subject": {
        "uri": "at://did:plc:...", 
        "cid": "..."
      },
      "item": {
        "uri": "at://did:plc:6u23fosnrkbujn5xwuc2wywi/app.bsky.feed.post/3mcyg2enwdj25",
        "cid": "bafyreigbgzobukfgqtpx4zg2gg3ab7rby6pnexdqmsrchdsh3mxv2opbki",
        "author": {
          "did": "did:plc:6u23fosnrkbujn5xwuc2wywi",
          "handle": "roundupnewsbotwa.bsky.social",
          "displayName": "LG News Roundup WA feed",
          "avatar": "..."
        },
        "record": {
          "$type": "app.bsky.feed.post",
          "createdAt": "2026-01-22T05:06:25.567518+00:00",
          "text": "© 2025 Shire of Katanning\n05 December 2025\nShire of Katanning\n#LGNewsRoundup #WALGA #WACouncils #ShireOfKatanning",
          "facets": [...]
        },
        "viewer": {
          "bookmarked": true,
          "threadMuted": false,
          "embeddingDisabled": false
        }
      }
    }
  ]
}
```

### Key Fields
- `bookmarks`: Array of bookmark objects.
- `item.uri`: The AT URI of the original post (needed for deletion/editing).
- `item.cid`: Content ID (needed for safe updates).
- `item.record.text`: The text content of the post (to check for malformation).
- `item.author.handle`: The bot that posted it (useful if managing multiple accounts).
- `cursor`: Pagination cursor for fetching more bookmarks.

## Workflow Integration
To use this for the "Malformed Post Correction" system:
1. **Admin User** manually bookmarks a bad post in the Bluesky app.
2. **Bot Script** polls `app.bsky.feed.getBookmarks`.
3. **Bot Script** identifies the bookmarked post.
4. **Bot Script** performs correction (e.g., delete and repost, or sophisticated rewrite).
5. **Bot Script** unbookmarks the post to clear the queue.

*Note: The "Unbookmark" mutation endpoint needs to be confirmed. It is likely a `deleteRecord` on a specific collection, or the API might interpret a `delete` on the bookmark view.*
