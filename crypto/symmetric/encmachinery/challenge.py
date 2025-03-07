#!/usr/bin/env python3
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

if os.path.exists("./flag.txt"):
    with open("./flag.txt", "rb") as f:
        FLAG = f.read().strip()
else:
    FLAG = b"UniTN{placeholder_flag}"


BLOCK_SIZE = 16
key = os.urandom(BLOCK_SIZE)
cipher = AES.new(key, AES.MODE_ECB)

def encrypt(m: bytes) -> bytes:
    # a bit of encoding to make hackerz more confused
    for _ in range(3):
        m = m.hex().encode("utf-8")
    m = pad(m, BLOCK_SIZE)
    return cipher.encrypt(m)

print("Welcome to EncMachinery™, the only encryption service so secure that even encrypted company secrets can be shared freely!")
print("Our encrypted company secrets: " + encrypt(FLAG).hex())
message = input("What do you want EncMachinery™ to encrypt (in hex)? ")
message = bytes.fromhex(message.strip())
print("Encrypted message: " + encrypt(message).hex())
