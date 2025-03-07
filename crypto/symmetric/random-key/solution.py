import math

MOD = 256

class LCG:
    def __init__(self, a: int, c: int, x0: int):
        self.a = a
        self.c = c
        self.x = x0

    def generate_byte(self) -> int:
        prev_x = self.x
        self.x = (self.a * self.x + self.c) % MOD
        return prev_x


enc = bytes.fromhex(open('./message.txt', 'rb').read().strip().decode())

plain = b"UniTN{"

stream_start = [c ^ p for c,p in zip(enc[:6], plain)]
s = list(stream_start)

s0, s1, s2, s3, s4, s5 = s[:6]

d1 = (s1 - s0) % 256
d2 = (s2 - s1) % 256
g = math.gcd(d1, 256)

m = 256 // g
d1_prime = d1 // g
d2_prime = d2 // g

inv_d1_prime = pow(d1_prime, -1, m)
a0 = (d2_prime * inv_d1_prime) % m

c0 = (s1 - a0 * s0) % 256

lcg = LCG(a0, c0, s0)

plain = bytes([c ^ lcg.generate_byte() for c in enc])
print(plain.decode())
