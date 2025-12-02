import requests

url = "https://www.basscoast.vic.gov.au//feeds/news.rss"
try:
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Content Type: {response.headers.get('Content-Type')}")
    print(f"Content Length: {len(response.content)}")
    print("First 500 chars:")
    print(response.text[:500])
except Exception as e:
    print(f"Error: {e}")
