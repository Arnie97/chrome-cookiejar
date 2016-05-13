import http.cookiejar
import os
import shutil
import sqlite3
import tempfile


class ChromeCookieJar(http.cookiejar.CookieJar):
    'Create CookieJar instances from database of Google Chrome.'

    def __init__(self, cookie_file_path, domain_filter='%', policy=None):
        super().__init__(policy)
        dummy = {key: None for key in (
            'port', 'port_specified', 'domain_specified', 'domain_initial_dot',
            'path_specified', 'discard', 'comment', 'comment_url', 'rest'
        )}

        with sqlite3.connect(cookie_file_path) as conn:
            conn.row_factory = lambda cursor, row: {
                col[0]: row[idx] for idx, col in enumerate(cursor.description)
            }
            sql = '''
                select
                    host_key as domain, name, value,
                    path, expires_utc as expires, secure
                from cookies
                where host_key like ?
            '''
            for row in conn.execute(sql, [domain_filter]):
                cookie_item = http.cookiejar.Cookie(**row, **dummy, version=0)
                self.set_cookie(cookie_item)


try:
    temp_path = tempfile.mkstemp()[1]
    cookie_path = os.path.join(
        os.environ['LOCALAPPDATA'],
        'Google/Chrome/User Data/Default/Cookies'
    )
    shutil.copyfile(cookie_path, temp_path)
    cookies = ChromeCookieJar(temp_path)
    os.remove(temp_path)

except FileNotFoundError:
    print('Chrome installation not found.')
