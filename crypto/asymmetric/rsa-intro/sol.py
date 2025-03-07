from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *
import pwn

r = remote('cyberchallenge.disi.unitn.it', 10500)
# r = process('./challenge.py')

pwn.context.log_level = "debug"

r.recvuntil(b':')
message = r.recvline().decode().strip()

int_mess = bytes_to_long(message.encode())

r.sendlineafter(b'? ', f'{int_mess}'.encode())

r.recvuntil(b': ')
p = int(r.recvline())

r.recvuntil(b': ')
q = int(r.recvline())

print(p, ' ', q)

n = p * q
phi = (p-1)*(q-1)

r.sendlineafter(b'? ', str(n).encode())
r.sendlineafter(b'? ', str(phi).encode())


e = 65537
d = pow(e, -1, phi)
r.sendlineafter(b'? ', str(pow(e, -1, phi)).encode())
r.sendlineafter(b'? ', str(pow(int_mess, e, n)).encode())

r.recvuntil(b': ')
cipher = r.recvline()

dec_flag = pow(int(cipher), d, n)
flag = long_to_bytes(dec_flag)
print(flag)
