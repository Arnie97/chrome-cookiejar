import os
import sys


def find_cookies_path() -> str:
    'Find the cookies database in default locations.'
    paths = DEFAULT_LOCATIONS.get(sys.platform, DEFAULT_LOCATIONS['linux'])
    for path in paths:
        file_path = os.path.join(os.path.expandvars(path), 'Cookies')
        if os.path.isfile(file_path):
            return file_path
    raise FileNotFoundError(
        'Cookies not found in the default locations. '
        'Please specify the path to the Cookies database.'
    )


DEFAULT_LOCATIONS = {
    'win32': [
        '%LOCALAPPDATA%/Google/Chrome/User Data/Default',
    ],
    'darwin': [
        '$HOME/Library/Application Support/Google/Chrome/Default',
        '$HOME/Library/Application Support/Chromium/Default',
    ],
    'linux': [
        '$HOME/.config/google-chrome/Default',
        '$HOME/.config/chromium/Default',
    ],
}
