# DPAPI access library
# This file uses code originally created by Crusher Joe:
# http://article.gmane.org/gmane.comp.python.ctypes/420

from ctypes import POINTER, Structure, c_char, c_wchar_p
from ctypes import byref, create_string_buffer, memmove, windll
from ctypes.wintypes import DWORD

CRYPTPROTECT_UI_FORBIDDEN = 0x01


class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', DWORD),
        ('pbData', POINTER(c_char))
    ]


def CryptUnprotectData(
    cipher_text=b'', entropy=b'', reserved=None, prompt_struct=None,
    flags=CRYPTPROTECT_UI_FORBIDDEN
):
    blob_in, blob_entropy, blob_out = map(
        lambda x: DATA_BLOB(len(x), create_string_buffer(x)),
        [cipher_text, entropy, b'']
    )
    desc = c_wchar_p()

    if not windll.crypt32.CryptUnprotectData(
        byref(blob_in), byref(desc), byref(blob_entropy),
        reserved, prompt_struct, flags, byref(blob_out)
    ):
        raise RuntimeError('Failed to decrypt the cipher text with DPAPI')

    description = desc.value
    buffer_out = create_string_buffer(int(blob_out.cbData))
    memmove(buffer_out, blob_out.pbData, blob_out.cbData)
    map(windll.kernel32.LocalFree, [desc, blob_out.pbData])
    return description, buffer_out.value
