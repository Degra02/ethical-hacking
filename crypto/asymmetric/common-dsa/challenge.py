#!/usr/bin/env python3
from hashlib import sha256
from Crypto.Util.number import isPrime, bytes_to_long
from random import randint
import os

if os.path.exists("./flag.txt"):
    with open("./flag.txt", "r") as f:
        FLAG = f.read().strip()
else:
    FLAG = "UniTN{placeholder_flag}"


p = 13232376895198612407547930718267435757728527029623408872245156039757713029036368719146452186041204237350521785240337048752071462798273003935646236777459223
q = 857393771208094202104259627990318636601332086981
g = 5421644057436475141609648488325705128047428394380474376834667300766108262613900542681289080713724597310673074119355136085795982097390670890367185141189796

assert isPrime(p)

d = randint(2, q-1)
e = pow(g, d, p)

def dsa(m, k):
    h = bytes_to_long(sha256(m).digest()) % q
    r = pow(g, k, p) % q
    inverse_k = pow(k, -1, q)
    s = (h + d*r)*inverse_k % q
    return r, s

def verify(m, r, s):
    h = bytes_to_long(sha256(m).digest()) % q
    inverse_s = pow(s, -1, q)
    if r < 1 or r > q:
        return False
    else:
        ers = pow(e, r*inverse_s % q,  p)
        ghs = pow(g, h*inverse_s % q, p)
        return r == (ers * ghs % p) % q


def menu():
    k = randint(1, q-1)
    while True:
        print("1. Sign message")
        print("2. Get flag")
        option = int(input("> "))

        if option == 1:
            m = bytes.fromhex(input("Message (in hex): "))
            if b"flag" in m:
                print("No hacks please")
                continue

            r, s = dsa(m, k)
            print("r:", r)
            print("s:", s)

        elif option == 2:
            m = bytes.fromhex(input("Command (in hex): "))

            if m != b"get_flag":
                print("The only possible command is: get_flag")
                continue

            print("Give me the signature!")
            r = int(input("r: "))
            s = int(input("s: "))

            if verify(m, r, s):
                print(FLAG)
            else:
                print("Try harder!")

menu()
