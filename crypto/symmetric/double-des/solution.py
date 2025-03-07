import string
import random
import os
from Crypto.Cipher import DES

BLOCK_SIZE = 8

def pad(s: bytes):
    return s + b" " * (BLOCK_SIZE - (len(s) % BLOCK_SIZE))

def generate_key():
    return pad("".join(random.choice(string.digits) for _ in range(6)).encode())


enc = bytes.fromhex(open('./message.txt', 'rb').read().decode())

plain = b"The flag"

enck1s = {}

for k1 in range(000000, 999999):
    k1 = ('{:06d}'.format(k1) + "  ").encode()
    c1 = DES.new(k1, DES.MODE_ECB)
    enck1 = c1.encrypt(plain)
    enck1s[enck1] = k1


for k2 in range(000000, 999999):
    k2 = ('{:06d}'.format(k2) + "  ").encode()
    c2 = DES.new(k2, DES.MODE_ECB)

    deck2 = c2.decrypt(enc[:8])

    if deck2 in enck1s:
        dec2 = c2.decrypt(enc)

        c1 = DES.new(enck1s[deck2], DES.MODE_ECB)
        pl = c1.decrypt(dec2)
        print(pl)








