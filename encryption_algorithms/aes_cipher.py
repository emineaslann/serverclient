# encryption_algorithms/aes_cipher.py
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16

def pkcs7_pad(data: bytes) -> bytes:
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len]) * pad_len

def pkcs7_unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    return data[:-pad_len]

class AESCipher:
    def encrypt(self, message: str, key: str) -> str:
        # key expected as raw string; we will use first 16 bytes (AES-128)
        key_bytes = key.encode('utf-8')
        if len(key_bytes) < 16:
            raise ValueError("AES key must be at least 16 bytes (use 16-byte key).")
        key_bytes = key_bytes[:16]
        iv = get_random_bytes(16)
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        plaintext = message.encode('utf-8')
        ct = cipher.encrypt(pkcs7_pad(plaintext))
        return base64.b64encode(iv + ct).decode('utf-8')

    def decrypt(self, token_b64: str, key: str) -> str:
        key_bytes = key.encode('utf-8')[:16]
        data = base64.b64decode(token_b64)
        iv = data[:16]
        ct = data[16:]
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        pt = pkcs7_unpad(cipher.decrypt(ct))
        return pt.decode('utf-8')
