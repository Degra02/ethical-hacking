from Crypto.Util.number import bytes_to_long, long_to_bytes
from math import gcd
from pwn import remote

r = remote('cyberchallenge.disi.unitn.it', 50103)

r.recvuntil(b': ')
c_flag = int(r.recvline(keepends=False))

# bcrypt only uses the first 72 bytes of the input to the hashing function
# if two integrity tokens share the same first 72 bytes, they will have the same hash
# integrity_token = name.encode() + long_to_bytes(encrypted)
r.sendlineafter(b'> ', b'1')
r.sendlineafter(b'> ', b'A' * 72)
r.sendlineafter(b'> ', b'A')
r.recvuntil(b': ')
c1 = int(r.recvline(keepends=False)) # A^e mod n

r.sendlineafter(b'> ', b'1')
r.sendlineafter(b'> ', b'A' * 72)
r.sendlineafter(b'> ', b'B')
r.recvuntil(b': ')
c2 = int(r.recvline(keepends=False)) # B^e mod n

r.sendlineafter(b'> ', b'1')
r.sendlineafter(b'> ', b'A' * 72)
r.sendlineafter(b'> ', b'C')
r.recvuntil(b': ')
c3 = int(r.recvline(keepends=False)) # B^e mod n

m1 = ord(b'A')
m2 = ord(b'B')
m3 = ord(b'C')
e = 65537

r1 = pow(m1, e) - c1 # A^e - A^e mod n
r2 = pow(m2, e) - c2 # B^e - B^e mod n
r3 = pow(m3, e) - c3
# both values are congruent to 0 mod n -> n = gcd(r2, r2)
# r1 and r2 are multiples of n, so their gcd must be n

# gcd between two numbers is not 100% n itself but can be a multiple of it
# better to increase the numbers
n = gcd(r1, r2, r3)

print(n)


# multiplicative attack with a small multiplier
s = 2

# s^e mod n -> this is the encryption of s
s_e = pow(s, e, n)

# modified ciphertext: c' = (c_flag * s^e) mod n
c_prime = (c_flag * s_e) % n
r.sendlineafter(b'> ', b'2')
r.sendlineafter(b'> ', b'A' * 72)

r.sendlineafter(b'> ', str(c_prime).encode())
r.recvuntil(b': ')
# the decryption will be:   m' = s * FLAG
m_prime = int(r.recvline(keepends=False))

# s * FLAG < n -> simply divide
# m = m' / s
flag_num = m_prime // s

# if mod n applies:
# s_inv = inverse(s, n)
# flag_num = (m_prime * s_inv) % n

flag = long_to_bytes(flag_num).decode()
print(flag)

