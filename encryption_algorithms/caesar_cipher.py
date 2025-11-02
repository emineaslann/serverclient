from .base_cipher import BaseCipher

class CaesarCipher(BaseCipher):
    """Klasik Caesar Cipher şifreleme sınıfı."""

    def encrypt(self, text, key=3):
        """Metni kaydırma anahtarına göre şifreler."""
        result = ""
        key = int(key) if key else 3  # Varsayılan 3

        for char in text:
            if char.isalpha():
                shift = 65 if char.isupper() else 97
                result += chr((ord(char) - shift + key) % 26 + shift)
            else:
                result += char
        return result

    def decrypt(self, text, key=3):
        """Metni çözer (şifreyi geri alır)."""
        result = ""
        key = int(key) if key else 3

        for char in text:
            if char.isalpha():
                shift = 65 if char.isupper() else 97
                result += chr((ord(char) - shift - key) % 26 + shift)
            else:
                result += char
        return result
