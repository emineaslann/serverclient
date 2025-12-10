# encryption_algorithms/manual_aes.py
# Çok basitleştirilmiş, güvenli olmayan bir "round" tabanlı toy örneğidir.
# Amaç: öğrencinin round/s-box/perm işlemlerini anlaması.

def simple_xor(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

class ManualAES:
    def encrypt(self, message: str, key: str) -> str:
        # key must be 16 bytes ideally
        kb = key.encode('utf-8')
        pt = message.encode('utf-8')
        # basit 4 round: rotate + xor
        state = pt
        for r in range(4):
            # rotation
            state = state[r:] + state[:r] if len(state) > 1 else state
            state = simple_xor(state, kb)
        # hex return
        return state.hex()

    def decrypt(self, token_hex: str, key: str) -> str:
        kb = key.encode('utf-8')
        state = bytes.fromhex(token_hex)
        for r in reversed(range(4)):
            state = simple_xor(state, kb)
            state = state[-r:] + state[:-r] if len(state) > 1 else state
        return state.decode('utf-8', errors='ignore')
