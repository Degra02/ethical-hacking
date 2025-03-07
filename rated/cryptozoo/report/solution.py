from pwn import remote

BLOCK_SIZE = 16

def first_exploit(r):
    r.sendlineafter(b'> ', b'1')
    r.sendlineafter(b'> ', b'Ferriy')     # Blocks configuration
    r.sendlineafter(b'> ', b'uubberduck') # "IVIVIVIVIVIVIVIV"
                                          # "pet=Ferriy|pet=u"
                                          # "ubberduck0000000"
    r.recvuntil(b': ')
    iv_ct = bytearray.fromhex(r.recvline().strip().decode())
    iv = iv_ct[:BLOCK_SIZE]; ct = iv_ct[BLOCK_SIZE:]

    delta1 = ord('y') ^ ord('s')
    iv[9] ^= delta1
    delta2 = ord('u') ^ ord('r')
    iv[-1] ^= delta2

    modified_ct = bytes(iv) + bytes(ct)

    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'> ', modified_ct.hex().encode())

    r.recvline(); r.recvline()
    print(f"First flag: {r.recvline().decode().strip()}") # Flag

def second_exploit(r):
    r.sendlineafter(b'> ', b'1')
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
    iv_ct = bytearray.fromhex(r.recvline().strip().decode())
    iv = iv_ct[:BLOCK_SIZE]; ct = iv_ct[BLOCK_SIZE:]

    ct[32] ^= (0x2 ^ 0x7) << 4   # high nibble bit flip:  , (0x2c) -> | (0x7c)
    ct[36] ^= (0xb ^ 0xd)        # low nibble bit flip:   ; (0x3b) -> = (0x3d)
    ct[37] ^= (0x6 ^ 0x2)        # low nibble bit flip:   v (0x76) -> r (0x72)
    ct[47] ^= (0x2 ^ 0x7) << 4   # high nibble bit flip:  , (0x2c) -> | (0x7c)
    delta3 = ord('t') ^ ord('F') # full byte bit flip:    t (0x74) -> F (0x46)
    ct[69] ^= delta3
    ct[75] ^= (0x4 ^ 0xc)        # low nibble bit flip:   t (0x74) -> | (0x7c)

    modified_ct = bytes(iv) + bytes(ct)
    r.sendlineafter(b'> ', b'2')
    r.sendlineafter(b'> ', modified_ct.hex().encode())

    r.recvline()
    print(f"Second flag: {r.recvline().decode().strip()}") # Flag


# ======== First version ========
r1 = remote('cyberchallenge.disi.unitn.it', 50100)
first_exploit(r1)

# ======== Second version ========
r2 = remote('cyberchallenge.disi.unitn.it', 50101)
second_exploit(r2)

