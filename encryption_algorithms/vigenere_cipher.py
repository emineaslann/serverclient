# encryption_algorithms/vigenere_cipher.py

class VigenereCipher:
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def generate_key(self, text, key):
        key = key.upper()
        if len(key) == 0:
            raise ValueError("Anahtar boş olamaz.")
        key = (key * (len(text) // len(key))) + key[:len(text) % len(key)]
        return key

    def encrypt(self, plaintext, key):
        plaintext = plaintext.upper()
        key = self.generate_key(plaintext, key)
        ciphertext = ""

        for p, k in zip(plaintext, key):
            if p in self.alphabet:
                p_index = self.alphabet.index(p)
                k_index = self.alphabet.index(k)
                c_index = (p_index + k_index) % 26
                ciphertext += self.alphabet[c_index]
            else:
                ciphertext += p  # harf dışındaki karakterleri aynen bırak
        return ciphertext

    def decrypt(self, ciphertext, key):
        ciphertext = ciphertext.upper()
        key = self.generate_key(ciphertext, key)
        plaintext = ""

        for c, k in zip(ciphertext, key):
            if c in self.alphabet:
                c_index = self.alphabet.index(c)
                k_index = self.alphabet.index(k)
                p_index = (c_index - k_index) % 26
                plaintext += self.alphabet[p_index]
            else:
                plaintext += c
        return plaintext
