# encryption_algorithms/rail_fence_cipher.py
from encryption_algorithms.base_cipher import BaseCipher

class RailFenceCipher(BaseCipher):
    def encrypt(self, text, key):
        try:
            rails = int(key)
        except:
            return "Anahtar bir sayı olmalı!"
        if rails <= 1:
            return text

        fence = ['' for _ in range(rails)]
        rail = 0
        direction = 1  # aşağı başla
        for ch in text:
            fence[rail] += ch
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1
        return ''.join(fence)

    def decrypt(self, text, key):
        try:
            rails = int(key)
        except:
            return "Anahtar bir sayı olmalı!"
        if rails <= 1:
            return text

        pattern = self._get_pattern(len(text), rails)
        result = [''] * len(text)
        pos = 0
        for r in range(rails):
            for i in range(len(text)):
                if pattern[i] == r:
                    result[i] = text[pos]
                    pos += 1
        return ''.join(result)

    def _get_pattern(self, length, rails):
        pattern = []
        rail = 0
        direction = 1
        for _ in range(length):
            pattern.append(rail)
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1
        return pattern

