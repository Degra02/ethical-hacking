from pwn import *

BLOCK_SIZE = 16

r = remote('cyberchallenge.disi.unitn.it', 50100)
# r = process('./challenge.py')

r.recvuntil(b'> ')
r.sendline(b'1')

r.sendlineafter(b'> ', b'Ferriy')
r.sendlineafter(b'> ', b'uubberduck')

# "iv"
# "pet=Ferriy|pet=u"
# "ubberduck0000000"

r.recvuntil(b': ')
ciphertext = bytes.fromhex(r.recvline().strip().decode())
print(ciphertext)

iv = ciphertext[:BLOCK_SIZE]
print("IV: ", iv)

x1 = iv[9].to_bytes()
d1 = ord('y') ^ ord('s')
r1 = bytes(a ^ b for a,b in zip(x1, d1.to_bytes()))

x2 = iv[-1].to_bytes()
d2 = ord('u') ^ ord('r')
r2 = bytes(a ^ b for a,b in zip(x2, d2.to_bytes()))

iv_forgiato = iv[:9] + r1 + iv[10:15] + r2
print("IV forg: ", iv_forgiato)

cipher_forgiato = iv_forgiato + ciphertext[BLOCK_SIZE:]
print("Cipher forg: ", cipher_forgiato)

r.sendlineafter(b'> ', b'2')
r.sendlineafter(b'> ', cipher_forgiato.hex().encode())

print(r.recvline())
print(r.recvline())
print(r.recvline())

