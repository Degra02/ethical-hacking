#!/usr/bin/env python3
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

if os.path.exists("./flag.txt"):
    with open("./flag.txt", "rb") as f:
        FLAG = f.read().strip()
else:
    FLAG = b"UniTN{placeholder_flag}"


BLOCK_SIZE = 16
key = os.urandom(BLOCK_SIZE)

iv = os.urandom(BLOCK_SIZE)
cipher = AES.new(key, AES.MODE_CBC, iv)
encrypted = cipher.encrypt(pad(FLAG, BLOCK_SIZE))
print("Here is a session cookie for you: " + iv.hex() + encrypted.hex())

while True:
    try:
        cookie = input("Give me a session cookie to check (in hex)? ")
        cookie = bytes.fromhex(cookie.strip())
        iv = cookie[:BLOCK_SIZE]
        encrypted = cookie[BLOCK_SIZE:]

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted)
        decrypted = unpad(decrypted, BLOCK_SIZE)
        print("TODO implement actual validity check")
    except ValueError:
        print("Invalid session cookie")
