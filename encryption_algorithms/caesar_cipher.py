# encryption_algorithms/caesar_cipher.py
from encryption_algorithms.base_cipher import BaseCipher
import string

class CaesarCipher(BaseCipher):
    def __init__(self):
        self.alphabet_upper = string.ascii_uppercase
        self.alphabet_lower = string.ascii_lowercase

    def encrypt(self, plaintext, key):
        try:
            shift = int(key)
        except:
            return "Anahtar sayı olmalı!"
        result = []
        for ch in plaintext:
            if ch in self.alphabet_upper:
                idx = (self.alphabet_upper.index(ch) + shift) % 26
                result.append(self.alphabet_upper[idx])
            elif ch in self.alphabet_lower:
                idx = (self.alphabet_lower.index(ch) + shift) % 26
                result.append(self.alphabet_lower[idx])
            else:
                result.append(ch)
        return ''.join(result)

    def decrypt(self, ciphertext, key):
        try:
            shift = int(key)
        except:
            return "Anahtar sayı olmalı!"
        result = []
        for ch in ciphertext:
            if ch in self.alphabet_upper:
                idx = (self.alphabet_upper.index(ch) - shift) % 26
                result.append(self.alphabet_upper[idx])
            elif ch in self.alphabet_lower:
                idx = (self.alphabet_lower.index(ch) - shift) % 26
                result.append(self.alphabet_lower[idx])
            else:
                result.append(ch)
        return ''.join(result)
