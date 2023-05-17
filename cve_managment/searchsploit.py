import requests
import cve_searchsploit
import sys

HIGH_CVSS_BOUND = 7.0

cve_searchsploit.update_db()

vendor = "google"
product = "chrome"

r = requests.get("https://cve.circl.lu/api/search/%s/%s" % (vendor, product))
vulns = r.json()

exploits = set()
cve_with_exploits = 0

for v in vulns:
    if "cvss" not in v or float(v["cvss"]) < HIGH_CVSS_BOUND:
        continue

    ids = cve_searchsploit.edbid_from_cve(v["id"])
    for i in ids:
        exploits.add(i)
    if len(ids) > 0:
        cve_with_exploits += 1
        print("", v["id"], ":", ids)

print()
print(" Number of severe CVEs with an exploit in ExploitDB:", cve_with_exploits)
print(" Number of public severe exploits for Chrome in ExploitDB:", len(exploits))
print()