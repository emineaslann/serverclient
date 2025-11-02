from abc import ABC, abstractmethod

class BaseCipher(ABC):
    name = "Base"

    @abstractmethod
    def encrypt(self, text, key):
        pass
