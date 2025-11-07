# encryption_algorithms/columnar_transposition_cipher.py
from encryption_algorithms.base_cipher import BaseCipher

class ColumnarTranspositionCipher(BaseCipher):
    def _get_order(self, key):
        """
        Anahtarın sütun sırasını döndürür.
        Aynı harfler için stabil (ilk göründüğü index önce) sıralama yapılır.
        Örnek: key = "ZEBRAS" -> order = [5, 2, 1, 3, 4, 0]  (örnek değil, mantık gösterimi)
        """
        key = key.upper()
        enumerated = list(enumerate(key))  # (index, char)
        # sort by char then by original index to be stable on duplicates
        sorted_en = sorted(enumerated, key=lambda x: (x[1], x[0]))
        # map original index -> rank
        order = [0] * len(key)
        for rank, (orig_idx, _) in enumerate(sorted_en):
            order[orig_idx] = rank
        return order

    def encrypt(self, text, key):
        if not key:
            return "Anahtar boş olamaz!"

        # normalize
        plain = ''.join(text.split()).upper()
        key = key.replace(" ", "")
        cols = len(key)
        rows = (len(plain) + cols - 1) // cols

        # doldur matris (satır satır)
        matrix = [['' for _ in range(cols)] for _ in range(rows)]
        idx = 0
        for r in range(rows):
            for c in range(cols):
                if idx < len(plain):
                    matrix[r][c] = plain[idx]
                    idx += 1

        # hangi sütunun hangi sırada okunacağını al
        order = self._get_order(key)  # order[orig_col] = rank
        # invert order: for rank -> orig_col
        rank_to_col = [None] * cols
        for orig_col, rank in enumerate(order):
            rank_to_col[rank] = orig_col

        # oku sütun sütun, rank sırasına göre
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

        # hangi sütunun hangi sırada olduğunu al
        order = self._get_order(key)
        rank_to_col = [None] * cols
        for orig_col, rank in enumerate(order):
            rank_to_col[rank] = orig_col

        # sütun uzunluklarını hesapla (son satır dolu olmayabilir)
        # bazı sütunlar diğerlerinden 1 kısa olur; bunun için toplam hücre sayısı = rows*cols
        total_cells = rows * cols
        empty_cells = total_cells - len(cipher)
        # sütunların doluluk sayısını rank sırasına göre hesapla
        col_heights = [rows] * cols
        # sondan başlayarak (en yüksek rank'lı sütunlar) boş hücre düşür
        for i in range(empty_cells):
            # en son rank'li sütun (cols-1 - i) bir hücre eksik
            col_heights[cols-1 - i] -= 1

        # matrix boş oluştur
        matrix = [['' for _ in range(cols)] for _ in range(rows)]
        idx = 0
        # cipher metnini rank sırasına göre sütun sütun yerleştir
        for rank in range(cols):
            col = rank_to_col[rank]
            height = col_heights[rank]
            for r in range(height):
                if idx < len(cipher):
                    matrix[r][col] = cipher[idx]
                    idx += 1

        # satır satır oku
        plaintext = ''
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c]:
                    plaintext += matrix[r][c]
        return plaintext
