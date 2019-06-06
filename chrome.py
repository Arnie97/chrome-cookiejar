import datetime
import http.cookiejar
import sqlite3
from win32crypt import CryptUnprotectData


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

            # Chrome encrypts cookie values since version 33
            sql = 'pragma table_info("cookies")'
            encrypted = any(
                field['name'] == 'encrypted_value'
                for field in conn.execute(sql)
            )

            sql = '''
                select
                    host_key as domain, name, value, %s
                    path, expires_utc, is_secure as secure
                from cookies
                where host_key like ?
            ''' % ('encrypted_value,' if encrypted else '')

            for row in conn.execute(sql, [domain_filter]):
                row['expires'] = webkit_timestamp_to_unix(row.pop('expires_utc'))
                if encrypted:
                    cipher_blob = row.pop('encrypted_value')
                    if not row['value']:
                        row['value'] = \
                            CryptUnprotectData(cipher_blob)[1].decode()
                cookie_item = http.cookiejar.Cookie(**row, **dummy, version=0)
                self.set_cookie(cookie_item)


def webkit_timestamp_to_unix(webkit_timestamp: int) -> float:
    if not webkit_timestamp:
        return
    t = datetime.datetime(1601, 1, 1)
    t += datetime.timedelta(microseconds=webkit_timestamp)
    return t.timestamp()
