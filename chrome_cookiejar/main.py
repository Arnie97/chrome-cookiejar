import datetime
import http.cookiejar
import sqlite3
from typing import Iterable
from .decrypt import decrypt


class ChromeCookieJar(http.cookiejar.CookieJar):
    'Create CookieJar instance from the Chrome cookies database.'

    def __init__(self, cookie_file_path, domain_filter='%', policy=None):
        super().__init__(policy)
        dummy = {key: None for key in (
            'port', 'port_specified', 'domain_specified', 'domain_initial_dot',
            'path_specified', 'discard', 'comment', 'comment_url', 'rest'
        )}

        with sqlite3.connect(cookie_file_path) as conn:
            conn.row_factory = dict_factory
            sql_fields = ', '.join(self.get_cookie_fields(conn))
            sql = 'select %s from cookies where host_key like ?' % sql_fields
            for row in conn.execute(sql, [domain_filter]):
                row['expires'] = \
                    webkit_timestamp_to_unix(row.pop('expires_utc'))
                if row.get('encrypted_value') and not row.get('value'):
                    row['value'] = decrypt(row.pop('encrypted_value')).decode()
                cookie_item = http.cookiejar.Cookie(**row, **dummy, version=0)
                self.set_cookie(cookie_item)

    @staticmethod
    def get_cookie_fields(conn: sqlite3.Connection) -> Iterable[str]:
        'Adjust table fields to be compatible with different Chrome versions.'
        yield from [
            'host_key as domain', 'name', 'value', 'path', 'expires_utc'
        ]
        fields = set(get_field_names(conn, table='cookies'))

        # Chrome encrypts cookie values since version 33
        if 'encrypted_value' in fields:
            yield 'encrypted_value'

        # 'secure' was renamed to 'is_secure' since version 66
        if 'is_secure' in fields:
            yield 'is_secure as secure'
        else:
            yield 'secure'


def dict_factory(cursor, row):
    'This row factory returns each row as a dict, with field names as the key.'
    return {
        col[0]: row[idx]
        for idx, col in enumerate(cursor.description)
    }


def get_field_names(conn: sqlite3.Connection, table: str) -> Iterable[str]:
    'Return all field names in the specified database table.'
    for field in conn.execute('pragma table_info("%s")' % table):
        yield field['name']


def webkit_timestamp_to_unix(webkit_timestamp: int) -> float:
    'Convert WebKit timestamp to Unix epoch.'
    if not webkit_timestamp:
        return
    t = datetime.datetime(1601, 1, 1)
    t += datetime.timedelta(microseconds=webkit_timestamp)
    return t.timestamp()
