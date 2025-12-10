# encryption_algorithms/rsa_cipher.py
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class RSACipher:
    def encrypt(self, message: str, key: str) -> dict:
        """
        If key is a PEM public key string -> use it to encrypt and return base64 ciphertext.
        If key is empty -> generate new keypair and return ciphertext plus private_key in result.
        """
        msg_bytes = message.encode('utf-8')
        if not key or not key.strip().startswith("-----BEGIN"):
            # generate keypair
            new_key = RSA.generate(2048)
            private_pem = new_key.export_key().decode('utf-8')
            pub_pem = new_key.publickey().export_key().decode('utf-8')
            cipher = PKCS1_OAEP.new(new_key.publickey())
            ct = cipher.encrypt(msg_bytes)
            return {
                "encrypted_message": base64.b64encode(ct).decode('utf-8'),
                "private_key": private_pem,
                "public_key": pub_pem
            }
        else:
            pub = RSA.import_key(key.encode('utf-8'))
            cipher = PKCS1_OAEP.new(pub)
            ct = cipher.encrypt(msg_bytes)
            return {"encrypted_message": base64.b64encode(ct).decode('utf-8')}

    def decrypt(self, token_b64: str, key: str) -> str:
        if not key or not key.strip().startswith("-----BEGIN"):
            raise ValueError("RSA decrypt requires private key in PEM format.")
        private = RSA.import_key(key.encode('utf-8'))
        cipher = PKCS1_OAEP.new(private)
        pt = cipher.decrypt(base64.b64decode(token_b64))
        return pt.decode('utf-8')
