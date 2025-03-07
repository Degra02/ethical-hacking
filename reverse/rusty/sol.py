from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii

c1 = (0x82184ad21431d70b).to_bytes(8, 'little')
c2 = (0x3dd17e32b49ae14d).to_bytes(8, 'little')
c3 = (0x150049113afb7336).to_bytes(8, 'little')
c4_0 = (0xfb7a0952ad1dcc6e).to_bytes(8, 'little')
c4_8 = (0x5ce8d9a5).to_bytes(4, 'little')


cipher = AES.new(key, AES.MODE_ECB)


