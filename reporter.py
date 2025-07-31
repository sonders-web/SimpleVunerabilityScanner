def report(vulns):
    if not vulns:
        print("\n[✓] No vulnerabilities found.")
        return

    print("\n=== Vulnerability Report ===")
    for v in vulns:
        print(f"""
[!] Type:     {v['type']}
    URL:      {v['url']}
    Payload:  {v['payload']}
""")
