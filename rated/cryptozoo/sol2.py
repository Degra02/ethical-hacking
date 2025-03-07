from pwn import remote, process

# r = remote('cyberchallenge.disi.unitn.it', 50101)
r = process('./challenge-2.py')

r.recvuntil(b'> ')
r.sendline(b'1')

r.sendlineafter(b'> ', b'A' * 23)
r.sendlineafter(b'> ', b',pet;vubberduck,AAAAAAAAAAAAAAAA')

# Blocks configuration
# "IVIVIVIVIVIVIVIV" Initialization Vector
# "pet=BillTheRock|" Must not change
# "pet=AAAAAAAAAAAA" First animal used for bitflips
# "AAAAAAAAAAA|pet=" ...
# "Xpet;vubberduckX" -> |pet=rubberduck|
# "AAAAAAAAAAAAAAAA" Second part of second animal used for bitflips
# "|pet=terristhepr" -> |pet=Ferris|hepr
# "ill0000000000000"

r.recvuntil(b': ')
ciphertext_hex = r.recvline().strip().decode()

BLOCK_SIZE = 16
iv_ct = bytearray.fromhex(ciphertext_hex)
iv = iv_ct[:BLOCK_SIZE]
ct = iv_ct[BLOCK_SIZE:]

ct[32] ^= (0x2 ^ 0x7) << 4   # high nibble bit flip:  , (0x2c) -> | (0x7c)
ct[36] ^= (0xb ^ 0xd)        # low nibble bit flip:   ; (0x3b) -> = (0x3d)
ct[37] ^= (0x6 ^ 0x2)        # low nibble bit flip:   v (0x76) -> r (0x72)
ct[47] ^= (0x2 ^ 0x7) << 4   # high nibble bit flip:  , (0x2c) -> | (0x7c)
delta3 = ord('t') ^ ord('F') # F of terristheprill -> must change whole byte
ct[69] ^= delta3
ct[75] ^= (0x4 ^ 0xc)        # low nibble bit flip:   , (0x74) -> | (0x7c)

modified_ct = bytes(iv) + bytes(ct)
r.sendlineafter(b'> ', b'2')
r.sendlineafter(b'> ', modified_ct.hex().encode())

r.recvline().decode().strip()
print(r.recvline().decode().strip()) # Flag
