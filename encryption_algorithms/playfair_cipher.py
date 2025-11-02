class PlayfairCipher:
    def __init__(self, key):
        self.key = self.prepare_key(key)
        self.matrix = self.generate_key_matrix(self.key)

    def prepare_key(self, key):
        key = key.upper().replace("J", "I")
        new_key = ""
        for char in key:
            if char not in new_key and char.isalpha():
                new_key += char
        return new_key

    def generate_key_matrix(self, key):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # J yok
        matrix = []
        for char in key:
            if char in alphabet:
                alphabet = alphabet.replace(char, "")
        full_key = key + alphabet

        # 5x5 matris oluştur
        matrix = [list(full_key[i:i+5]) for i in range(0, 25, 5)]
        return matrix

    def find_position(self, char):
        for i, row in enumerate(self.matrix):
            for j, val in enumerate(row):
                if val == char:
                    return i, j
        return None, None

    def prepare_text(self, text):
        text = text.upper().replace("J", "I")
        prepared = ""
        i = 0
        while i < len(text):
            a = text[i]
            b = text[i + 1] if i + 1 < len(text) else "X"
            if a == b:
                prepared += a + "X"
                i += 1
            else:
                prepared += a + b
                i += 2
        if len(prepared) % 2 != 0:
            prepared += "X"
        return prepared

    def encrypt(self, plaintext):
        plaintext = self.prepare_text(plaintext)
        ciphertext = ""
        for i in range(0, len(plaintext), 2):
            a, b = plaintext[i], plaintext[i + 1]
            row_a, col_a = self.find_position(a)
            row_b, col_b = self.find_position(b)

            if row_a == row_b:
                ciphertext += self.matrix[row_a][(col_a + 1) % 5]
                ciphertext += self.matrix[row_b][(col_b + 1) % 5]
            elif col_a == col_b:
                ciphertext += self.matrix[(row_a + 1) % 5][col_a]
                ciphertext += self.matrix[(row_b + 1) % 5][col_b]
            else:
                ciphertext += self.matrix[row_a][col_b]
                ciphertext += self.matrix[row_b][col_a]
        return ciphertext

