# encryption_algorithms/des_cipher.py
import base64
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 8

def pad8(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len]) * pad_len

def unpad8(data: bytes) -> bytes:
    pad_len = data[-1]
    return data[:-pad_len]

class DESCipher:
    def encrypt(self, message: str, key: str) -> str:
        key_bytes = key.encode('utf-8')
        if len(key_bytes) < 8:
            raise ValueError("DES key must be at least 8 bytes.")
        key_bytes = key_bytes[:8]
        iv = get_random_bytes(8)
        cipher = DES.new(key_bytes, DES.MODE_CBC, iv)
        ct = cipher.encrypt(pad8(message.encode('utf-8')))
        return base64.b64encode(iv + ct).decode('utf-8')

    def decrypt(self, token_b64: str, key: str) -> str:
        key_bytes = key.encode('utf-8')[:8]
        data = base64.b64decode(token_b64)
        iv = data[:8]
        ct = data[8:]
        cipher = DES.new(key_bytes, DES.MODE_CBC, iv)
        pt = unpad8(cipher.decrypt(ct))
        return pt.decode('utf-8')
