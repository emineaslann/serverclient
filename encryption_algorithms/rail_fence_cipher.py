from encryption_algorithms.base_cipher import BaseCipher

class RailFenceCipher(BaseCipher):
    def encrypt(self, text, key):
        if not key.isdigit():
            return "Anahtar bir sayı olmalı!"
        rails = int(key)
        if rails <= 1:
            return text

        fence = ['' for _ in range(rails)]
        rail = 0
        direction = 1  # Başlangıç yönü: aşağı

        for char in text:
            fence[rail] += char
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1  # yönü değiştir

        return ''.join(fence)

    def decrypt(self, text, key):
        if not key.isdigit():
            return "Anahtar bir sayı olmalı!"
        rails = int(key)
        if rails <= 1:
            return text

        pattern = self._get_pattern(len(text), rails)
        result = [''] * len(text)
        index = 0

        for r in range(rails):
            for i in range(len(text)):
                if pattern[i] == r:
                    result[i] = text[index]
                    index += 1

        return ''.join(result)

    def _get_pattern(self, length, rails):
        pattern = []
        rail = 0
        direction = 1  # Aşağı doğru başla
        for _ in range(length):
            pattern.append(rail)
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1
        return pattern

