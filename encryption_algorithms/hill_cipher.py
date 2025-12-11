# encryption_algorithms/hill_cipher.py
import math

class HillCipher:
    """
    Basit 2x2 Hill Cipher implementasyonu.
    - Key: iki satır/iki sütun integer matrisi (örnek formatlar: "3 3\n2 5" veya "3 3;2 5")
    - Plaintext: A-Z harfleri (diğerleri atılır). Küçük/büyük otomatik normalize edilir.
    - Padding: tek karakter kalırsa 'X' eklenir.
    """

    def _clean_text(self, text):
        return "".join([c for c in text.upper() if c.isalpha()])

    def _parse_key(self, key):
        # Çok toleranslı: yeni satır, noktalı virgül veya pipe ile ayrılmış satırları kabul eder
        if isinstance(key, str):
            rows = []
            sep = None
            if "\n" in key:
                sep = "\n"
            elif ";" in key:
                sep = ";"
            elif "|" in key:
                sep = "|"

            if sep:
                parts = [r.strip() for r in key.split(sep) if r.strip()]
            else:
                # tek satırsa boşluklara göre iki sayı bekle
                parts = [key.strip()]

            for p in parts:
                nums = [int(x) for x in p.split() if x.strip()]
                if nums:
                    rows.append(nums)

            # Eğer tek satır verildiyse ama 4 sayı varsa ikiye böl
            if len(rows) == 1 and len(rows[0]) == 4:
                a = rows[0]
                rows = [a[:2], a[2:]]
        else:
            raise ValueError("Key must be a string with numeric matrix entries")

        if len(rows) != 2 or len(rows[0]) != 2 or len(rows[1]) != 2:
            raise ValueError("Key must be a 2x2 matrix (e.g. '3 3\\n2 5')")

        # modulo 26 normalize
        return [[rows[0][0] % 26, rows[0][1] % 26],
                [rows[1][0] % 26, rows[1][1] % 26]]

    def _modinv(self, a, m):
        # modular inverse using extended euclid
        a = a % m
        if a == 0:
            return None
        # Extended Euclidean
        def egcd(a,b):
            if b==0:
                return (1,0,a)
            x,y,g = egcd(b, a%b)
            return (y, x - (a//b)*y, g)
        x, y, g = egcd(a, m)
        if g != 1:
            return None
        return x % m

    def _matrix_det_inv(self, mat):
        # determinant and inverse for 2x2 mod 26
        a, b = mat[0]
        c, d = mat[1]
        det = (a * d - b * c) % 26
        inv_det = self._modinv(det, 26)
        if inv_det is None:
            return None  # not invertible
        # inverse of 2x2: inv_det * [[d, -b],[-c, a]]
        inv = [[( d * inv_det) % 26, ((-b) * inv_det) % 26],
               [((-c) * inv_det) % 26, ( a * inv_det) % 26]]
        return inv

    def _mat_vec_mul(self, mat, vec):
        return [ (mat[0][0]*vec[0] + mat[0][1]*vec[1]) % 26,
                 (mat[1][0]*vec[0] + mat[1][1]*vec[1]) % 26 ]

    def encrypt(self, message, key):
        mat = self._parse_key(key)
        text = self._clean_text(message)
        if len(text) % 2 == 1:
            text += "X"
        out = []
        for i in range(0, len(text), 2):
            v = [ord(text[i]) - 65, ord(text[i+1]) - 65]
            r = self._mat_vec_mul(mat, v)
            out.append(chr(r[0] + 65))
            out.append(chr(r[1] + 65))
        return "".join(out)

    def decrypt(self, message, key):
        mat = self._parse_key(key)
        inv = self._matrix_det_inv(mat)
        if inv is None:
            raise ValueError("Key matrix is not invertible modulo 26; cannot decrypt.")
        text = "".join([c for c in message.upper() if c.isalpha()])
        if len(text) % 2 == 1:
            text += "X"
        out = []
        for i in range(0, len(text), 2):
            v = [ord(text[i]) - 65, ord(text[i+1]) - 65]
            r = self._mat_vec_mul(inv, v)
            out.append(chr((r[0] % 26) + 65))
            out.append(chr((r[1] % 26) + 65))
        return "".join(out)
