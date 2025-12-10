# encryption_algorithms/manual_des.py
# Basit 4-round Feistel toy (güvenli değildir)
def feistel_round(left: bytes, right: bytes, subkey: bytes) -> (bytes, bytes):
    # basit f(): xor + rotate
    f = bytes([ (b ^ subkey[i % len(subkey)]) for i,b in enumerate(right)])
    # yeni left
    new_left = bytes([l ^ f[i % len(f)] for i,l in enumerate(left)])
    return new_left, right

class ManualDES:
    def encrypt(self, message: str, key: str) -> str:
        kb = key.encode('utf-8')[:8]
        data = message.encode('utf-8')
        # pad to even length
        if len(data) % 2 != 0:
            data += b'\x00'
        left = data[:len(data)//2]
        right = data[len(data)//2:]
        rounds = 4
        for r in range(rounds):
            left, right = right, bytes([a ^ b for a,b in zip(left, kb*(len(left)//len(kb)+1))])
        return (left+right).hex()

    def decrypt(self, token_hex: str, key: str) -> str:
        kb = key.encode('utf-8')[:8]
        data = bytes.fromhex(token_hex)
        left = data[:len(data)//2]
        right = data[len(data)//2:]
        rounds = 4
        for r in range(rounds):
            right, left = left, bytes([a ^ b for a,b in zip(right, kb*(len(right)//len(kb)+1))])
        return (left+right).rstrip(b'\x00').decode('utf-8', errors='ignore')
