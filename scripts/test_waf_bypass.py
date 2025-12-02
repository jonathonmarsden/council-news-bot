import requests
from curl_cffi import requests as curl_requests
import time

URLS = [
    ("City of Ballarat", "https://www.ballarat.vic.gov.au/news"),
    ("Bass Coast", "https://www.basscoast.vic.gov.au/about-council/news-listing"),
    ("Blue Mountains", "https://www.bmcc.nsw.gov.au/media-centre"),
    ("Burwood", "https://www.burwood.nsw.gov.au/News-Media"),
    ("Brisbane", "https://www.brisbane.qld.gov.au/about-council/council-information-and-rates/news-and-publications/living-in-brisbane-newsletter"),
    ("Gold Coast", "https://www.goldcoast.qld.gov.au/Council/City-news"),
    ("Cumberland", "https://www.cumberland.nsw.gov.au/media-releases"),
    ("Liverpool", "https://www.liverpool.nsw.gov.au/council/news"),
    ("Parramatta", "https://www.cityofparramatta.nsw.gov.au/about-parramatta/news"),
    ("Ryde", "https://www.ryde.nsw.gov.au/Council/News-and-Media"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def test_requests(name, url):
    try:
        start = time.time()
        resp = requests.get(url, headers=HEADERS, timeout=10)
        duration = time.time() - start
        print(f"  [Requests] Status: {resp.status_code}, Length: {len(resp.content)}, Time: {duration:.2f}s")
        return resp.status_code
    except Exception as e:
        print(f"  [Requests] Error: {str(e)[:50]}...")
        return 0

def test_curl_cffi(name, url):
    try:
        start = time.time()
        resp = curl_requests.get(url, impersonate="chrome110", timeout=10)
        duration = time.time() - start
        print(f"  [CurlCFFI] Status: {resp.status_code}, Length: {len(resp.content)}, Time: {duration:.2f}s")
        return resp.status_code
    except Exception as e:
        print(f"  [CurlCFFI] Error: {str(e)[:50]}...")
        return 0

print(f"Testing {len(URLS)} URLs for WAF bypass potential...\n")

for name, url in URLS:
    print(f"--- {name} ---")
    print(f"URL: {url}")
    
    req_status = test_requests(name, url)
    curl_status = test_curl_cffi(name, url)
    
    if req_status in [403, 406, 503] and curl_status == 200:
        print(f"✅ SUCCESS: curl_cffi bypassed WAF for {name}!")
    elif req_status == 200 and curl_status == 200:
        print(f"ℹ️ INFO: Both methods worked. WAF might not be the issue.")
    elif curl_status != 200:
        print(f"❌ FAIL: curl_cffi also failed.")
    
    print("")
