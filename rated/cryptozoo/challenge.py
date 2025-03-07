#!/usr/bin/env python3
import os
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

FLAG = os.getenv("FLAG")
if not FLAG:
    FLAG = "UniTN{placeholder_flag}"

BLOCK_SIZE = 16
KEY = os.urandom(BLOCK_SIZE)
ALLOWED_CHARACTERS = string.ascii_letters + " .,;?!'\""


def sanitize(animal_name: str):
    for c in animal_name:
        if c not in ALLOWED_CHARACTERS:
            print(
                f"Nice try, but you can't have {c} in your animal name. The only characters allowed are: {ALLOWED_CHARACTERS}")
            return False
    if "rubberduck" in animal_name:
        print("A rubberduck, that thing is not fit for a zoo, it does not even move.")
        return False
    elif "Ferris" in animal_name:
        print("Ferris?!?! How can you even think of putting that in a zoo?")
        return False

    return True


def add_animal():
    print("Choose an animal to add to your zoo")
    animal_name = input("> ")
    sanitized = sanitize(animal_name)
    if not sanitized:
        return
    print("Choose another animal to add to your zoo")
    animal_name2 = input("> ")
    sanitized = sanitize(animal_name2)
    if not sanitized:
        return
    zoo = f"pet={animal_name}|pet={animal_name2}".encode()
    padded_zoo = pad(zoo, BLOCK_SIZE)

    iv = os.urandom(BLOCK_SIZE)
    cipher = AES.new(key=KEY, mode=AES.MODE_CBC, iv=iv)
    enc_zoo = cipher.encrypt(padded_zoo)
    print("Here's your zoo, I made sure to protect it with AES so that no one can tamper with it:",
          iv.hex() + enc_zoo.hex())


def view_zoo():
    try:
        print("Insert your encrypted zoo (hex)")
        iv_enc_zoo = bytes.fromhex(input("> "))
        iv, enc_zoo = iv_enc_zoo[:BLOCK_SIZE], iv_enc_zoo[BLOCK_SIZE:]
        cipher = AES.new(key=KEY, mode=AES.MODE_CBC, iv=iv)
        padded_zoo = cipher.decrypt(enc_zoo)
        zoo = unpad(padded_zoo, BLOCK_SIZE)

        pets = zoo.split(b"|")
        found_pets = []
        for pet in pets:
            pieces = pet.split(b"=")
            if pieces[0] == b"pet":
                found_pets.append(pieces[1])

        if b"Ferris" in found_pets and b"rubberduck" in found_pets:
            print("You can't have Ferris and a rubberduck in the same zoo, that's just cruel.")
            print("Take this flag and go away.")
            print(FLAG)
        else:
            print("Here are the animals in your zoo: ", ", ".join([p.decode() for p in found_pets]))
    except (ValueError, IndexError):
        print(
            "Hmm, something went wrong. You didn't try to tamper with the zoo, didn't you?")


print("Hi, welcome to the Zoo Keeper!")
print("After programming for many years I decided to take a break and start a zoo.")
print("Since I am not a fan of people, I decided to make it a virtual zoo.")
while True:
    print()
    print("What do you want to do?")
    print("1. Create a new zoo")
    print("2. View your zoo")
    option = input("> ")

    if option == "1":
        add_animal()
    elif option == "2":
        view_zoo()
    else:
        print("Bye!")
        break
