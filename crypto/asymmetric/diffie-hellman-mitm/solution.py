import pwn
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from hashlib import sha256

r = pwn.remote("cyberchallenge.disi.unitn.it", "10401")

pwn.context.log_level = "debug"

def receive():
    r.recvuntil(b": ")
    return r.recvline(keepends=False)


BLOCK_SIZE = 16
p = 2410312426921032588552076022197566074856950548502459942654116941958108831682612228890093858261341614673227141477904012196503648957050582631942730706805009223062734745341073406696246014589361659774041027169249453200378729434170325843778659198143763193776859869524088940195577346119843545301547043747207749969763750084308926339295559968882457872412993810129130294592999947926365264059284647209730384947211681434464714438488520940127459844288859336526896320919633919
g = 2


priv = 2 # = b_alice = b_bob


# receive from alice
r.recvuntil(b": ")
r.recvuntil(b": ")
r.recvuntil(b": ")


alice_ga = int(r.recvline(keepends=False).decode())

ga_fake = pow(g, priv, p)
r.sendlineafter(b": ", str(ga_fake).encode())

r.recvuntil(b": ")
bob_ga = int(r.recvline(keepends=False).decode())

gb_fake = pow(g, priv, p)
r.sendlineafter(b": ", str(gb_fake).encode())


key_alice = pow(alice_ga, priv, p)
key_a = sha256(long_to_bytes(key_alice)).digest()[-BLOCK_SIZE:]
aes_a = AES.new(key_a, AES.MODE_ECB)

key_bob = pow(bob_ga, priv, p)
key_b = sha256(long_to_bytes(key_bob)).digest()[-BLOCK_SIZE:]
aes_b = AES.new(key_b, AES.MODE_ECB)

alice_enc = bytes.fromhex(receive().decode())
alice_dec = aes_a.decrypt(alice_enc)
print(alice_dec)

bob_enc = aes_b.encrypt(alice_dec)
r.sendlineafter(b": ", bob_enc.hex().encode())

bob_enc = bytes.fromhex(receive().decode())
bob_dec = aes_b.decrypt(bob_enc)
print(bob_dec)


