import sys

if sys.platform == 'win32':
    from .win32crypt import CryptUnprotectData

    def decrypt(cipher_blob: bytes) -> bytes:
        return CryptUnprotectData(cipher_blob)[1]

else:
    decrypt = NotImplemented
