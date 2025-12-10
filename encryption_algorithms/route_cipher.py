# encryption_algorithms/route_cipher.py
from encryption_algorithms.base_cipher import BaseCipher

class RouteCipher(BaseCipher):
    def encrypt(self, text, key):
        if not str(key).isdigit():
            return "Anahtar bir sayı olmalı!"
        cols = int(key)
        text = ''.join(text.split())
        rows = (len(text) + cols - 1) // cols

        matrix = [['' for _ in range(cols)] for _ in range(rows)]
        idx = 0
        for r in range(rows):
            for c in range(cols):
                if idx < len(text):
                    matrix[r][c] = text[idx]
                    idx += 1

        res = ''
        for c in range(cols):
            for r in range(rows):
                if matrix[r][c]:
                    res += matrix[r][c]
        return res

    def decrypt(self, text, key):
        if not str(key).isdigit():
            return "Anahtar bir sayı olmalı!"
        cols = int(key)
        text = ''.join(text.split())
        rows = (len(text) + cols - 1) // cols

        matrix = [['' for _ in range(cols)] for _ in range(rows)]
        idx = 0
        for c in range(cols):
            for r in range(rows):
                if idx < len(text):
                    matrix[r][c] = text[idx]
                    idx += 1

        res = ''
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c]:
                    res += matrix[r][c]
        return res

