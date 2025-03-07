#!/usr/bin/env python3
import string
import random
import os
from Crypto.Cipher import DES

if os.path.exists("./flag.txt"):
    with open("./flag.txt", "rb") as f:
        FLAG = f.read().strip()
else:
    FLAG = b"UniTN{placeholder_flag}"


BLOCK_SIZE = 8

def pad(s: bytes):
    return s + b" " * (BLOCK_SIZE - (len(s) % BLOCK_SIZE))

def generate_key():
    return pad("".join(random.choice(string.digits) for _ in range(6)).encode())


k1 = generate_key()
k2 = generate_key()

cipher1 = DES.new(k1, DES.MODE_ECB)
cipher2 = DES.new(k2, DES.MODE_ECB)
enc1 = cipher1.encrypt(pad(b"The flag is: " + FLAG))
enc2 = cipher2.encrypt(enc1)

with open("message.txt", "w") as f:
    f.write(enc2.hex())
