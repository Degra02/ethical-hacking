#!/usr/bin/env python3
import os

import bcrypt
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes


FLAG = os.getenv("FLAG")
if not FLAG:
    FLAG = "UniTN{placeholder_flag}"

SALT = bcrypt.gensalt()
rsa = RSA.generate(1024)

hashes = set()


def encrypt(m):
    return pow(m, rsa.e, rsa.n)


def decrypt(c):
    return pow(c, rsa.d, rsa.n)


def protect():
    print("Enter your name:")
    name = input("> ")
    print("Enter your secret:")
    secret = input("> ")
    secret = bytes_to_long(secret.encode())
    encrypted = encrypt(secret)
    print("Here is your encrypted secret:", encrypted)
    integrity_token = name.encode() + long_to_bytes(encrypted)
    # TODO check if big strings can cause any issue
    hashes.add(bcrypt.hashpw(integrity_token, SALT))


def show():
    print("Enter your name:")
    name = input("> ")
    print("Enter the encrypted secret:")
    encrypted = int(input("> "))
    if encrypted < 0:
        print("Negative numbers are not allowed anymore for security reasons.")
        return

    integrity_token = name.encode() + long_to_bytes(encrypted)
    hash_token = bcrypt.hashpw(integrity_token, SALT)
    if hash_token not in hashes:
        print("Integrity check failed.")
        return
    print("Decrypting your secret...")
    decrypted = decrypt(encrypted)
    if decrypted == bytes_to_long(FLAG.encode()):
        print("Keep your hands off my secret!")
    else:
        print("Here is your secret:", decrypted)
        print("People seemed to like the numbers so here it is still in numerical form.")


def main():
    print("Do you want to know my biggest secret?")
    print("Here it is:", encrypt(bytes_to_long(FLAG.encode())))
    print("I encrypted it using RSA so that you can see it, but you can't decrypt it.")
    print("Thanks to the great success of the last version, and the not so great issues, I decided to add a new feature.")
    print("Now you add your name to your secret, and thanks to bcrypt only valid pairs of username,secret will be decrypted.")
    while True:
        print("What do you want to do?")
        print("1. Protect a secret")
        print("2. Decrypt a secret")
        option = input("> ")

        if option == "1":
            protect()
        elif option == "2":
            show()
        else:
            import sys
            print("Invalid option")
            sys.exit(0)


if __name__ == "__main__":
    main()
