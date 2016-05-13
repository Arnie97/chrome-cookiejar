#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from chrome import ChromeCookieJar

jar = ChromeCookieJar('Cookies', '%zhihu.com')
response = requests.get('https://www.zhihu.com', cookies=jar, verify=False)
soup = BeautifulSoup(response.text)
print(soup.find('span', attrs={'class': 'name'}).text)
