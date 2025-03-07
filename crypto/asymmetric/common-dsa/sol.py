from hashlib import sha256
from Crypto.Util.number import bytes_to_long, inverse
from pwn import remote
import pwn

io = remote("cyberchallenge.disi.unitn.it", 10503)
pwn.context.log_level = 'debug'

p = 13232376895198612407547930718267435757728527029623408872245156039757713029036368719146452186041204237350521785240337048752071462798273003935646236777459223
q = 857393771208094202104259627990318636601332086981
g = 5421644057436475141609648488325705128047428394380474376834667300766108262613900542681289080713724597310673074119355136085795982097390670890367185141189796


def get_signature(message):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"Message (in hex): ", message.hex())
    io.recvuntil(b'r: ')
    r = int(io.recvline(keepends=False).decode())

    io.recvuntil(b's: ')
    s = int(io.recvline(keepends=False).decode())
    return r, s

m1 = b"hello"
m2 = b"test"
r1, s1 = get_signature(m1)
r2, s2 = get_signature(m2)

print(r1, s1)
print(r2, s2)

h1 = bytes_to_long(sha256(m1).digest()) % q
h2 = bytes_to_long(sha256(m2).digest()) % q

k = ((h1 - h2) * inverse(s1 - s2, q)) % q

d = ((s1 * k - h1) * inverse(r1, q)) % q

message = b"get_flag"
h = bytes_to_long(sha256(message).digest()) % q
r = pow(g, k, p) % q
s = ((h + d * r) * inverse(k, q)) % q

io.sendlineafter(b"> ", b"2")
io.sendlineafter(b"Command (in hex): ", message.hex().encode())
io.sendlineafter(b"r: ", str(r))
io.sendlineafter(b"s: ", str(s))

io.interactive()
