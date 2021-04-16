from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


def aes_cbc_decrypt(
    cipher_blob: bytes,
    password: bytes,
    salt=b'saltysalt',
    length=16,
    iv=16 * b' ',
    iterations=1,
) -> bytes:
    key = PBKDF2(password, salt, length, iterations)  # type: ignore
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)

    # strip off the 'v10' prefix before AES decrypt
    clear_text = cipher.decrypt(cipher_blob[3:])

    # strip off the padding
    padding = clear_text[-1] if clear_text else 0
    return clear_text[:-padding]


def get_chrome_safe_storage() -> bytes:
    raise NotImplementedError
