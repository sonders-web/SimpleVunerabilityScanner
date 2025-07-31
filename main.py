from crawler import crawl
from scanner import test_sql_injection, test_xss_forms
from reporter import report
from urllib.parse import urlparse

target_url = input("Enter target URL (e.g., http://testphp.vulnweb.com): ")
domain = urlparse(target_url).netloc
pages = crawl(target_url, domain)

vulns = []

for page in pages:
    sqli_results = test_sql_injection(page)
    for url, payload in sqli_results:
        vulns.append({"type": "SQL Injection", "url": url, "payload": payload})

    xss_results = test_xss_forms(page)
    for url, payload in xss_results:
        vulns.append({"type": "XSS", "url": url, "payload": payload})

report(vulns)
