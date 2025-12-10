# encryption_algorithms/substitution_cipher.py
from encryption_algorithms.base_cipher import BaseCipher
import string

class SubstitutionCipher(BaseCipher):
    # Örnek sabit ikame alfabesi (örnek: QWERTY...)
    # Eğer öğretmen/tezde farklı bir harita istersen burada değiştir.
    MAP = dict(zip(string.ascii_uppercase, "QWERTYUIOPASDFGHJKLZXCVBNM"))
    REVERSE_MAP = {v: k for k, v in MAP.items()}

    def encrypt(self, plaintext, key=None):
        text = plaintext.upper()
        out = []
        for ch in text:
            out.append(self.MAP.get(ch, ch))
        return ''.join(out)

    def decrypt(self, ciphertext, key=None):
        text = ciphertext.upper()
        out = []
        for ch in text:
            out.append(self.REVERSE_MAP.get(ch, ch))
        return ''.join(out)
