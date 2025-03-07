
from pwn import *

BLOCK_SIZE = 16

# r = remote('cyberchallenge.disi.unitn.it', 50101)
r = process('./challenge-2.py')

r.recvuntil(b'> ')
r.sendline(b'1')

r.sendlineafter(b'> ', b'AAAAAAAAAAAAAAAAA')
r.sendlineafter(b'> ', b'tubberduckXAAAAAAAAAAA')

r.recvuntil(b': ')
ciphertext_hex = r.recvline().strip().decode()
log.info("original ciphertext: " + ciphertext_hex)

ciphertext = bytearray.fromhex(ciphertext_hex)
iv = ciphertext[:BLOCK_SIZE]
ct = ciphertext[BLOCK_SIZE:]

# ferristheprill can be changed to Ferris|heprill

# "IVIVIVIVIVIVIVIV"
# "pet=BillTheRock|"
# "pet=AAAAAAAAAAAA"
# "AAAAAA|pet=Xtubbe" -> pet=rubberduck|
# "rduckXAAAAAAAAAA"
# "|pet=terristhepr" -> =Ferris|heprill0
# "ill0000000000000"

# | of |pet=tubber
delta0 = ord('|') ^ ord('|')
ct[21] ^= ord('|')

# r of tubberduckX
delta1 = ord('t') ^ ord('r')
ct[25] ^= delta1

# | of tubberduckX
delta2 = ord('X') ^ ord('|')
ct[30] ^= delta2

# F of terristheprill
delta3 = ord('t') ^ ord('F')
ct[49 + 4] ^= delta3

delta4 = ord('t') ^ ord('|')
ct[55 + 4] ^= delta4

modified_ct = bytes(iv) + bytes(ct)
log.info("Modified ciphertext: " + modified_ct.hex())

r.sendlineafter(b'> ', b'2')
r.sendlineafter(b'> ', modified_ct.hex().encode())

print(r.recvline().decode().strip())
print(r.recvline().decode().strip())
print(r.recvline().decode().strip())
