from Crypto.Util.number import long_to_bytes
from math import gcd
from pwn import remote

def get_cipher(r: remote, message: bytes, name=None) -> int:
    r.sendlineafter(b'> ', b'1')
    if name: r.sendlineafter(b'> ', name)
    r.sendlineafter(b'> ', message)
    r.recvuntil(b': ')
    return int(r.recvline(keepends=False))

e = 65537
def compute_n(ciphers: dict[bytes, int]) -> int:
    # r_i = p^e - (p^e mod n) are multiples of n, so their gcd is n or
    # a multiple of it -> the more values the better
    # r_i is congruent to 0 mod n
    rs = [(pow(ord(p), e) - c) for p,c in ciphers.items()]
    return gcd(*rs)

def multiplicative_attack(r: remote, n: int, c_flag: int, name=None) -> int:
    s = 2                         # small multiplier
    s_e = pow(s, e, n)            # encryption of s
    c_prime = (c_flag * s_e) % n  # modified ciphertext: c' = (c_flag * s^e) mod n

    r.sendlineafter(b'> ', b'2')
    if name: r.sendlineafter(b'> ', b'A' * 72)
    r.sendlineafter(b'> ', str(c_prime).encode())
    r.recvuntil(b': ')

    m_prime = int(r.recvline(keepends=False)) # m' = s * FLAG
    return m_prime // s                       # s * FLAG < n -> simply divide

# ======== First version ========
r1 = remote('cyberchallenge.disi.unitn.it', 50102)
r1.recvuntil(b': ')
c_flag = int(r1.recvline(keepends=False))
ciphers = {}
for p in [b'A', b'B', b'C']:
    ciphers[p] = get_cipher(r1, p)

n = compute_n(ciphers)
int_flag = multiplicative_attack(r1, n, c_flag)
print(long_to_bytes(int_flag).decode())

# ======== Second version =======
r2 = remote('cyberchallenge.disi.unitn.it', 50103)
r2.recvuntil(b': ')
c_flag = int(r2.recvline(keepends=False))

# bcrypt only uses the first 72 bytes of the input to the hashing function
# if two integrity tokens share the same first 72 bytes, they will have the same hash
# integrity_token = name.encode() + long_to_bytes(encrypted)
name = b'A' * 72

ciphers = {}
for p in [b'A', b'B', b'C']:
    ciphers[p] = get_cipher(r2, p, name)

n = compute_n(ciphers)
int_flag = multiplicative_attack(r2, n, c_flag, name)
print(long_to_bytes(int_flag).decode())
