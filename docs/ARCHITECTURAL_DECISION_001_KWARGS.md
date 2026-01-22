# Critical Architecture Fix: Scraper Initialization
**Date**: 22 January 2026

## The Incident
On this date, it was discovered that the production bot was failing silently (in terms of output) but loudly (in non-fatal logs) for dozens of councils. The logs showed:
`TypeError: __init__() got an unexpected keyword argument 'enabled'`

## The Cause
The `ScraperFactory` was refactored previously to be more "helpful", passing any configuration key found in `councils.json` that wasn't strictly reserved (like `id` or `scraper`) to the target Scraper class via `**extra_kwargs`.

However, many Scraper classes (specifically `CardScraper`, `RSSScraper`, `CatalystScraper` and WA custom scrapers) had manual `__init__` signatures that did **not** include `**kwargs`.

When a council config file had an extra key—commonly `enabled: true` (which is used by the loader but still passed down) or metadata keys—the Scraper class would reject it and crash during instantiation.

## The Fix
All Scraper classes have been updated to include `**kwargs` in their `__init__` signature and pass it to `super().__init__(..., **kwargs)`.

## The New Rule
**EVERY Scraper class implementation must accept `**kwargs` in its `__init__` method.**

### Incorrect
```python
class MyScraper(BaseScraper):
    def __init__(self, council_id, council_name, news_url):
        super().__init__(council_id, council_name, news_url)
```

### Correct
```python
class MyScraper(BaseScraper):
    def __init__(self, council_id, council_name, news_url, **kwargs):
        super().__init__(council_id, council_name, news_url, **kwargs)
        # Handle specific args if needed, ignore the rest
```
