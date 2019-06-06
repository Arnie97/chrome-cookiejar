#!/usr/bin/env python3

import os
import re
import requests
import shutil
from chrome import ChromeCookieJar


def get_cookiejar(domain_filter='%'):
    'Copy the cookies, so that it could be read while Chrome is open.'
    cookie_file_path = os.path.join(
        os.environ['LOCALAPPDATA'],
        'Google/Chrome/User Data/Default/Cookies'
    )
    shutil.copyfile(cookie_file_path, 'Cookies')
    return ChromeCookieJar('Cookies', domain_filter)


def test_github():
    'Print current logged-in GitHub user.'
    jar = get_cookiejar('%github.com')
    response = requests.get('https://github.com', cookies=jar)
    login_user = re.compile(r'<meta name="user-login" content="(.+?)">')
    match = login_user.search(response.text)
    if match:
        print('GitHub login user:', match.group(1))
    else:
        print('GitHub not logged in')


if __name__ == '__main__':
    test_github()
