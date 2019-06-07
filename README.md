# Chrome Cookiejar
This module helps to utilize your Chrome cookies in Python scripts.
It's especially useful when scraping sites that requires login,
as you can test your ideas easily without solving the CAPTCHAs and emulating the whole login process.

## Supported platforms
This package is only tested on Python 3.

Please also note that values of cookies are encrypted with platform specific algorithms since Chrome 33.
The decrypt helper for Windows is already included; however, only older versions of Chrome is currently supported on macOS or Linux.

## Get started
Use the following code snippet to create an instance of `http.cookiejar.CookieJar` that includes all cookies from your Chrome browser:

```python
>>> from chrome_cookiejar import ChromeCookieJar
>>> cookiejar = ChromeCookieJar('/path/of/your/Cookies')  # doctest: +SKIP

```

The file path is optional; if omitted, the library will try to read cookies from the default user profile path of Chrom(ium).
If you're not sure, check `chrome://version` and follow the *Profile Path* shown here.

As the `Cookies` file is a SQLite database, you could filter the host domain with SQL wildcards:

```python
>>> import requests, re
>>> jar = ChromeCookieJar(host_filter='%gith_b.com')
>>> login_user = re.compile(r'<meta name="user-login" content="(.+?)">')
>>> login_user.findall(requests.get('https://github.com', cookies=None).text)
[]
>>> login_user.findall(requests.get('https://github.com', cookies=jar).text)
['Arnie97']

```
