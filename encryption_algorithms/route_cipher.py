# encryption_algorithms/route_cipher.py
from encryption_algorithms.base_cipher import BaseCipher

class RouteCipher(BaseCipher):
    def encrypt(self, text, key):
        if not key.isdigit():
            return "Anahtar bir sayı olmalı!"
        key = int(key)

        text = text.replace(" ", "")
        cols = key
        rows = (len(text) + cols - 1) // cols

        # Matrise satır satır yerleştir
        matrix = [['' for _ in range(cols)] for _ in range(rows)]
        index = 0
        for r in range(rows):
            for c in range(cols):
                if index < len(text):
                    matrix[r][c] = text[index]
                    index += 1

        # Route Cipher: sütun sütun yukarıdan aşağıya oku
        result = ''
        for c in range(cols):
            for r in range(rows):
                if matrix[r][c]:
                    result += matrix[r][c]

        return result

    def decrypt(self, text, key):
        if not key.isdigit():
            return "Anahtar bir sayı olmalı!"
        key = int(key)

        text = text.replace(" ", "")
        cols = key
        rows = (len(text) + cols - 1) // cols

        # Matris oluştur
        matrix = [['' for _ in range(cols)] for _ in range(rows)]
        index = 0

        # Sütun sütun yerleştir
        for c in range(cols):
            for r in range(rows):
                if index < len(text):
                    matrix[r][c] = text[index]
                    index += 1

        # Satır satır oku
        result = ''
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c]:
                    result += matrix[r][c]

        return result

