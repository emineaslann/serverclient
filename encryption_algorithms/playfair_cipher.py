from encryption_algorithms.base_cipher import BaseCipher

class PlayfairCipher(BaseCipher):
    def __init__(self):
        self.matrix = []

    def generate_matrix(self, key):
        key = key.lower().replace("j", "i")
        alphabet = "abcdefghiklmnopqrstuvwxyz"

        seen = set()
        result = []

        for c in key:
            if c not in seen and c in alphabet:
                seen.add(c)
                result.append(c)

        for c in alphabet:
            if c not in seen:
                seen.add(c)
                result.append(c)

        # 5x5 matrix
        self.matrix = [result[i:i+5] for i in range(0, 25, 5)]

    def find_position(self, char):
        for i in range(5):
            for j in range(5):
                if self.matrix[i][j] == char:
                    return i, j
        return None

    def process_message(self, message):
        message = message.lower().replace("j", "i")
        message = "".join([c for c in message if c.isalpha()])

        result = ""
        i = 0
        while i < len(message):
            a = message[i]
            if i + 1 < len(message):
                b = message[i + 1]
                if a == b:
                    b = "x"
                    i += 1
                else:
                    i += 2
            else:
                b = "x"
                i += 1

            result += a + b

        return result

    def encrypt(self, message, key):
        self.generate_matrix(key)
        message = self.process_message(message)

        encrypted = ""

        for i in range(0, len(message), 2):
            a = message[i]
            b = message[i + 1]

            r1, c1 = self.find_position(a)
            r2, c2 = self.find_position(b)

            if r1 == r2:
                encrypted += self.matrix[r1][(c1 + 1) % 5]
                encrypted += self.matrix[r2][(c2 + 1) % 5]
            elif c1 == c2:
                encrypted += self.matrix[(r1 + 1) % 5][c1]
                encrypted += self.matrix[(r2 + 1) % 5][c2]
            else:
                encrypted += self.matrix[r1][c2]
                encrypted += self.matrix[r2][c1]

        return encrypted.upper()

    def decrypt(self, message, key):
        self.generate_matrix(key)
        message = message.lower()

        decrypted = ""

        for i in range(0, len(message), 2):
            a = message[i]
            b = message[i + 1]

            r1, c1 = self.find_position(a)
            r2, c2 = self.find_position(b)

            if r1 == r2:
                decrypted += self.matrix[r1][(c1 - 1) % 5]
                decrypted += self.matrix[r2][(c2 - 1) % 5]
            elif c1 == c2:
                decrypted += self.matrix[(r1 - 1) % 5][c1]
                decrypted += self.matrix[(r2 - 1) % 5][c2]
            else:
                decrypted += self.matrix[r1][c2]
                decrypted += self.matrix[r2][c1]

        return decrypted.upper()
