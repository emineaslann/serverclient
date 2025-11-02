from .caesar_cipher import CaesarCipher
from .substitution_cipher import SubstitutionCipher

ALL_CIPHERS = {
    "Caesar Cipher": CaesarCipher(),
    "Substitution Cipher": SubstitutionCipher(),
}
