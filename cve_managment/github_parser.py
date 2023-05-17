"""git_link = "https://github.com/trickest/cve"

total_list = "https://raw.githubusercontent.com/trickest/cve/main/references.txt"

example = "https://github.com/trickest/cve/tree/main/2023"
'https://github.com/trickest/cve/tree/main/1999'


page = requests.get(url).text
soup = bs4.BeautifulSoup(page)
soup.prettify()
for anchor in soup.findAll('a', {"class": "Link--primary"}, href=True):
	print(anchor['href'])
	#if not "commits" in anchor['href']:
		#page2 = requests.get("https://raw.githubusercontent.com"+anchor['href'].replace("/blob", "")).text
		#print(page2)
		#print("https://raw.githubusercontent.com"+anchor['href'])
	

	#soup2 = bs4.BeautifulSoup(page2)
	#print(soup2.findAll('a', href=True)[0])
"""

import requests
import bs4

url = 'https://github.com/trickest/cve/tree/main/'


def get_by_id(ids):
	#CVE-2021-31239
	parts = ids.split('-')
	url_builder = f"{parts[1]}/{ids}.md"
	#print(url_builder)
	#print("https://raw.githubusercontent.com/trickest/cve/main/"+url_builder.replace("/blob", ""))
	page2 = requests.get("https://raw.githubusercontent.com/trickest/cve/main/"+url_builder.replace("/blob", "")).text
	#print(page2)
	return page2
	


"""
2021/CVE-2021-31239.md
https://raw.githubusercontent.com/trickest/cve/main/2021/CVE-2021-31239.md
### [CVE-2021-31239](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-31239)
![](https://img.shields.io/static/v1?label=Product&message=n%2Fa&color=blue)
![](https://img.shields.io/static/v1?label=Version&message=n%2Fa&color=blue)
![](https://img.shields.io/static/v1?label=Vulnerability&message=n%2Fa&color=brighgreen)

### Description

An issue found in SQLite SQLite3 v.3.35.4 that allows a remote attacker to cause a denial of service via the appendvfs.c function.

### POC

#### Reference
- https://www.sqlite.org/forum/forumpost/d9fce1a89b

#### Github
No PoCs found on GitHub currently.
"""