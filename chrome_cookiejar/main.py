import datetime
import http.cookiejar
import sqlite3
from typing import Dict, Iterable, Optional, Any
from .decrypt import decrypt
from .path import find_cookies_path


class ChromeCookieJar(http.cookiejar.CookieJar):

    def __init__(
        self,
        cookies_path=None,
        host_filter='%',
        policy=None
    ):
        '''Create CookieJar instance from the Chrome cookies database.

        Parameters
        ----------
        cookies_path: str, optional
            Path of the Chrom(ium) Cookies database file.
            If omitted, try to find the file in its default locations.

        host_filter: str, optional
            Filter cookies in the database by their host names.
            Only matched items would be added to the cookie jar.
            Support % and _ wildcards, as in the SQL "LIKE" clause.
            If omitted, include all cookies in the database.
        '''
        if cookies_path is None:
            cookies_path = find_cookies_path()

        super().__init__(policy)
        dummy = {key: None for key in (
            'port', 'port_specified', 'domain_specified', 'domain_initial_dot',
            'path_specified', 'discard', 'comment', 'comment_url', 'rest'
        )}

        with sqlite3.connect(cookies_path) as conn:
            conn.row_factory = dict_factory
            sql_fields = ', '.join(self.get_cookie_fields(conn))
            sql = 'select %s from cookies where host_key like ?' % sql_fields
            for row in conn.execute(sql, [host_filter]):
                row['expires'] = nt_timestamp_to_unix(row.pop('expires_utc'))
                if row.get('encrypted_value') and not row.get('value'):
                    row['value'] = decrypt(row.pop('encrypted_value')).decode()
                self.set_cookie(http.cookiejar.Cookie(
                    **row, **dummy, version=0,  # typing: ignore
                ))

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


def dict_factory(cursor: sqlite3.Cursor, row: tuple) -> Dict[str, Any]:
    'This row factory returns each row as a dict, with field names as the key.'
    return {
        col[0]: row[idx]
        for idx, col in enumerate(cursor.description)
    }


def get_field_names(conn: sqlite3.Connection, table: str) -> Iterable[str]:
    'Return all field names in the specified database table.'
    for field in conn.execute('pragma table_info("%s")' % table):
        yield field['name']


def nt_timestamp_to_unix(nt_timestamp: int) -> Optional[float]:
    '''Convert Windows NT FILETIME timestamp to Unix epoch.

    >>> nt_timestamp_to_unix(10275638401000000)
    91111881601.0
    '''
    if not nt_timestamp:
        return None
    t = datetime.datetime(1601, 1, 1)
    t += datetime.timedelta(microseconds=nt_timestamp)
    return t.timestamp()
