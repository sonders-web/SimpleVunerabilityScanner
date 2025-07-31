from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse

visited = set()

def is_internal_link(link, base_domain):
    return base_domain in urlparse(link).netloc or urlparse(link).netloc == ""

def crawl(url, base_domain, depth=2):
    if depth == 0 or url in visited:
        return set()

    print(f"[+] Crawling: {url}")
    visited.add(url)
    found_links = set()

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup.find_all("a", href=True):
            raw_href = tag['href']
            full_url = urljoin(url, raw_href)
            if is_internal_link(full_url, base_domain):
                if full_url not in visited:
                    found_links.add(full_url)
    except requests.RequestException as e:
        print(f"[!] Failed to crawl {url}: {e}")

    all_links = set()
    for link in found_links:
        all_links.update(crawl(link, base_domain, depth - 1))

    return visited.union(all_links)
