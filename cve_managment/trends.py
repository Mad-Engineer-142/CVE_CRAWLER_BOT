import requests
import datetime
import urllib.request, json 
#import config

import re
from bs4 import BeautifulSoup


"""
cve_trends = "https://cvetrends.com/api/cves/"#config.cve_trends_url
#24hrs
#7days



r = requests.get(f"{cve_trends}/24hrs")
container = r.json()
for i in container['data']:
	print(i['cve'])


# parse cvetrends.com--------------------------------------------------------------------------------------------------
def get_top_cve_list():
    link = 'https://cvetrends.com/api/cves/24hrs'
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "lxml")
    regex = re.findall(r'"cve": "CVE-\d{4}-\d{4,8}"', soup.get_text())
    top_cve_list = []
    for item in regex:
        top_cve_list.append(re.search(r'CVE-\d{4}-\d{4,8}', item).group())

    return top_cve_list

#top_cve_list = get_top_cve_list()  # Получение топа cve с cvetrends.com
#print(top_cve_list)

# parse opencve.io---------------------------------------------------------------------------------------------------- 
def parsing_opencve():
    url1 = 'https://www.opencve.io/login/'
    url2 = 'https://www.opencve.io/login'
    csrf_token = ''
    s = requests.Session()
    response = s.get(url1)
    soup = BeautifulSoup(response.text, 'lxml')

    # Get CSRF
    for a in soup.find_all('meta'):
        if 'name' in a.attrs:
            if a.attrs['name'] == 'csrf-token':
                csrf_token = a.attrs['content']

    # Authentication
    s.post(
        url2,
        data={
            'username': 'david20092003@gmail.com',
            'password': PASSWORD,
            'csrf_token': csrf_token,
        },
        headers={'referer': 'https://www.opencve.io/login'},
        verify=False
    )
    # Get new CVE
    cve_line = []
    for page_num in range(1, 20):
        pagination = f'https://www.opencve.io/?page={page_num}'
        resp = s.get(pagination)
        parse = BeautifulSoup(resp.text, 'lxml')
        for cve in parse.find_all('h3', class_='timeline-header'):
            index = cve.text.find('has changed')
            if index == -1:
                cve_line.append(cve.text.replace(' is a new CVE', ''))

    cve_line_no_replic = []
    for item in cve_line:
        if item not in cve_line_no_replic:
            cve_line_no_replic.append(item[:-1])
    return cve_line_no_replic

cve_line = parsing_opencve()  # Получение списка новых cve с сайта opencve.io
print(cve_line)"""