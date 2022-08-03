import requests
from lxml import html
from urllib.parse import urlparse

def get_urls_from_string(page_content,base_url):
    ans = []
    tree = html.fromstring(page_content)
    tree.make_links_absolute(base_url = base_url)
    for elem in tree.iter():
        if elem.tag == "a":
            ans.append(elem.get("href"))
    return ans

def normalize_url(url):
    urlObj = urlparse(url)
    ans = urlObj.netloc+urlObj.path
    ans = ans.lower()
    if ans[(len(ans)-1)] == '/':
        ans = ans[:-1]
    return ans

def crawl_page(base_url,current_url,pages):
    normalized_url = normalize_url(current_url)
    if normalized_url not in pages:
        pages[normalized_url] = 0

    if urlparse(base_url).netloc != urlparse(current_url).netloc:
        pages[normalized_url] = None

    if pages[normalized_url] is None:
        return pages
    
    if pages[normalized_url] > 0:
        pages[normalized_url] += 1
        return pages
    
    res = requests.get(current_url)
    try:
        validate_response(res,current_url)
    except Exception as e:
        print(e)
        pages[normalized_url] = None
        return pages

    pages[normalized_url] += 1
    urls = get_urls_from_string(res.content,base_url)
    for url in urls:
        crawl_page(base_url,url,pages)

    return pages
    

def validate_response(resp,url):
    if resp.status_code != 200:
        raise Exception("'"+url+"' didn't result in a 200 response code")
    if "text/html" not in resp.headers["content-type"].lower():
        raise Exception("Didn't result in an HTML response")