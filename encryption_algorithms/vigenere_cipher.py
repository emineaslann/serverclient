# encryption_algorithms/vigenere_cipher.py
from encryption_algorithms.base_cipher import BaseCipher

class VigenereCipher(BaseCipher):
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def generate_key(self, text, key):
        key = key.upper()
        if len(key) == 0:
            raise ValueError("Anahtar boş olamaz.")
        # sadece harfler için aynı uzunlukta anahtar
        full = []
        ki = 0
        for ch in text:
            if ch.upper() in self.alphabet:
                full.append(key[ki % len(key)])
                ki += 1
            else:
                full.append(ch)
        return ''.join(full)

    def encrypt(self, plaintext, key):
        plaintext = plaintext.upper()
        full_key = self.generate_key(plaintext, key)
        ciphertext = ""
        for p, k in zip(plaintext, full_key):
            if p in self.alphabet:
                p_index = self.alphabet.index(p)
                k_index = self.alphabet.index(k)
                c_index = (p_index + k_index) % 26
                ciphertext += self.alphabet[c_index]
            else:
                ciphertext += p
        return ciphertext

    def decrypt(self, ciphertext, key):
        ciphertext = ciphertext.upper()
        full_key = self.generate_key(ciphertext, key)
        plaintext = ""
        for c, k in zip(ciphertext, full_key):
            if c in self.alphabet:
                c_index = self.alphabet.index(c)
                k_index = self.alphabet.index(k)
                p_index = (c_index - k_index) % 26
                plaintext += self.alphabet[p_index]
            else:
                plaintext += c
        return plaintext
