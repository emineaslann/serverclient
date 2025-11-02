# encryption_algorithms/substitution_cipher.py
from encryption_algorithms.base_cipher import BaseCipher
import string

class SubstitutionCipher(BaseCipher):
    def __init__(self):
        self.alphabet = string.ascii_lowercase

    def generate_substitution_table(self, key):
        """
        Anahtar kelimeden türetilen bir alfabe tablosu oluşturur.
        Örneğin: key='phukded' -> 'phukde...'
        """
        key = key.lower()
        # Anahtardaki tekrar eden harfleri kaldır
        unique_key = ""
        for ch in key:
            if ch not in unique_key and ch in self.alphabet:
                unique_key += ch

        # Geriye kalan harfleri ekle
        for ch in self.alphabet:
            if ch not in unique_key:
                unique_key += ch

        return unique_key

    def encrypt(self, plaintext, key):
        table = self.generate_substitution_table(key)
        ciphertext = ""
        for ch in plaintext.lower():
            if ch in self.alphabet:
                ciphertext += table[self.alphabet.index(ch)]
            else:
                ciphertext += ch
        return ciphertext

    def decrypt(self, ciphertext, key):
        table = self.generate_substitution_table(key)
        plaintext = ""
        for ch in ciphertext.lower():
            if ch in table:
                plaintext += self.alphabet[table.index(ch)]
            else:
                plaintext += ch
        return plaintext

