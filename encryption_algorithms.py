# encryption_algorithms.py
"""
Bu dosya tüm şifreleme algoritmalarını içerir.
Yeni algoritma eklendikçe buraya eklenir.
"""

# ============================================================
#                    CAESAR CIPHER
# ============================================================
class CaesarCipher:
    def __init__(self, key):
        try:
            self.key = int(key)
        except ValueError:
            self.key = 3  # Varsayılan anahtar değeri
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def encrypt(self, text):
        text = text.upper()
        result = ""
        for ch in text:
            if ch in self.alphabet:
                idx = (self.alphabet.index(ch) + self.key) % 26
                result += self.alphabet[idx]
            else:
                result += ch
        return result

    def decrypt(self, text):
        text = text.upper()
        result = ""
        for ch in text:
            if ch in self.alphabet:
                idx = (self.alphabet.index(ch) - self.key) % 26
                result += self.alphabet[idx]
            else:
                result += ch
        return result


# ============================================================
#                    VIGENERE CIPHER
# ============================================================
class VigenereCipher:
    def __init__(self, key):
        self.key = key.upper() if key else "A"
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def _format_key(self, text):
        """Metin uzunluğuna göre anahtarı tekrarlar."""
        key_repeated = ""
        key_index = 0
        for ch in text:
            if ch.isalpha():
                key_repeated += self.key[key_index % len(self.key)]
                key_index += 1
            else:
                key_repeated += ch
        return key_repeated

    def encrypt(self, text):
        text = text.upper()
        formatted_key = self._format_key(text)
        result = ""
        for t_char, k_char in zip(text, formatted_key):
            if t_char in self.alphabet:
                shift = self.alphabet.index(k_char)
                idx = (self.alphabet.index(t_char) + shift) % 26
                result += self.alphabet[idx]
            else:
                result += t_char
        return result

    def decrypt(self, text):
        text = text.upper()
        formatted_key = self._format_key(text)
        result = ""
        for t_char, k_char in zip(text, formatted_key):
            if t_char in self.alphabet:
                shift = self.alphabet.index(k_char)
                idx = (self.alphabet.index(t_char) - shift) % 26
                result += self.alphabet[idx]
            else:
                result += t_char
        return result


# ============================================================
#                    GELECEK ALGORİTMALAR
# ============================================================
# Buraya eklenecek:
# - XOR Cipher
# - Affine Cipher
# - Hill Cipher (isterseniz)
#
# Yeni algoritma eklendiğinde:
#  1️⃣ Yeni sınıf oluştur
#  2️⃣ server.py içindeki get_cipher_instance() fonksiyonuna ekle
# ============================================================
