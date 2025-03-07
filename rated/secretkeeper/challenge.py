#!/usr/bin/env python3
import os

from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long


FLAG = os.getenv("FLAG")
if not FLAG:
    FLAG = "UniTN{placeholder_flag}"

rsa = RSA.generate(1024)
print(rsa.n)

def encrypt(m):
    return pow(m, rsa.e, rsa.n)


def decrypt(c):
    return pow(c, rsa.d, rsa.n)


def protect():
    print("Enter your secret:")
    secret = input("> ")
    secret = bytes_to_long(secret.encode())
    print("Encrypting your secret...")
    encrypted = encrypt(secret)
    print("Here is your encrypted secret:", encrypted)


def show():
    print("Enter the encrypted secret:")
    encrypted = int(input("> "))
    print("Decrypting your secret...")
    decrypted = decrypt(encrypted)
    if decrypted == bytes_to_long(FLAG.encode()):
        print("Keep your hands off my secret!")
    else:
        print("Here is your secret:", decrypted)
        print("Due to budget cuts it is in numerical form.")

def main():
    print("Do you want to know my biggest secret?")
    print("Here it is:", encrypt(bytes_to_long(FLAG.encode())))
    print("I encrypted it using RSA so that you can see it, but you can't decrypt it.")
    print("Using my service you can do the same for your secrets.")
    # print("Since I can't afford to store this data, take the public key with you.", rsa.export_key())

    print("What do you want to do?")
    while True:
        print("1. Protect a secret")
        print("2. Decrypt a secret")
        option = input("> ")

        if option == "1":
            protect()
        elif option == "2":
            show()
        else:
            print("Invalid option, try again.")
            import sys
            sys.exit(0)

if __name__ == "__main__":
    main()
