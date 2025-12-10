# encryption_algorithms/columnar_transposition_cipher.py
from encryption_algorithms.base_cipher import BaseCipher

class ColumnarTranspositionCipher(BaseCipher):
    def _get_order(self, key):
        key = key.upper()
        enumerated = list(enumerate(key))
        sorted_en = sorted(enumerated, key=lambda x: (x[1], x[0]))
        order = [0] * len(key)
        for rank, (orig_idx, _) in enumerate(sorted_en):
            order[orig_idx] = rank
        return order

    def encrypt(self, text, key):
        if not key:
            return "Anahtar boş olamaz!"
        plain = ''.join(text.split()).upper()
        key = key.replace(" ", "")
        cols = len(key)
        rows = (len(plain) + cols - 1) // cols

        matrix = [['' for _ in range(cols)] for _ in range(rows)]
        idx = 0
        for r in range(rows):
            for c in range(cols):
                if idx < len(plain):
                    matrix[r][c] = plain[idx]
                    idx += 1

        order = self._get_order(key)
        rank_to_col = [None] * cols
        for orig_col, rank in enumerate(order):
            rank_to_col[rank] = orig_col

        ciphertext = ''
        for rank in range(cols):
            col = rank_to_col[rank]
            for r in range(rows):
                if matrix[r][col]:
                    ciphertext += matrix[r][col]
        return ciphertext

    def decrypt(self, text, key):
        if not key:
            return "Anahtar boş olamaz!"
        cipher = ''.join(text.split()).upper()
        key = key.replace(" ", "")
        cols = len(key)
        rows = (len(cipher) + cols - 1) // cols

        order = self._get_order(key)
        rank_to_col = [None] * cols
        for orig_col, rank in enumerate(order):
            rank_to_col[rank] = orig_col

        total_cells = rows * cols
        empty_cells = total_cells - len(cipher)
        col_heights = [rows] * cols
        for i in range(empty_cells):
            col_heights[cols-1 - i] -= 1

        matrix = [['' for _ in range(cols)] for _ in range(rows)]
        idx = 0
        for rank in range(cols):
            col = rank_to_col[rank]
            height = col_heights[rank]
            for r in range(height):
                if idx < len(cipher):
                    matrix[r][col] = cipher[idx]
                    idx += 1

        plaintext = ''
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c]:
                    plaintext += matrix[r][c]
        return plaintext
