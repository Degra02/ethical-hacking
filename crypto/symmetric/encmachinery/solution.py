from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pwn import *
import string

def decrypt(c: bytes) -> bytes:
    for _ in range(3):
        c = bytes.fromhex(c.decode())

    c = unpad(c, BLOCK_SIZE)
    return c

def splitEvery(s: bytes, n: int) -> list:
    return [s[i:i+n] for i in range(0, len(s), n)]

BLOCK_SIZE = 16
r = remote('cyberchallenge.disi.unitn.it', 10101)
r.recvuntil(b'secrets: ')

enc = splitEvery(r.recvline(keepends=False), 32)

r.recvuntil(b'? ')

payload = ""
for a in string.printable:
    for b in string.printable:
        payload += a + b


r.sendline(payload.encode('utf-8').hex().encode())
r.recvuntil(b': ')

encrypted_char_pairs = splitEvery(r.recvline(keepends=False), 32)

for flag_char_pair in enc:
    try:
        index = encrypted_char_pairs.index(flag_char_pair)
        print(payload[index*2 : index*2+2], end="")
    except ValueError:
        print("", end="")
print()


