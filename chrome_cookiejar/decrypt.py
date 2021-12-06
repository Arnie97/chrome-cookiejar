import sys

if sys.platform == 'win32':
    from .win32crypt import CryptUnprotectData

    def decrypt(cipher_blob: bytes) -> bytes:
        return CryptUnprotectData(cipher_blob)[1]

else:
    from .unix_crypt import aes_cbc_decrypt, get_chrome_safe_storage

    def decrypt(cipher_blob: bytes) -> bytes:
        if not cipher_blob:
            return cipher_blob
        elif cipher_blob.startswith(b'v10'):
            if sys.platform == 'darwin':
                password = get_chrome_safe_storage()
            else:
                password = b'peanuts'.encode('utf-8')
        elif cipher_blob.startswith(b'v11'):
            password = get_chrome_safe_storage()
        else:
            raise ValueError('Unknown cipher type: %r' % cipher_blob)
        if sys.platform == 'darwin':
            return aes_cbc_decrypt(cipher_blob, password, iterations=1003)
        else:
            return aes_cbc_decrypt(cipher_blob, password)
