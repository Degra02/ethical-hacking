#!/usr/bin/env python3
import os
from Crypto.Cipher import AES
from Crypto.Hash import MD5

if os.path.exists("./flag.txt"):
    with open("./flag.txt", "rb") as f:
        FLAG = f.read().strip()
else:
    FLAG = b"UniTN{placeholder_flag}"


key = os.urandom(16)
message = os.urandom(64)
print("Here is a key (hex):", key.hex())
print("Here is a message (hex):", message.hex())

encrypted = input("What is the AES encrypted message using the given key (hex)? ")
encrypted = bytes.fromhex(encrypted)
aes = AES.new(key, AES.MODE_ECB)
if aes.encrypt(message) != encrypted:
    print("Nope")
    exit()

digest = input("What is the the MD5 hash digest of the message (hex)? ")
md5 = MD5.new(message)
if md5.hexdigest() != digest:
    print("Nope")
    exit()

print(FLAG)
