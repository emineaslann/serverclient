import numpy as np

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# --- yardımcı fonksiyonlar ---

def text_to_numbers(text):
    return [ALPHABET.index(c) for c in text.upper() if c.isalpha()]

def numbers_to_text(nums):
    return ''.join(ALPHABET[n % 26] for n in nums)

def mod_inverse_matrix(matrix, modulus=26):
    det = int(round(np.linalg.det(matrix)))  # determinant
    det_mod = det % modulus

    # determinant mod 26 için ters alınır
    det_inv = pow(det_mod, -1, modulus)

    # klasik adjoint (adjugate)
    adj = np.round(det * np.linalg.inv(matrix)).astype(int)

    return (det_inv * adj) % modulus


# --- Hill Encryption (3x3) ---

def encrypt_hill(plaintext, key_matrix):
    nums = text_to_numbers(plaintext)

    # 3’e tam bölünmezse padding X ekle
    while len(nums) % 3 != 0:
        nums.append(ALPHABET.index("X"))

    nums = np.array(nums).reshape(-1, 3)

    encrypted = (nums @ key_matrix) % 26
    encrypted = encrypted.reshape(-1)

    return numbers_to_text(encrypted)


# --- Hill Decryption (3x3) ---

def decrypt_hill(ciphertext, key_matrix):
    nums = text_to_numbers(ciphertext)

    nums = np.array(nums).reshape(-1, 3)

    inv_key = mod_inverse_matrix(key_matrix)

    decrypted = (nums @ inv_key) % 26
    decrypted = decrypted.reshape(-1)

    return numbers_to_text(decrypted)
