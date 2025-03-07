import pwn
import itertools

BLOCK_SIZE = 16

def splitEvery(s: bytes, n: int) -> list:
    """splits a byte array (or a string) into chunks of length n"""
    return [s[i:i+n] for i in range(0, len(s), n)]

def xorBytes(var: bytes, key: bytes) -> bytes:
    """Xors the two byte arrays, repeating the second one if needed and
    returning another byte array with the same length as the first parameter"""
    return bytes(a ^ b for a, b in zip(var, itertools.cycle(key)))


#r = pwn.process(["python", "challenge.py"])
r = pwn.remote("cyberchallenge.disi.unitn.it", 10102)

r.recvuntil(b": ")
blocks = splitEvery(bytes.fromhex(r.recvline(keepends=False).decode("utf-8")), BLOCK_SIZE)

res = b''
for i in range(len(blocks)-1):
    # contains the characters recovered so far from the end of this block
    prev = b''

    # try to decrypt block i+1, by using block i as IV
    for j in range(BLOCK_SIZE):
        # the last block will already have correct padding, so if we started with
        # 1 we would get back from the server that the padding is correct, instead
        # of being able to guess the last byte of the padded block
        for k in [0] + list(range(2, 256)) + [1]:
            # construct the IV so that, when AES-CBC decryption will XOR it with the
            # decrpyted ciphertext, the resulting plaintext has correct padding (i.e.
            # the byte j+1 repeated j times) up until the current character we are
            # trying to guess
            padding = bytes([k^(j+1)] + [v^(j+1) for v in prev])
            iv = xorBytes(b'\0'*(BLOCK_SIZE-len(padding)) + padding, blocks[i])

            r.sendlineafter(b"? ", (iv + blocks[i+1]).hex().encode("utf-8"))
            line = r.recvline(keepends=False)

            # if we got back "TODO" it means the decryption went well
            #  => therefore the padding was correct
            # ~=> therefore the j+1-th byte from the end of the block is equal to j+1
            #       (just like all last j bytes, as we constructed above)
            # <=> therefore k^(j+1)^(character we want to guess) = (j+1)
            # <=> therefore k = (character we want to guess)
            if b"TODO" in line:
                prev = bytes([k]) + prev
                print("Got it!", prev)
                break
    res += prev
print(res)
