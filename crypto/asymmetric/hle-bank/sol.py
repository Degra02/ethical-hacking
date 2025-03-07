from pwn import *
import hlextend


r = remote('cyberchallenge.disi.unitn.it', 10201)

r.sendlineafter(b'> ', b'1')
r.sendlineafter(b'> ', b'pippo')
r.sendlineafter(b'> ', b'poppi')

r.recvuntil(b': ')
login_token = r.recvline(keepends=False)

r.recvuntil(b': ')
password = r.recvline(keepends=False)

sha = hlextend.new('sha1')
richperson_login = sha.extend(b'||||richperson', b'poppi||||pippo', 32, password.decode())
new_passw = sha.hexdigest()

r.sendlineafter(b'> ', b'2')
r.sendlineafter(b'> ', richperson_login.hex())
r.sendlineafter(b'> ', new_passw.encode())

r.interactive()

