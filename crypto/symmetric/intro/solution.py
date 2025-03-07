from Crypto.Cipher import AES
from Crypto.Hash import MD5
from pwn import *


r = remote('cyberchallenge.disi.unitn.it', 10003)

r.recvuntil(b':')
key = bytes.fromhex(r.recvline().strip().decode())
print(key)

r.recvuntil(b':')
message = bytes.fromhex(r.recvline().strip().decode())
print(message)

aes = AES.new(key, AES.MODE_ECB)
enc = aes.encrypt(message)
print(enc)

r.recvuntil(b'? ')
r.sendline(enc.hex().encode())

r.recvuntil(b'? ')

md5 = MD5.new(message)
r.sendline(md5.hexdigest().encode())

r.interactive()

