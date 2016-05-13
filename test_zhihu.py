#!/usr/bin/env python

import os
import requests
import shutil
from bs4 import BeautifulSoup
from chrome import ChromeCookieJar

shutil.copyfile(
    os.path.join(
        os.environ['LOCALAPPDATA'],
        'Google/Chrome/User Data/Default/Cookies'
    ),
    'Cookies'
)

jar = ChromeCookieJar('Cookies', '%zhihu.com')
response = requests.get(
    'https://www.zhihu.com/question/following', cookies=jar, verify=False
)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.find('span', class_='name').text)
for item in soup.find_all('a', class_='question_link'):
    print(item.text)
