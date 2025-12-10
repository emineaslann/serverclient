# encryption_algorithms/pigpen_cipher.py
from encryption_algorithms.base_cipher import BaseCipher

class PigpenCipher(BaseCipher):
    pigpen_map = {
        'A': '𐌰', 'B': '𐌱', 'C': '𐌲', 'D': '𐌳', 'E': '𐌴', 'F': '𐌵',
        'G': '𐌶', 'H': '𐌷', 'I': '𐌸', 'J': '𐌹', 'K': '𐌺', 'L': '𐌻',
        'M': '𐌼', 'N': '𐌽', 'O': '𐌾', 'P': '𐌿', 'Q': '𐍀', 'R': '𐍁',
        'S': '𐍂', 'T': '𐍃', 'U': '𐍄', 'V': '𐍅', 'W': '𐍆', 'X': '𐍇',
        'Y': '𐍈', 'Z': '𐍉'
    }
    reverse_map = {v: k for k, v in pigpen_map.items()}

    def encrypt(self, text, key=None):
        text = text.upper()
        return ''.join(self.pigpen_map.get(ch, ch) for ch in text)

    def decrypt(self, text, key=None):
        return ''.join(self.reverse_map.get(ch, ch) for ch in text)
