# Chrome Cookies
This module helps to utilize your Chrome cookies in Python scripts.
It's especially useful when scraping sites that requires login,
as you can test your ideas easily without having to recognize the captchas and emulate the whole login process first.

## Supported platforms
This package is only tested on Python 3.

Please also note that values of cookies are encrypted with platform specific algorithms since Chrome 33.
The decrypt helper for Windows is already included; however, only older versions of Chrome is currently supported on macOS or Linux.

## Get started
First, you need to locate your `Cookies` file.
By default, the path is `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cookies` for Windows, `~/.config/google-chrome/Default` for Linux and `~/Library/Application Support/Google/Chrome/Default/Cookies` for macOS.
If in doubt, you can always navigate to *chrome://version* and follow the *Profile Path* shown here.

To avoid problems, it's recommended to exit your Chrome or use a copy of the file.

Use the following snippet of code to create an instance of `http.cookiejar.CookieJar` including all cookies from your chrome:

```python
from chrome import ChromeCookieJar
cookiejar = ChromeCookieJar(path_of_your_cookies_file)
```

As the `Cookies` file is a SQLite database, you can optionally filter the domain of cookies with SQL wildcards:

```python
from chrome import ChromeCookieJar
cookiejar = ChromeCookieJar(path_of_your_cookies_file, '%github.com')
```
